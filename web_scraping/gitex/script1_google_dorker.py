#!/usr/bin/env python3
"""
Script 1 — Google Dorker
─────────────────────────
For each of the 30 exhibitors, searches Google for LinkedIn
profiles of decision-makers using targeted dork queries.

Output: data/out_google_dork.csv
    columns: full_name, title, company, country, linkedin_url, source, sectors

Usage:
    python3 script1_google_dorker.py
"""

import csv
import os
import re
import time
import urllib.parse
from selenium.webdriver.common.by import By
from config import (
    EXHIBITORS_CSV, OUT_GOOGLE_DORK, SEARCH_TITLES,
    DELAY_MIN, DELAY_MAX, MASTER_COLUMNS
)
from browser import make_driver, human_delay, safe_get, wait_for_captcha

# ── Helpers ───────────────────────────────────────────────────────────────────

PROGRESS_FILE = OUT_GOOGLE_DORK.replace(".csv", "_progress.txt")


def load_progress() -> set:
    """Return set of company names already processed."""
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE) as f:
        return set(line.strip() for line in f if line.strip())


def save_progress(company: str):
    with open(PROGRESS_FILE, "a") as f:
        f.write(company + "\n")


def clean_company(name: str) -> str:
    """Strip legal suffixes for cleaner search queries."""
    for suffix in [
        " Ltd", " LLC", " FZCO", " FZE", " PTE. LTD",
        " Limited", " Pty", " Inc", " Corp", " Co.",
    ]:
        name = name.replace(suffix, "")
    return name.strip()


def slug_to_name(url: str) -> str:
    """Extract a human name from a LinkedIn /in/slug."""
    slug = url.rstrip("/").split("/in/")[-1].split("?")[0]
    slug = re.sub(r"-?\d+$", "", slug)   # strip trailing ID
    parts = [p for p in slug.split("-") if p]
    if len(parts) < 2:
        return ""
    return " ".join(p.capitalize() for p in parts[:3])  # max 3 parts


def build_queries(company: str, country: str) -> list[str]:
    """Build Google dork queries for this company."""
    short = clean_company(company)
    title_block = " OR ".join(f'"{t}"' for t in SEARCH_TITLES[:8])  # keep query short

    queries = [
        # Primary: LinkedIn profile with decision-maker title
        f'site:linkedin.com/in "{short}" ({title_block})',
        # Secondary: LinkedIn profile with country
        f'site:linkedin.com/in "{short}" "{country}"' if country else None,
        # Event-specific: people announcing attendance
        f'site:linkedin.com "{short}" "AI Everything Kenya" OR "GITEX Kenya"',
    ]
    return [q for q in queries if q]


def google_search_links(driver, query: str) -> list[str]:
    """Run a Google search and return all linkedin.com/in links found."""
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}&num=10&hl=en"

    safe_get(driver, url)
    human_delay()

    # Check for no results
    page = driver.page_source
    if "did not match any documents" in page.lower():
        return []

    # Extract all links
    links = []
    anchors = driver.find_elements(By.TAG_NAME, "a")
    for a in anchors:
        try:
            href = a.get_attribute("href") or ""
            # Google wraps real URLs — unwrap them
            if "linkedin.com/in/" in href:
                # Clean tracking params
                href = href.split("?")[0]
                if href not in links:
                    links.append(href)
        except Exception:
            continue
    return links


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Load exhibitors
    with open(EXHIBITORS_CSV, newline="", encoding="utf-8") as f:
        exhibitors = list(csv.DictReader(f))

    done = load_progress()
    print(f"📋 {len(exhibitors)} exhibitors loaded. {len(done)} already processed.\n")

    # Load existing results to append
    existing_rows = []
    if os.path.exists(OUT_GOOGLE_DORK):
        with open(OUT_GOOGLE_DORK, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    results = list(existing_rows)
    seen_urls = {r["linkedin_url"] for r in results if r.get("linkedin_url")}

    driver = make_driver(headless=False)
    print("🌐 Browser launched. Starting search...\n")

    try:
        for idx, row in enumerate(exhibitors):
            company = row["company"].strip()
            country = row.get("country", "").strip()
            sectors = row.get("sectors", "").strip()

            if company in done:
                print(f"[{idx+1}/{len(exhibitors)}] ⏭️  Skipping {company} (already done)")
                continue

            print(f"[{idx+1}/{len(exhibitors)}] 🔍 {company}")
            queries = build_queries(company, country)
            found_this_company = 0

            for q in queries:
                print(f"    Query: {q[:80]}...")
                links = google_search_links(driver, q)

                for url in links:
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)
                    name = slug_to_name(url)
                    if not name:
                        continue

                    results.append({
                        "full_name":     name,
                        "title":         "",   # Apollo will fill
                        "company":       company,
                        "country":       country,
                        "linkedin_url":  url,
                        "twitter_handle": "",
                        "source":        "google_dork",
                        "notes":         f"Exhibitor at GITEX Kenya 2026",
                        "sectors":       sectors,
                    })
                    found_this_company += 1
                    print(f"    ✅ {name} → {url}")

                human_delay()  # pause between queries

            if found_this_company == 0:
                print(f"    ⚠️  No profiles found")

            save_progress(company)

            # Save after every company (in case of crash)
            with open(OUT_GOOGLE_DORK, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(MASTER_COLUMNS))
                writer.writeheader()
                writer.writerows(results)

            print(f"    💾 Saved. Running total: {len(results)} leads\n")
            human_delay(DELAY_MIN + 2, DELAY_MAX + 3)  # extra pause between companies

    except KeyboardInterrupt:
        print("\n⏹️  Interrupted. Progress saved — re-run to continue.")
    finally:
        driver.quit()

    print(f"\n✅ Script 1 done. {len(results)} LinkedIn profiles saved to:")
    print(f"   {OUT_GOOGLE_DORK}")


if __name__ == "__main__":
    main()