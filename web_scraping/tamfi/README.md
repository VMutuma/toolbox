# Tamfi — Tanzania Microfinance Decision-Maker Scraper

Finds named decision-makers (CEO, COO, Head of Credit, Head of Customer Experience, etc.) at Tanzanian microfinance institutions and SACCOS, using Google-dork style searches submitted directly through a real Google search box in a Selenium-controlled browser (rather than Apollo or an API).

## How it works

For each organization × target role combination, it:
1. Submits a query like `"Head of Credit" "K-Finance Limited" Tanzania -job -vacancy -intern` into Google's search box.
2. Waits for results, detecting and pausing on CAPTCHA pages until you solve them manually.
3. Tries several CSS selectors against the results (Google's markup changes often) to find each result's title, link, and snippet.
4. Runs three regex patterns against the combined title+snippet text to extract candidate full names — after a role keyword (`CEO: John Doe`), general capitalized name pairs, or after an honorific (`Mr. John Doe`).
5. Saves matches (organization, role searched, result title/link/snippet, extracted names) to a timestamped CSV and appends to a running `all_contacts_master.csv`.

Progress is checkpointed per organization *and* per role within an organization (`progress.json`), so a run can be stopped and resumed without repeating searches already done — important since this script deliberately runs slowly to avoid getting blocked.

## Scripts

### `scrape_tamfi.py`
The primary version, using `undetected-chromedriver` to reduce the chance of Google flagging the browser as automated. Delays between searches are 8–15s, with a 2-minute break every 10 organizations.

### `scraper_fallback.py`
A slower, plain-Selenium fallback for when the undetected version starts getting blocked anyway. Delays are much longer (20–40s between searches, 5-minute break every 5 organizations), and it periodically restarts the browser entirely during long breaks to further reduce fingerprinting.

## Usage

```bash
python3 scrape_tamfi.py
# or, if that's getting blocked:
python3 scraper_fallback.py
```

Both scripts require manually solving any CAPTCHA that appears (press Enter in the terminal once solved) — there's no automated CAPTCHA-solving.

## Known limitations

- Name extraction is regex-based against search snippets, not a real NLP/NER step — it will produce false positives (any two capitalized words) alongside real names, so the output needs manual review before use.
- Both scripts currently hardcode a short sample `ORGANIZATIONS` list rather than loading the full ~350-organization list from a file.
