# Apollo ABM Scraper

Account-based marketing (ABM) lead generation against a curated list of ~350 target companies across 8 verticals (Healthcare, Banking & Insurance, Betting & Gaming, EV & Clean Energy, Agri & Food, Logistics & Cargo, ISPs & Telecom, Other), using the [Apollo.io](https://apollo.io) API to find named decision-makers at each account.

There are two generations of this scraper in this folder, using different strategies to deal with the same core problem: **Apollo's organization-name search often fails to match a company by its common name.**

## Setup

```bash
cp .env.example .env
# then edit .env and add your real Apollo API key
```

`abm_config.py` loads `APOLLO_API_KEY` from `.env` via `python-dotenv`. The `.env` file itself is gitignored — never commit your real key.

## Approach 1 — Name-search first (`apollo_scraper_main.py`, `abm_browser.py`, `abm_config.py`)

The original approach:
1. For each target company, try Apollo's organization search (`q_organization_name`) using the exact name, then a series of fallback variations (stripped suffixes like "Bank"/"Hospital", first word only, appended country codes, acronyms) until one returns a match.
2. Once an organization ID is found, search Apollo for people at that org matching a vertical-specific list of target titles (e.g. Banking & Insurance → "Head of Digital", "CTO", "COO"...).
3. Progress is checkpointed to a text file (one company per line) so a crashed/interrupted run can resume without re-querying companies already processed.
4. Results are deduplicated by email and written to timestamped CSVs (`apollo_leads_*.csv` for hits, `apollo_not_found_*.csv` for companies Apollo couldn't match at all).

`abm_browser.py` provides Selenium helper functions (stealth browser setup, human-like delays, CAPTCHA detection/waiting) that are available to this pipeline but not directly used by the current name-search flow — they're there for browser-based fallback searches if needed.

**Weakness:** name-based search on Apollo is unreliable for smaller or regionally-named companies — many accounts end up in "not found" even though they exist in Apollo's database under a different organization record.

## Approach 2 — Domain-first (`abm_second/`)

A more reliable two-step pipeline that sidesteps name-matching entirely by resolving each company to its actual website domain first:

### Step 1 — `1_crawl_domains.py`
Uses Selenium to Google each company name (with a country hint appended) and extracts the most likely official domain from the search results, skipping known non-company domains (LinkedIn, Crunchbase, ZoomInfo, etc.). Checkpoints progress to `domains_checkpoint.csv` so it can resume, and writes a clean `domains_final.csv` at the end.

### Step 2 — `2_apollo_enrich.py`
Given the domain list, this runs Apollo's two-step enrichment flow:
- **Step A (free):** `mixed_people/api_search` — searches Apollo by `q_organization_domains` + a target title/seniority filter, discovering people without spending credits. Results go to `apollo_people_raw.csv`.
- **Step B (paid):** `people/bulk_match` — enriches up to 10 people per call with `reveal_personal_emails=true` to get verified emails. Results go to `apollo_people_final.csv`.

Both steps checkpoint independently (`ckpt_search.json`, `ckpt_enrich.json`) so you only pay for enrichment once per person, even across multiple runs.

## Usage

```bash
# Approach 1
python3 apollo_scraper_main.py

# Approach 2
cd abm_second
python3 1_crawl_domains.py     # produces domains_final.csv
python3 2_apollo_enrich.py     # consumes domains_final.csv, produces apollo_people_final.csv
```

## Notes

- `COMPANY_NAME_MAPPINGS` in `abm_config.py` lets you manually map a company's "known" name to whatever name actually matches in Apollo, loaded from `data/company_name_mappings.csv` if present.
- All output CSVs, checkpoints, and progress files live under `data/`, which is gitignored.
