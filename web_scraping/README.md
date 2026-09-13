# Web Scraping

A collection of independent lead-generation / web scraping mini-projects, each targeting a different event, directory, or account list to surface decision-maker contacts for outbound sales. The projects don't share code — each folder is self-contained.

## Projects

| Folder | What it does |
|---|---|
| [`agritec/`](agritec/README.md) | Scrapes the AgriTec Africa exhibitor directory for company contact details (address, website, socials). |
| [`apollo_abm/`](apollo_abm/README.md) | Account-based marketing scraper — finds decision-makers at a curated list of ~350 target companies via the Apollo.io API. Includes a newer domain-first pipeline (`abm_second/`). |
| [`gitex/`](gitex/README.md) | Multi-stage pipeline to find and qualify leads (exhibitor staff + event attendees) for the GITEX Kenya / AI Everything Kenya event, merging Google search, Twitter/X, and LinkedIn post signals into one prioritized lead list. |
| [`tamfi/`](tamfi/README.md) | Google-dork based scraper to find named decision-makers (CEO, COO, etc.) at Tanzanian microfinance institutions and SACCOS. |

## Setup notes

- Each Python file expects the packages it imports (`selenium`, `pandas`, `requests`, `undetected-chromedriver`, `python-dotenv`, `webdriver-manager`) to be installed — there's no single consolidated `requirements.txt` yet since the projects grew independently.
- Selenium-based scripts expect Chrome/Chromium and a matching `chromedriver` to be available locally (see paths in each project's config).
- `apollo_abm/` needs a `.env` file with your own `APOLLO_API_KEY` — copy `apollo_abm/.env.example` to `apollo_abm/.env` and fill in your key. Never commit the real `.env`.
- `gitex/` needs its own `config.py` — copy `gitex/config.example.py` to `gitex/config.py` and adjust paths for your machine. `config.py` is gitignored since it holds machine-specific paths.
- All `data/` folders, CSV outputs, checkpoint/progress files, and browser driver binaries are gitignored — this repo tracks the scraper *code*, not the scraped datasets.

## Security note

An Apollo API key was previously left as an inline comment in `gitex/apollo_scraper.py`. It has been removed from the code, but if that key was ever live, it should be treated as compromised and rotated in the Apollo dashboard.
