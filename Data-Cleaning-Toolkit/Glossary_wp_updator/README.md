# WordPress Glossary Content Expander with Gemini AI

This Python script automates the process of fetching existing glossary terms from a WordPress site, expanding their content using the Google Gemini AI, and then updating those terms back on WordPress via its REST API. It's designed to enrich short glossary definitions into more comprehensive articles.

## Table of Contents

-   [Features](#features)
-   [Prerequisites](#prerequisites)
-   [Setup](#setup)
    -   [Environment Variables (.env)](#environment-variables-env)
    -   [WordPress Configuration](#wordpress-configuration)
-   [Usage](#usage)
-   [Input CSV Format](#input-csv-format)
-   [Output](#output)
-   [Troubleshooting Common Issues](#troubleshooting-common-issues)
    -   [401 Unauthorized Error](#401-unauthorized-error)
    -   [Gemini API Blocking Content](#gemini-api-blocking-content)
    -   [Invalid JSON from Gemini](#invalid-json-from-gemini)
-   [Important Notes](#important-notes)

## Features

* **Fetch Glossary Terms:** Retrieves existing glossary term details (ID, title, content, excerpt) from WordPress using their slugs.
* **AI-Powered Content Expansion:** Utilizes Google Gemini's Generative AI to expand and re-write definitions into detailed, professional, and HTML-formatted content.
* **Dynamic Excerpt Generation:** Gemini also generates a new, concise excerpt based on the expanded content.
* **WordPress Update:** Posts the newly generated content and excerpt back to the corresponding WordPress glossary term.
* **CSV-Driven Process:** Reads a list of glossary term URLs from a CSV file to process in bulk.
* **Logging:** Generates a log file (`glossary_update_log.txt`) detailing successes, failures, and skipped items.

## Prerequisites

Before running this script, ensure you have:

* **Python 3.7+:** Download from [python.org](https://www.python.org/downloads/).
* **Required Python Libraries:**
    * `requests`
    * `python-dotenv`
    * `google-generativeai`
* **A WordPress Website:** With the Glossary custom post type active.
* **WordPress User with Application Password:** An Administrator or Editor role is usually required.
* **Google Gemini API Key:** Obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Setup

1.  **Clone or Download the Script:**
    Save the provided Python script (e.g., `update_glossary.py`) to your local machine.

2.  **Install Python Libraries:**
    Open your terminal or command prompt and run:
    ```bash
    pip install requests python-dotenv google-generativeai
    ```

3.  **Environment Variables (.env):**
    Create a file named `.env` in the **same directory** as your Python script. Populate it with your sensitive API keys and WordPress credentials:

    ```env
    WP_USERNAME="your_wordpress_username"
    WP_APPLICATION_PASSWORD="your_wordpress_application_password"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    Replace the placeholder values with your actual credentials. **Do not share your `.env` file publicly.**

4.  **WordPress Configuration:**

    * **WordPress REST API:** Ensure your WordPress site's REST API is enabled and accessible. It typically is by default.
    * **Application Passwords:**
        * Log in to your WordPress admin dashboard.
        * Navigate to **Users > Profile**.
        * Scroll down to "Application Passwords."
        * Give your new application password a name (e.g., "Glossary Updater") and click "Add New Application Password."
        * **Copy the generated password immediately.** You will only see it once. This is the `WP_APPLICATION_PASSWORD` you need for your `.env` file.
    * **User Permissions:** The WordPress user associated with your Application Password *must* have the necessary capabilities to **edit and publish** custom post types, specifically your `glossary` post type. An Administrator role generally has these, but sometimes custom post types or security plugins apply stricter rules. If you encounter a `401 Unauthorized` or `403 Forbidden` error, this is the primary area to investigate.

5.  **Configure API URLs in Script:**
    Open `update_glossary.py` and set your WordPress API URLs. **Ensure they are correct and point to your site.**

    ```python
    # WordPress API
    WP_API_COLLECTION_URL = "[https://yourdomain.com/wp-json/wp/v2/glossary](https://yourdomain.com/wp-json/wp/v2/glossary)" 
    WP_API_UPDATE_URL_BASE = "[https://yourdomain.com/wp-json/wp/v2/glossary/](https://yourdomain.com/wp-json/wp/v2/glossary/)" 
    ```
    (Replace `https://yourdomain.com/` with your actual WordPress site URL).

## Usage

1.  **Prepare your Input CSV File:** Create a CSV file named `Glossary_Low_Word_Count.csv` (or update `INPUT_CSV_FILE` variable in the script if you use a different name) in the same directory as the script. See [Input CSV Format](#input-csv-format) for details.

2.  **Run the Script:**
    Open your terminal or command prompt, navigate to the directory where you saved the script, and run:
    ```bash
    python update_glossary.py
    ```

The script will begin fetching, expanding, and updating your glossary terms. Progress and errors will be printed to the console and logged to `glossary_update_log.txt`.

## Input CSV Format

The input CSV file (`Glossary_Low_Word_Count.csv` by default) must contain a column named `Url`. This column should list the full URLs of the glossary terms you wish to process.

**Example `Glossary_Low_Word_Count.csv`:**

