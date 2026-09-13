# GITEX Kenya Lead Scraper

A 4-stage pipeline to build a prioritized lead list for the GITEX Kenya / AI Everything Kenya event, combining three different signal sources into one deduplicated, scored master list — plus a standalone Apollo enrichment script reused from the broader ABM effort.

## Setup

```bash
cp config.example.py config.py
```

Edit `config.py` for your machine (Chrome/Chromedriver paths, delay tuning). `config.py` is gitignored since it's machine-specific; `config.example.py` is the tracked template.

`browser.py` provides shared Selenium helpers used by every script below: launching a stealth Chrome instance, human-like randomized delays, and automatic CAPTCHA detection (the script pauses and waits for you to solve it manually in the browser window, then resumes).

## Pipeline

### Script 1 — `script1_google_dorker.py`
For each of the event's exhibitors (loaded from `gitex_kenya_exhibitors_only.csv`), runs targeted Google searches (`site:linkedin.com/in "Company" ("CEO" OR "Founder" OR ...)`) to find LinkedIn profiles of likely decision-makers at that company. Extracts a guessed name from the LinkedIn URL slug. Output: `data/out_google_dork.csv`.

### Script 2 — `script2_twitter_scraper.py`
Searches Twitter/X (via public Nitter mirror instances, no login required) for people posting about the event using its keywords/hashtags (`GITEX Kenya`, `#AIEverythingKenya`, etc.), combined with intent words like "attending" or "speaking at". Output: `data/out_twitter.csv`.

### Script 3 — `script3_linkedin_posts.py`
Searches Google for actual LinkedIn *posts* (not just profiles) mentioning the event alongside attendance-intent phrases ("excited to", "will be at", "see you at"...). These are self-identified warm leads — people who've publicly said they're going. Output: `data/out_linkedin_posts.csv`.

### Script 3b — `script3b_enrich_people.py`
Cleans up and enriches the raw leads from scripts 1 and 3:
- Loads exhibitor-staff leads from Script 1's output.
- Extracts individual people from Script 3's post URLs (filtering out company-page slugs via a maintained skip-list).
- For anyone missing a real name/title/company, Googles their LinkedIn slug and parses the result snippet (`Name - Title at Company | LinkedIn`) to fill in the blanks.
- Writes everything to `data/master_leads.csv` with a `source`/`source_detail` column so you always know where a lead came from.

### Script 4 — `script4_merge.py`
A simpler alternative/complement to 3b: merges the three raw CSVs (dork, Twitter, LinkedIn posts) directly, deduplicates by LinkedIn URL → Twitter handle → name+company (in that priority order), and assigns each lead a priority score:
- **HIGH** — exhibitor staff with a LinkedIn URL and name, or a self-identified LinkedIn post with a URL
- **MEDIUM** — Twitter-sourced with a name, or has both LinkedIn URL and name from another source
- **LOW** — everything else

Output: `data/master_leads.csv`, sorted HIGH → MEDIUM → LOW.

### `apollo_scraper.py`
A standalone script (not part of the numbered pipeline) that runs the same account list and vertical-title logic as `apollo_abm/` against Apollo.io directly, taking the API key as a CLI argument rather than from `.env`:
```bash
python apollo_scraper.py --api-key YOUR_API_KEY
```
This predates the `.env`-based `apollo_abm/` project and duplicates its `ACCOUNTS`/`VERTICAL_TITLES` data — worth consolidating with `apollo_abm/apollo_scraper_main.py` at some point since they've since diverged slightly.

## Usage order

```bash
python3 script1_google_dorker.py
python3 script2_twitter_scraper.py
python3 script3_linkedin_posts.py
python3 script3b_enrich_people.py   # or script4_merge.py
```

Every script checkpoints its progress (either to a `_progress.txt` file or by saving the CSV after every item), so any of them can be safely interrupted and re-run without starting over or duplicating work already done.
