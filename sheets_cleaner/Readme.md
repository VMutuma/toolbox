# Google Sheets Data Cleaner

This project provides a Python script to automate the process of cleaning and deduplicating email lists stored across multiple worksheets within a Google Sheet. The cleaned data is then combined and written to a new (or existing) Google Sheet.

## Features

* **Google Sheets Integration:** Authenticates and reads data from multiple worksheets within a specified Google Sheet URL.
* **Robust Data Cleaning:**
    * Filters rows based on an 'Active' status column.
    * Removes emails containing 'support' in the address.
    * Fills missing 'Name' entries by extracting potential names from email addresses.
    * Removes duplicate rows within each sheet based on the email address.
* **Cross-Sheet Deduplication:** Combines data from all cleaned sheets and performs a final deduplication based on email address across the entire dataset.
* **Automated Google Sheet Output:** Writes the final cleaned email list to a specified output Google Sheet, creating it if it doesn't exist.
* **Detailed Logging:** Provides comprehensive log messages to both the console and a log file (`sheets_cleaner.log`) for tracking script execution, warnings, and errors.
* **Retry Mechanism:** Implements exponential backoff and retry logic for Google Sheets API calls to handle transient network issues and API rate limits.

## 🛠️ Prerequisites

Before running the script, ensure you have the following:

1.  **Python 3.x:** Installed on your system.
2.  **Required Python Libraries:**
    * `gspread`
    * `pandas`
    * `tenacity`
    * `requests`
    * `numpy`
3.  **Google Cloud Project & Service Account Key:**
    * A Google Cloud Project enabled with the Google Sheets API and Google Drive API.
    * A service account created within this project.
    * The JSON key file for this service account.
4.  **Google Sheet Permissions:** The Google Sheet you intend to read from (and write to) must be shared with the email address of your service account (e.g., `your-service-account-name@your-project-id.iam.gserviceaccount.com`) with `Editor` access.

## Setup

1.  **Clone or Download:** Get the `clean_sheets.py` file into a dedicated project directory.
2.  **Install Dependencies:**
    ```bash
    pip install gspread pandas tenacity requests numpy
    ```
3.  **Place Service Account Key:** Place your Google Service Account JSON key file in the same directory as `clean_sheets.py`. Rename it to something simple like `service_account.json` or update the `SERVICE_ACCOUNT_KEY_PATH` variable in the script accordingly.

## Configuration

Open `clean_sheets.py` and modify the following variables in the `--- Configuration Section ---` to match your setup:

* `SERVICE_ACCOUNT_KEY_PATH`: Path to your Google Service Account JSON key file (e.g., `'service_account.json'`).
* `GOOGLE_SHEET_URL`: The full URL of the Google Sheet you want to process.
* `EMAIL_STATUS_COLUMN`: The exact name of the column in your input sheets that indicates an email's status (e.g., 'Status'). Used for filtering 'Active' entries.
* `EMAIL_ADDRESS_COLUMN`: The exact name of the column containing email addresses (e.g., 'Email').
* `NAME_COLUMN`: The exact name of the column containing names (e.g., 'Name').
* `OUTPUT_SHEET_NAME`: The name for the new (or existing) sheet where the combined and cleaned data will be written (e.g., `'Combined_Cleaned_Newsletters_Email_List'`).
* `LOG_FILE_NAME`: Name for the log file (default: `sheets_cleaner.log`).
* `LOG_LEVEL`: Logging verbosity (`logging.INFO` for general, `logging.DEBUG` for more detailed).

## How to Run

Navigate to your project directory in the terminal or command prompt and run the script:

```bash
python clean_sheets.py