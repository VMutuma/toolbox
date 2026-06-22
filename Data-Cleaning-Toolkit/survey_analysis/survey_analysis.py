import pandas as pd
import gspread
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_KEY_PATH = os.environ.get('SERVICE_ACCOUNT_KEY_PATH')
SURVEY_SHEET_URL = os.environ.get('SURVEY_SHEET_URL')
SURVEY_WORKSHEET_NAME = os.environ.get('SURVEY_WORKSHEET_NAME', 'Feedback_Report')
COLUMNS_TO_DROP = ['Referrer Name', 'Task Owner']

OUTPUT_EXCEL_FILE = 'Survey_Analysis_Report.xlsx'
CHARTS_DIR = Path('Survey_Charts')

CHARTS_DIR.mkdir(parents=True, exist_ok=True)

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('viridis')

def load_data_from_google_sheets(service_account_key_path: str, sheet_url: str, worksheet_name: str, columns_to_drop: list) -> pd.DataFrame | None:
    if not service_account_key_path or not sheet_url or not worksheet_name:
        print("Error: Google Sheets configuration (key path, URL, or worksheet name) is missing.")
        return None

    try:
        gc = gspread.service_account(filename=service_account_key_path)
        spreadsheet = gc.open_by_url(sheet_url)
        worksheet = spreadsheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        df = df.drop(columns=columns_to_drop, errors='ignore')
        return df
    except FileNotFoundError:
        print(f"Error: Service account key file not found at '{service_account_key_path}'. "
              "Please ensure the path is correct and accessible.")
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet not found at URL '{sheet_url}'. "
              "Please check the URL and ensure the service account has access.")
        return None
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet '{worksheet_name}' not found in the spreadsheet. "
              "Please check the worksheet name.")
        return None
    except gspread.exceptions.NoValidUrlKeyFound:
        print(f"Error: Invalid Google Sheet URL format: '{sheet_url}'. "
              "Ensure it's a valid Google Sheets URL.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data loading: {e}")
        return None

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame | None:
    if df is None:
        return None

    df['Added Time'] = pd.to_datetime(df['Added Time'], errors='coerce')

    multi_select_columns = [
        'Multi-select Question A',
        'Multi-select Question B',
        'Multi-select Question C',
        'Multi-select Question D',
        'Multi-select Question E',
        'Multi-select Question F'
    ]

    for col in multi_select_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(
                lambda x: [item.strip() for item in x.split(',') if item.strip()] if pd.notnull(x) and x.lower() != 'nan' else []
            )
    return df

def add_value_labels(ax, orient='v', fmt='{:.1f}%'):
    if orient == 'v':
        for p in ax.patches:
            height = p.get_height()
            if pd.notnull(height) and height > 0.001:
                ax.annotate(fmt.format(height) if fmt else f'{int(height)}',
                            (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='bottom', xytext=(0, 5), textcoords='offset points', fontsize=9)
    else:
        for p in ax.patches:
            width = p.get_width()
            if pd.notnull(width) and width > 0.001:
                ax.annotate(fmt.format(width) if fmt else f'{int(width)}',
                            (width, p.get_y() + p.get_height() / 2.),
                            ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9)

def get_single_choice_analysis_and_chart(dataframe: pd.DataFrame, column_name: str, chart_filename: Path) -> tuple[pd.DataFrame, Path | None]:
    analysis_df = pd.DataFrame({'Error': [f"Column '{column_name}' not found."]})
    chart_path = None

    if column_name in dataframe.columns:
        counts = dataframe[column_name].value_counts(dropna=False)
        percentages = dataframe[column_name].value_counts(dropna=False, normalize=True)
        analysis_df = pd.DataFrame({'Count': counts, 'Percentage': percentages})
        analysis_df.index.name = 'Response'
        
        analysis_df_sorted = analysis_df.sort_values(by='Count', ascending=False)

        plt.figure(figsize=(10, max(6, len(analysis_df_sorted) * 0.5)))
        ax = sns.barplot(x=analysis_df_sorted.index, y='Count', data=analysis_df_sorted,
                         hue=analysis_df_sorted.index, palette='viridis', legend=False)
        plt.title(f'Distribution of: {column_name}', fontsize=14)
        plt.xlabel('Response', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        
        add_value_labels(ax, fmt=None)
        plt.tight_layout()
        
        chart_path = CHARTS_DIR / chart_filename
        plt.savefig(chart_path)
        plt.close()
    return analysis_df, chart_path

def get_multi_select_analysis_and_chart(dataframe: pd.DataFrame, column_name: str, chart_filename: Path) -> tuple[pd.DataFrame, Path | None]:
    analysis_df = pd.DataFrame({'Error': [f"Column '{column_name}' not found."]})
    chart_path = None

    if column_name in dataframe.columns:
        all_selections = [item for sublist in dataframe[column_name].dropna() for item in sublist if item]
        
        if all_selections:
            selection_counts = pd.Series(all_selections).value_counts()
            
            num_respondents = len(dataframe)
            respondent_percentages = {}
            for option in selection_counts.index:
                count_for_option = dataframe[column_name].apply(lambda x: option in x if isinstance(x, list) else False).sum()
                respondent_percentages[option] = (count_for_option / num_respondents)

            analysis_df = pd.DataFrame({
                'Count of Selections': selection_counts,
                'Percentage of Respondents': pd.Series(respondent_percentages)
            }).sort_values(by='Percentage of Respondents', ascending=False)
            analysis_df.index.name = 'Option'

            plt.figure(figsize=(10, max(6, len(analysis_df) * 0.5)))
            ax = sns.barplot(x=analysis_df.index, y='Percentage of Respondents', data=analysis_df,
                             hue=analysis_df.index, palette='magma', legend=False)
            plt.title(f'Popularity of Options for: {column_name}', fontsize=14)
            plt.xlabel('Option', fontsize=12)
            plt.ylabel('Percentage of Respondents (%)', fontsize=12)
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=10)

            add_value_labels(ax, fmt='{:.1%}')
            plt.tight_layout()

            chart_path = CHARTS_DIR / chart_filename
            plt.savefig(chart_path)
            plt.close()
        else:
            analysis_df = pd.DataFrame({'Info': ["No selections made for this question."]})
    return analysis_df, chart_path

def get_rating_analysis_and_chart(dataframe: pd.DataFrame, column_name: str, chart_filename: Path) -> tuple[pd.DataFrame, Path | None]:
    analysis_df = pd.DataFrame({'Error': [f"Column '{column_name}' not found."]})
    chart_path = None

    if column_name in dataframe.columns:
        counts = dataframe[column_name].value_counts(dropna=False)
        percentages = dataframe[column_name].value_counts(dropna=False, normalize=True)
        analysis_df = pd.DataFrame({'Count': counts, 'Percentage': percentages})
        analysis_df.index.name = 'Rating'

        numeric_series = pd.to_numeric(dataframe[column_name], errors='coerce').dropna()
        
        common_rating_order = {
            'Excellent': 5, 'Very Good': 4, 'Good': 3, 'Average': 2, 'Poor': 1,
            'Highly beneficial': 5, 'Somewhat beneficial': 4, 'Minimal impact': 3, 'Not a significant contributor': 2,
            'Very likely': 5, 'Likely': 4, 'Neutral': 3, 'Unlikely': 2, 'Very unlikely': 1, 'Not sure': 0,
            'Extremely important': 5, 'Very important': 4, 'Moderately important': 3, 'Slightly important': 2, 'Not important at all': 1,
            'Satisfied': 5, 'Neutral': 3, 'Dissatisfied': 1,
            '50 - 100%': 4, '25-50%': 3, 'Less than 25%': 2,
            'Very satisfied': 5, 'Satisfied': 4, 'Neutral': 3, 'Dissatisfied': 2, 'Very dissatisfied': 1
        }

        ordered_ratings = []
        if all(isinstance(x, (int, float)) for x in counts.index):
            ordered_ratings = sorted(counts.index.tolist())
        else:
            sorted_items = sorted([(item, common_rating_order.get(item, -1)) for item in counts.index], key=lambda x: x[1], reverse=True)
            ordered_ratings = [item[0] for item in sorted_items if item[1] != -1]
            unordered_items = [item for item in counts.index if item not in ordered_ratings]
            ordered_ratings.extend(unordered_items)

        ordered_counts = [counts.get(r, 0) for r in ordered_ratings]

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(x=ordered_ratings, y=ordered_counts,
                         hue=ordered_ratings, palette='coolwarm', legend=False)
        plt.title(f'Ratings Distribution for: {column_name}', fontsize=14)
        plt.xlabel('Rating', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        add_value_labels(ax, fmt=None)
        plt.tight_layout()

        chart_path = CHARTS_DIR / chart_filename
        plt.savefig(chart_path)
        plt.close()

        if not numeric_series.empty:
            summary_stats = pd.DataFrame({
                'Statistic': ['Mean', 'Median', 'Mode'],
                'Value': [numeric_series.mean(), numeric_series.median(), ', '.join(map(str, numeric_series.mode().tolist()))]
            })
            analysis_df = pd.concat([analysis_df, summary_stats.set_index('Statistic')], axis=0)
            
    return analysis_df, chart_path

def create_pivot_table(df: pd.DataFrame, writer: pd.ExcelWriter):
    pivot_sheet_name = 'Flexible Pivot Table'
    worksheet = writer.book.add_worksheet(pivot_sheet_name)
    
    worksheet.write(0, 0, "Instructions: This is a flexible pivot table. Drag fields from the PivotTable Fields pane on the right into the Rows, Columns, Values, and Filters areas to explore the data.")
    worksheet.write(1, 0, "All categorical fields from the raw data are available for rows/columns/filters.")
    worksheet.write(2, 0, "For values, you can count responses for any categorical field (e.g., 'Added Time' for total respondents, or a specific rating field for counts).")
    
    max_row = len(df)
    max_col = len(df.columns)
    
    source_range_end_col = chr(ord('A') + max_col - 1)
    source_range = f"'Raw Data'!A1:{source_range_end_col}{max_row + 1}"

    worksheet.add_pivot_table({
        'data_range': source_range,
        'name': 'SurveyAnalysisPivot',
        'ref': 'A5',
        'rows': [],
        'columns': [],
        'values': [],
        'filters': [],
        'row_axis_is_discrete': True
    })

def main_analysis_script():
    df = load_data_from_google_sheets(SERVICE_ACCOUNT_KEY_PATH, SURVEY_SHEET_URL, SURVEY_WORKSHEET_NAME, COLUMNS_TO_DROP)

    if df is None:
        print("Exiting analysis due to data loading failure.")
        return

    df = preprocess_data(df)

    if df is None:
        print("Exiting analysis due to data preprocessing failure.")
        return

    print("Generating Survey Analysis Report...")

    try:
        with pd.ExcelWriter(OUTPUT_EXCEL_FILE, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Raw Data', index=False)

            analyses_config = {
                'Business Objectives': ('multi', 'Multi-select Question A'), 
                'Core Functionalities': ('single', 'Single-select Question B'),
                'Strategy Alignment': ('single', 'Single-select Question C'),
                'Key Provider Factors': ('single', 'Single-select Question D'),
                'Provider Role': ('single', 'Single-select Question E'), 
                'Service Significance': ('single', 'Single-select Question F'),
                'Business Contribution': ('single', 'Single-select Question G'), 
                'Objective Support Rating': ('rating', 'Rating Question H'), 
                'ROI Evaluation': ('rating', 'Rating Question I'), 
                'Average ROI Observed': ('rating', 'Rating Question J'),
                'Retention Factors': ('multi', 'Multi-select Question B'), 
                'Improvement Areas': ('multi', 'Multi-select Question C'), 
                'Future Usage Likelihood': ('single', 'Single-select Question K'), 
                'Future Communication Channels': ('single', 'Single-select Question L'), 
                'Interest in Feature X': ('single', 'Single-select Question M'), 
                'Interest in Feature Y': ('single', 'Single-select Question N'), 
                'Interest in Feature Z': ('single', 'Single-select Question O'), 
                'Impact of Emerging Tech': ('multi', 'Multi-select Question D'), 
                'Desired Tech Trends': ('multi', 'Multi-select Question E'), 
                'Importance of Channel Support': ('single', 'Single-select Question P'), 
                'Switching Triggers': ('multi', 'Multi-select Question F'), 
                'Single Change Request': ('single', 'Single-select Question Q'), 
                'Overall Satisfaction': ('single', 'Single-select Question R')
            }

            for sheet_name, (analysis_type, column_name) in analyses_config.items():
                safe_sheet_name = sheet_name[:31].replace('[', '_').replace(']', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('/', '_').replace('\\', '_')
                chart_filename = Path(f"{safe_sheet_name}_chart.png")

                analysis_result_df = pd.DataFrame() 
                chart_path = None

                if analysis_type == 'single':
                    analysis_result_df, chart_path = get_single_choice_analysis_and_chart(df, column_name, chart_filename)
                elif analysis_type == 'multi':
                    analysis_result_df, chart_path = get_multi_select_analysis_and_chart(df, column_name, chart_filename)
                elif analysis_type == 'rating':
                    analysis_result_df, chart_path = get_rating_analysis_and_chart(df, column_name, chart_filename)
                else:
                    analysis_result_df = pd.DataFrame({'Error': ['Unknown analysis type.']})

                worksheet = writer.book.add_worksheet(safe_sheet_name)
                
                header = [analysis_result_df.index.name or ''] + analysis_result_df.columns.tolist()
                worksheet.write_row('A1', header)

                percentage_format = writer.book.add_format({'num_format': '0.0%'})

                for r_idx, (index_val, row_series) in enumerate(analysis_result_df.iterrows()):
                    current_excel_row = r_idx + 1
                    worksheet.write(current_excel_row, 0, index_val)

                    for c_idx, col_name in enumerate(analysis_result_df.columns):
                        value = row_series[col_name]
                        current_excel_col = c_idx + 1
                        
                        if col_name in ['Percentage', 'Percentage of Respondents'] and pd.notnull(value):
                            worksheet.write(current_excel_row, current_excel_col, value, percentage_format)
                        else:
                            worksheet.write(current_excel_row, current_excel_col, value)

                for col_num, col_name in enumerate(header):
                    if col_name == (analysis_result_df.index.name or ''):
                        max_len = max(len(str(col_name)), analysis_result_df.index.astype(str).map(len).max())
                    elif col_name in analysis_result_df.columns:
                        max_len = max(len(str(col_name)), analysis_result_df[col_name].astype(str).map(len).max())
                    else:
                        max_len = len(str(col_name))
                    worksheet.set_column(col_num, col_num, max_len + 2)

                if chart_path and chart_path.exists():
                    start_row = len(analysis_result_df) + 3 
                    start_col = 0 
                    worksheet.insert_image(start_row, start_col, str(chart_path))
            
            create_pivot_table(df, writer)

        print(f"Analysis report with charts and a flexible pivot table successfully generated at: {OUTPUT_EXCEL_FILE}")
        print(f"All chart images saved in the '{CHARTS_DIR}' directory.")

    except Exception as e:
        print(f"An unexpected error occurred while creating the Excel report: {e}")

if __name__ == "__main__":
    main_analysis_script()