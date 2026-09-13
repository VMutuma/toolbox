# AgriTec Africa Exhibitor Scraper

Scrapes the [AgriTec Africa](https://www.agritecafrica.com/directory/) exhibitor directory using Selenium and exports company contact details to CSV.

## Scripts

### `scrape_agritec_selenium.py`
The initial version. It:
1. Loads the directory page and finds every exhibitor profile link (`/participate/...`), trying several CSS selectors since the site's markup isn't consistent.
2. Visits each exhibitor's page and extracts: company name, a single address, website, Facebook/Instagram/LinkedIn links, and a description.
3. Saves everything to `agritec_exhibitors_full.csv`.

This version treats "address" as a single field — which turned out to be a problem, since each exhibitor page actually lists *up to three* different addresses (venue, company, and event organizer), and the script had no way to tell them apart.

### `scrape_correct_addresses.py`
A corrected follow-up. Instead of grabbing the first address-like element it finds, it collects every map-marker icon list item on the page in order and assigns them positionally:
1. First address → `venue_address`
2. Second address → `company_address` (the one that actually matters for outreach)
3. Third address → `organizer_address`

It also captures the same social/website fields and a truncated (500-char) description, saving results to `agritec_company_addresses.csv`.

## Usage

```bash
python3 scrape_correct_addresses.py
```

Both scripts run headless Chrome by default. No API keys or credentials are required — this is a pure public-page scrape.

## Known limitations

- Address extraction relies on icon class names (`fa-map-marker-alt`) and item order on the page — if AgriTec changes their site template, this will silently return wrong or empty addresses.
- No retry/resume logic — if the browser crashes partway through, you restart from the beginning.
