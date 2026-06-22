
# Glossary Scraper

## Overview
This project is a Python-based scraper that extracts glossary terms, definitions, and detailed explanations from websites' documentation. The scraper retrieves the glossary from the given page, fetches the linked term pages, and saves the information in multiple formats: CSV, JSON, and Word document.

## Features
- Scrape glossary terms, definitions, and links from the Twilio glossary page.
- Follow links to individual term pages and extract the header and paragraphs.
- Output results in three formats:
  - CSV file
  - JSON file
  - Word document

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/twilio-glossary-scraper.git
   cd glossary-scraper
   ```

2. Set up a Python virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper:

1. Open `main.py` and modify the URL (if you want to scrape a different page).
2. Run the scraper:

   ```bash
   python main.py
   ```

The scraper will fetch the glossary, follow links, extract the required data, and save the results in the CSV format, JSON format and Word document.

## Configuration

You can configure the following in the `main.py` file:
- `url`: The URL of the glossary page to scrape.
- `headers`: Custom headers for the HTTP requests (default headers are set for Twilio).

## Logging

Logs are stored in the `scraper.log` file. Make sure to keep this file in the `.gitignore` to avoid uploading it to version control systems.

## Notes

- The scraper extracts the term name, definition, and follows the links to get the full details.
- You can modify the scraper in the future to work with other glossary pages by adjusting the parsing logic.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
