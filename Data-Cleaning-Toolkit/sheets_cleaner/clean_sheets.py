import gspread
import pandas as pd
import re
import numpy as np
import time
import logging
import os
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type, after_log
from gspread.exceptions import APIError
from requests.exceptions import RequestException, ConnectionError 

# --- Configuration Section ---
SERVICE_ACCOUNT_KEY_PATH = 'Add your service account key JSON file path here'  # Replace with your actual service account key file path
# Ensure the service account has Editor access to the Google Sheet you want to modify
GOOGLE_SHEET_URL = 'Add Google Sheets URL here'  # Replace with your actual Google Sheets URL
EMAIL_STATUS_COLUMN = 'Status'
EMAIL_ADDRESS_COLUMN = 'Email'
NAME_COLUMN = 'Name'
OUTPUT_SHEET_NAME = 'Combined_Cleaned_Newsletters_Email_List'

# --- Logging Configuration ---
LOG_FILE_NAME = 'sheets_cleaner.log'
LOG_LEVEL = logging.INFO

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(SCRIPT_DIR, LOG_FILE_NAME)

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode='a'),
        logging.StreamHandler()
    ]
)

# --- Tenacity Retry Decorator Configuration ---
# Retry on both gspread's APIError and requests' general request exceptions
standard_gspread_retry = retry(
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception_type((APIError, RequestException)),
    after=after_log(logging.getLogger(), logging.WARNING)
)

# --- End Configuration Section ---


@standard_gspread_retry
def authenticate_google_sheets(key_path):
    """Authenticates with Google Sheets using a service account."""
    gc = gspread.service_account(filename=key_path)
    logging.info("Successfully authenticated with Google Sheets.")
    print("Authenticated with Google Sheets.")
    return gc

@standard_gspread_retry
def get_google_sheet(gc, sheet_url):
    """Opens the Google Sheet by URL."""
    try:
        spreadsheet = gc.open_by_url(sheet_url)
        logging.info(f"Successfully opened Google Sheet: '{spreadsheet.title}'")
        print(f"Opened Google Sheet: '{spreadsheet.title}'")
        return spreadsheet
    except gspread.exceptions.SpreadsheetNotFound:
        logging.error(f"Spreadsheet not found at URL: {sheet_url}")
        logging.error("Please check the URL and ensure the service account has Editor access to the sheet.")
        print("ERROR: Spreadsheet not found or accessible. Check log for details.")
        exit()
    except Exception as e:
        logging.error(f"Error opening spreadsheet: {e}", exc_info=True)
        print("ERROR: Could not open spreadsheet. Check log for details.")
        exit()

def read_all_sheets_to_dfs(spreadsheet):
    """
    Reads all worksheets from the spreadsheet into a dictionary of Pandas DataFrames.
    Implements an outer retry loop for sheets that fail to be read.
    """
    all_dfs = {}
    
    @standard_gspread_retry
    def _get_all_worksheet_titles(spreadsheet_obj):
        return [ws.title for ws in spreadsheet_obj.worksheets()]

    worksheet_titles = _get_all_worksheet_titles(spreadsheet)
    logging.info(f"Found {len(worksheet_titles)} worksheets in the spreadsheet.")

    absolutely_required_cols = [NAME_COLUMN, EMAIL_ADDRESS_COLUMN]

    # Initialize sheets to process and their retry counts
    sheets_to_process = list(worksheet_titles)
    max_external_retries = 3 
    sheet_attempt_counts = {title: 0 for title in worksheet_titles}
    
    @standard_gspread_retry
    def _get_worksheet_obj(spreadsheet_obj, title):
        return spreadsheet_obj.worksheet(title)

    @standard_gspread_retry
    def _get_sheet_data(worksheet):
        return worksheet.get_all_values()

    while sheets_to_process:
        current_round_failures = []
        logging.info(f"\n--- Starting retry round for {len(sheets_to_process)} sheets ---")

        for title in sheets_to_process:
            sheet_attempt_counts[title] += 1
            current_attempt = sheet_attempt_counts[title]

            if current_attempt > max_external_retries:
                logging.error(f"  Sheet '{title}' failed after {max_external_retries} total attempts. Permanently skipping this sheet.")
                continue 

            logging.info(f"  Attempting to read sheet '{title}' (Overall attempt {current_attempt}/{max_external_retries})...")

            try:
                ws = _get_worksheet_obj(spreadsheet, title)

                data = _get_sheet_data(ws)
                
                if not data:
                    logging.info(f"  Skipping empty sheet: '{title}' (no data rows).")
                    continue 

                # Convert to DataFrame
                df = pd.DataFrame(data[1:], columns=data[0])

                missing_abs_required_cols = [col for col in absolutely_required_cols if col not in df.columns]
                if missing_abs_required_cols:
                    logging.warning(f"  Sheet '{title}' is missing mandatory columns ({', '.join(missing_abs_required_cols)}). Skipping this sheet due to structural invalidity.")
                    continue 

                all_dfs[title] = df
                logging.info(f"  Successfully read and parsed '{title}' with {len(df)} rows.")

            except (APIError, RequestException, ConnectionError) as e:
                # Catch specific API/network errors that tenacity might have re-raised after its internal retries
                logging.warning(f"  API/Network error after internal retries for sheet '{title}': {e}. Adding to retry queue.")
                current_round_failures.append(title)
            except Exception as e:
                # Catch any other unexpected errors during processing a sheet
                logging.error(f"  Unexpected error processing sheet '{title}': {e}. Adding to retry queue.", exc_info=True)
                current_round_failures.append(title)
        
        # If there are still sheets that failed this round, set them for the next round
        sheets_to_process = current_round_failures

        if sheets_to_process:
            logging.info(f"  {len(sheets_to_process)} sheets failed this round and will be re-attempted. Waiting before next attempt...")
            time.sleep(10) 
        else:
            logging.info("  All remaining sheets processed successfully or permanently skipped.")

    return all_dfs

def extract_name_from_email(email):
    """
    Extracts a potential name from an email address.
    """
    if pd.isna(email) or not isinstance(email, str) or not email.strip():
        return None

    local_part = email.split('@')[0]
    name = re.sub(r'[._-]', ' ', local_part)
    name = ' '.join(word.capitalize() for word in name.split())
    name = re.sub(r'(?<=\w)(\d+)$', '', name)

    return name.strip() if name else None

def clean_and_transform_data(df, email_status_col, email_address_col, name_col):
    """
    Cleans a single DataFrame:
    - Conditionally filters for 'Active' email status (if status column exists).
    - Removes 'support' emails.
    - Populates missing names from email addresses.
    - Selects and reorders only 'Name' and 'Email' columns.
    - Removes duplicates based on email address.
    """
    initial_rows = len(df)
    logging.info(f"    Initial rows in sheet: {initial_rows}")

    for col in [email_address_col, name_col]:
        if col in df.columns:
            df[col] = df[col].astype(str)
        else:
            logging.error(f"    Critical column '{col}' not found in DataFrame. Skipping transformation for this sheet.")
            return pd.DataFrame(columns=[name_col, email_address_col])

    if email_status_col in df.columns:
        df[email_status_col] = df[email_status_col].astype(str)
        rows_before_status_filter = len(df)
        df = df[df[email_status_col].str.contains('Active', case=False, na=False)]
        logging.info(f"    Removed {rows_before_status_filter - len(df)} rows not 'Active'.")
    else:
        logging.info(f"    Skipping 'Active' status filtering: Email status column '{email_status_col}' not found in this sheet.")

    rows_before_support_filter = len(df)
    df = df[~df[email_address_col].str.contains('support', case=False, na=False)]
    logging.info(f"    Removed {rows_before_support_filter - len(df)} rows with 'support' emails.")

    df[name_col] = df[name_col].replace('', np.nan).replace('None', np.nan).replace('nan', np.nan)
    
    rows_with_missing_names = df[name_col].isna().sum()
    if rows_with_missing_names > 0:
        logging.info(f"    Attempting to fill {rows_with_missing_names} missing names from email addresses.")
        df[name_col] = df.apply(
            lambda row: extract_name_from_email(row[email_address_col]) if pd.isna(row[name_col]) else row[name_col],
            axis=1
        )
        filled_count = rows_with_missing_names - df[name_col].isna().sum()
        logging.info(f"    Filled {filled_count} names from emails.")
    else:
        logging.info("    No missing names to fill for this sheet.")

    df = df[[name_col, email_address_col]].copy()

    df[name_col] = df[name_col].astype(str).str.strip()
    df[email_address_col] = df[email_address_col].astype(str).str.strip()
    df[name_col] = df[name_col].replace('None', '').replace('nan', '')

    rows_before_dedupe = len(df)
    df.drop_duplicates(subset=[email_address_col], inplace=True)
    logging.info(f"    Removed {rows_before_dedupe - len(df)} duplicate rows based on email address (per sheet).")

    logging.info(f"    Cleaned sheet now has {len(df)} rows.")
    return df

def main():
    print("Starting sheets cleaner script...")
    logging.info("Script started.")

    gc = authenticate_google_sheets(SERVICE_ACCOUNT_KEY_PATH)
    spreadsheet = get_google_sheet(gc, GOOGLE_SHEET_URL)

    logging.info("Reading data from all worksheets...")
    all_dfs_raw = read_all_sheets_to_dfs(spreadsheet)

    if not all_dfs_raw:
        logging.warning("No data found in any sheets after initial checks. Exiting.")
        print("No data found. Exiting.")
        return

    print("\nCleaning and transforming data...")
    logging.info("Cleaning and transforming data in each worksheet...")
    all_dfs_cleaned = {}
    for sheet_title, df in all_dfs_raw.items():
        print(f"  Processing sheet: '{sheet_title}'")
        logging.info(f"  Processing sheet: '{sheet_title}'")
        cleaned_df = clean_and_transform_data(df.copy(), EMAIL_STATUS_COLUMN, EMAIL_ADDRESS_COLUMN, NAME_COLUMN)
        if not cleaned_df.empty:
            all_dfs_cleaned[sheet_title] = cleaned_df
        else:
            logging.warning(f"  Sheet '{sheet_title}' resulted in an empty DataFrame after cleaning. Not including in combined data.")

    print("\nCombining all cleaned data...")
    logging.info("Combining all cleaned data into a single DataFrame...")
    list_of_cleaned_dfs = list(all_dfs_cleaned.values())

    if not list_of_cleaned_dfs:
        logging.warning("No data left after cleaning and transformation. Exiting.")
        print("No data left. Exiting.")
        return

    combined_df = pd.concat(list_of_cleaned_dfs, ignore_index=True)
    logging.info(f"Total rows in initially combined DataFrame: {len(combined_df)}")
    print(f"Total rows in initially combined DataFrame: {len(combined_df)}")

    logging.info(f"Performing final deduplication on combined data based on '{EMAIL_ADDRESS_COLUMN}'...")
    initial_combined_rows = len(combined_df)
    if EMAIL_ADDRESS_COLUMN in combined_df.columns:
        combined_df.drop_duplicates(subset=[EMAIL_ADDRESS_COLUMN], inplace=True)
        logging.info(f"  Removed {initial_combined_rows - len(combined_df)} additional duplicates from combined data.")
    else:
        logging.warning(f"  Email address column '{EMAIL_ADDRESS_COLUMN}' not found in combined data for final deduplication.")
    logging.info(f"Final combined data size: {len(combined_df)} rows.")
    print(f"Final combined data size: {len(combined_df)} rows.")


    print(f"\nWriting combined and cleaned data to Google Sheet: '{OUTPUT_SHEET_NAME}'...")
    logging.info(f"Writing combined and cleaned data to Google Sheet: '{OUTPUT_SHEET_NAME}'...")
    try:
        @standard_gspread_retry
        def _get_or_create_worksheet(spreadsheet_obj, sheet_name, df_cols, df_rows):
            try:
                ws = spreadsheet_obj.worksheet(sheet_name)
                logging.info(f"  Existing sheet '{sheet_name}' found. Clearing content.")
                ws.clear()
                return ws
            except gspread.exceptions.WorksheetNotFound:
                logging.info(f"  Sheet '{sheet_name}' not found. Creating new sheet.")
                return spreadsheet_obj.add_worksheet(
                    title=sheet_name,
                    rows=str(df_rows + 1),
                    cols=str(df_cols)
                )

        output_worksheet = _get_or_create_worksheet(spreadsheet, OUTPUT_SHEET_NAME, len(combined_df.columns), len(combined_df))
        
        time.sleep(2)

        data_to_write = [combined_df.columns.values.tolist()] + combined_df.fillna('').values.tolist()

        @standard_gspread_retry
        def _update_sheet_data(worksheet, data):
            worksheet.update(data)

        _update_sheet_data(output_worksheet, data_to_write)
        
        logging.info(f"Successfully wrote {len(combined_df)} rows to '{OUTPUT_SHEET_NAME}'.")
        print(f"Successfully wrote {len(combined_df)} rows to '{OUTPUT_SHEET_NAME}'.")

    except Exception as e:
        logging.error(f"Error writing data back to Google Sheet: {e}", exc_info=True)
        print("ERROR: Could not write data back to Google Sheet. Check log for details.")

    logging.info("Script process complete.")
    print("\nProcess complete!")

if __name__ == "__main__":
    main()