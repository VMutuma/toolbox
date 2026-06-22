# Survey Data Analysis Tool

This Python script automates the process of fetching survey data from a Google Sheet, performing various types of analysis (single-choice, multi-select, and rating questions), generating insightful charts, and compiling all results into a comprehensive Excel report, including a flexible pivot table.

## Features

* **Google Sheets Integration**: Securely connects to your survey data stored in Google Sheets using a service account.
* **Automated Data Preprocessing**: Handles date conversions and transforms multi-select string fields into usable list formats.
* **Comprehensive Analysis**: Provides statistical summaries for:
    * Single-choice questions (counts and percentages).
    * Multi-select questions (counts of selections and percentage of respondents selecting each option).
    * Rating scale questions (counts, percentages, and summary statistics like mean, median, mode).
* **Automated Chart Generation**: Creates visually appealing bar charts for each analyzed question, saved as PNG files.
* **Excel Report Generation**: Consolidates raw data, detailed analysis tables, and includes the generated charts directly within an organized Excel workbook.
* **Flexible Pivot Table**: An integrated pivot table in the Excel report allows for dynamic, ad-hoc exploration of the raw data.

## Getting Started

Follow these steps to set up and run the analysis script.

### Prerequisites

* **Python 3.8+**: Ensure you have a compatible Python version installed.
* **Google Service Account**: You need a Google Cloud Platform project with the Google Sheets API enabled and a service account key file (JSON format). This service account must have read access to your Google Sheet.
    * [How to set up a Service Account for Google Sheets API](https://gspread.readthedocs.io/en/latest/oauth2.html#service-account)
* **Google Sheet with Survey Data**: Your survey responses should be in a Google Sheet accessible by the service account.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install pandas gspread matplotlib seaborn python-dotenv xlsxwriter
    ```

### Configuration (`.env` file)

To keep your sensitive information secure and out of the public repository, create a file named `.env` in the root directory of your project (the same directory as `main.py`).

Add the following variables to your `.env` file, replacing the placeholder values with your actual credentials and sheet details:

```dotenv
# Path to your Google Service Account JSON key file
# Example: SERVICE_ACCOUNT_KEY_PATH="/path/to/your/service_account_key.json"
SERVICE_ACCOUNT_KEY_PATH="<path/to/your/service_account_key.json>"

# The full URL of your Google Sheet containing the survey data
SURVEY_SHEET_URL="<your_google_sheet_url>"

# The exact name of the worksheet within your Google Sheet that contains the report data
SURVEY_WORKSHEET_NAME="<your_survey_worksheet_name>"