#!/usr/bin/env python3
"""
Script 2 — Twitter/X Public Search Scraper
────────────────────────────────────────────
Searches Twitter/X public search (no login) for people
posting about AI Everything Kenya / GITEX Kenya.

Extracts: display name, handle, bio (title + company usually in bio)

Output: data/out_twitter.csv

Usage:
    python3 script2_twitter_scraper.py
"""

import csv
import os
import re
import time
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import OUT_TWITTER, EVENT_KEYWORDS, MASTER_COLUMNS
from browser import make_driver, human_delay, safe_get

# ── Config ────────────────────────────────────────────────────────────────────

# Twitter/X search URLs — no login needed for public search
# nitter.net is a public Twitter mirror, no login, no JS wall
NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.net",
]

SCROLL_PAUSE = 3       # seconds between scrolls
MAX_SCROLLS  = 8       # per query
MAX_RESULTS  = 200     # stop after this many unique profiles


# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_handle(handle: str) -> str:
    return handle.strip().lstrip("@")


def extract_profile_info(card_element) -> dict | None:
    """Extract name, handle, bio from a tweet card element."""
    try:
        # Name
        name_el = card_element.find_element(By.CSS_SELECTOR, ".fullname, .username a, a.username")
        name = name_el.text.strip()

        # Handle
        handle_el = card_element.find_element(By.CSS_SELECTOR, ".username, span.username")
        handle = clean_handle(handle_el.text.strip())

        if not name or not handle:
            return None

        return {
            "full_name":      name,
            "title":          "",
            "company":        "",
            "country":        "",
            "linkedin_url":   "",
            "twitter_handle": f"@{handle}",
            "source":         "twitter_search",
            "notes":          "",
            "sectors":        "",
        }
    except Exception:
        return None


def search_nitter(driver, base_url: str, query: str, seen_handles: set) -> list[dict]:
    """Search a Nitter instance for a query and extract unique profiles."""
    results = []
    encoded = urllib.parse.quote_plus(query)
    url = f"{base_url}/search?q={encoded}&f=tweets"

    print(f"    🔍 {url[:80]}...")
    try:
        safe_get(driver, url)
    except Exception as e:
        print(f"    ⚠️  Failed to load: {e}")
        return results

    # Check if instance is working
    if "nitter" not in driver.page_source.lower() and "tweet" not in driver.page_source.lower():
        print("    ⚠️  Instance not responding, trying next...")
        return results

    for scroll in range(MAX_SCROLLS):
        # Find tweet cards
        cards = driver.find_elements(By.CSS_SELECTOR, ".timeline-item, .tweet-card, article")

        for card in cards:
            try:
                # Get the profile link
                profile_links = card.find_elements(By.CSS_SELECTOR, "a[href*='/']")
                handle = ""
                name = ""

                for link in profile_links:
                    href = link.get_attribute("href") or ""
                    text = link.text.strip()
                    # Nitter profile links look like /username
                    if re.match(r"https?://[^/]+/[A-Za-z0-9_]+$", href):
                        handle = href.rstrip("/").split("/")[-1]
                        break

                # Get display name — usually bold/strong text in card
                name_els = card.find_elements(By.CSS_SELECTOR, ".fullname, strong, b, .name")
                for el in name_els:
                    t = el.text.strip()
                    if t and not t.startswith("@") and len(t) > 1:
                        name = t
                        break

                if not handle or handle in seen_handles:
                    continue
                if handle.lower() in ("search", "login", "signup", "about"):
                    continue

                seen_handles.add(handle)

                # Get tweet text for context note
                tweet_text = ""
                try:
                    tweet_el = card.find_element(By.CSS_SELECTOR, ".tweet-content, .tweet-body, p")
                    tweet_text = tweet_el.text.strip()[:100]
                except Exception:
                    pass

                results.append({
                    "full_name":      name or handle,
                    "title":          "",
                    "company":        "",
                    "country":        "",
                    "linkedin_url":   "",
                    "twitter_handle": f"@{handle}",
                    "source":         "twitter_search",
                    "notes":          f'Posted about event: "{tweet_text}"' if tweet_text else "Found via event keyword search",
                    "sectors":        "",
                })
                print(f"    ✅ @{handle} ({name})")

            except Exception:
                continue

        # Scroll down for more
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE)

        # Check if we hit "Load more" button
        try:
            load_more = driver.find_element(By.CSS_SELECTOR, ".show-more a, .load-more")
            driver.execute_script("arguments[0].click();", load_more)
            human_delay(2, 4)
        except Exception:
            pass  # No load more button — that's fine

    return results


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Load existing results
    existing_rows = []
    if os.path.exists(OUT_TWITTER):
        with open(OUT_TWITTER, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    results = list(existing_rows)
    seen_handles = {r["twitter_handle"].lstrip("@") for r in results if r.get("twitter_handle")}

    print(f"🐦 Twitter/X Scraper — targeting {len(EVENT_KEYWORDS)} keyword sets")
    print(f"   Already found: {len(results)} profiles\n")

    driver = make_driver(headless=False)

    # Find a working Nitter instance first
    working_instance = None
    print("🔎 Finding working Nitter instance...")
    for instance in NITTER_INSTANCES:
        try:
            driver.get(instance)
            human_delay(2, 4)
            if "nitter" in driver.page_source.lower() or "twitter" in driver.title.lower():
                working_instance = instance
                print(f"   ✅ Using: {instance}\n")
                break
        except Exception:
            continue

    if not working_instance:
        print("❌ No Nitter instance available. Falling back to Twitter public search...")
        working_instance = "https://twitter.com"

    try:
        for keyword in EVENT_KEYWORDS:
            print(f"\n📌 Keyword: '{keyword}'")

            # Search queries
            queries = [
                keyword,
                f"{keyword} attending",
                f"{keyword} excited",
                f"{keyword} speaking",
                f"{keyword} exhibiting",
                f"{keyword} Nairobi",
            ]

            for query in queries:
                if len(results) >= MAX_RESULTS:
                    print(f"\n🎯 Hit max results ({MAX_RESULTS}). Stopping.")
                    break

                found = search_nitter(driver, working_instance, query, seen_handles)
                results.extend(found)

                # Save after every query
                with open(OUT_TWITTER, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=list(MASTER_COLUMNS))
                    writer.writeheader()
                    writer.writerows(results)

                human_delay()

    except KeyboardInterrupt:
        print("\n⏹️  Interrupted. Progress saved.")
    finally:
        driver.quit()

    print(f"\n✅ Script 2 done. {len(results)} Twitter profiles saved to:")
    print(f"   {OUT_TWITTER}")


if __name__ == "__main__":
    main()