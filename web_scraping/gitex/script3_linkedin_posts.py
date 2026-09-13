#!/usr/bin/env python3
"""
Script 3 — LinkedIn Posts via Google Dork
───────────────────────────────────────────
Searches Google for LinkedIn posts about the event.
People who post "I'll be at AI Everything Kenya" are
self-identified warm leads — they've already committed to attend.

Extracts: Name, LinkedIn profile URL, snippet (post preview)

Output: data/out_linkedin_posts.csv

Usage:
    python3 script3_linkedin_posts.py
"""

import csv
import os
import re
import urllib.parse
from selenium.webdriver.common.by import By
from config import (
    OUT_LI_POSTS, EVENT_KEYWORDS, MASTER_COLUMNS,
    DELAY_MIN, DELAY_MAX
)
from browser import make_driver, human_delay, safe_get, wait_for_captcha

# ── Config ────────────────────────────────────────────────────────────────────

MAX_PAGES_PER_QUERY = 3   # Google pages to paginate through

INTENT_PHRASES = [
    "attending", "excited to", "see you at", "will be at",
    "join us", "we will be", "speaking at", "exhibiting at",
    "looking forward", "can't wait", "meet me at",
    "happy to", "proud to", "thrilled to",
]

PROGRESS_FILE = OUT_LI_POSTS.replace(".csv", "_progress.txt")


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_progress() -> set:
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE) as f:
        return set(line.strip() for line in f if line.strip())


def save_progress(query: str):
    with open(PROGRESS_FILE, "a") as f:
        f.write(query + "\n")


def slug_to_name(url: str) -> str:
    """Extract name from LinkedIn /in/slug."""
    if "/in/" not in url:
        return ""
    slug = url.rstrip("/").split("/in/")[-1].split("?")[0]
    slug = re.sub(r"-?\d+$", "", slug)
    parts = [p for p in slug.split("-") if p]
    if len(parts) < 2:
        return ""
    return " ".join(p.capitalize() for p in parts[:3])


def extract_snippet(result_element) -> str:
    """Get the text snippet from a Google search result."""
    try:
        snippet_el = result_element.find_element(
            By.CSS_SELECTOR, ".VwiC3b, .s3v9rd, span.aCOpRe, .st"
        )
        return snippet_el.text.strip()[:200]
    except Exception:
        return ""


def build_queries() -> list[str]:
    """Build all LinkedIn post dork queries."""
    queries = []

    for keyword in EVENT_KEYWORDS:
        # Posts mentioning the event
        queries.append(f'site:linkedin.com/posts "{keyword}"')
        queries.append(f'site:linkedin.com/feed/update "{keyword}"')

        # With intent phrases
        for phrase in INTENT_PHRASES[:5]:  # top 5 to avoid too many queries
            queries.append(f'site:linkedin.com "{keyword}" "{phrase}"')

    # Activity pages (another LinkedIn URL pattern for posts)
    queries.append('site:linkedin.com "AI Everything Kenya" 2026')
    queries.append('site:linkedin.com "GITEX Kenya" "May 2026"')
    queries.append('site:linkedin.com "KICC" "AI Everything" 2026')

    # Deduplicate
    return list(dict.fromkeys(queries))


def search_google_for_posts(driver, query: str, seen_urls: set) -> list[dict]:
    """Search Google and extract LinkedIn profile/post URLs."""
    found = []

    for page in range(MAX_PAGES_PER_QUERY):
        start = page * 10
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num=10&start={start}&hl=en"

        safe_get(driver, url)
        human_delay()

        # Check for no results
        if "did not match any documents" in driver.page_source.lower():
            break

        # Find all search result containers
        results = driver.find_elements(By.CSS_SELECTOR, "div.g, div[data-sokoban-container]")

        if not results:
            # Fallback: grab all LinkedIn links directly
            results = [driver]

        page_had_results = False

        for result in results:
            try:
                links = result.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href") or ""

                    # We want /in/ profiles OR /posts/ pages
                    if "linkedin.com/in/" in href or "linkedin.com/posts/" in href:
                        # Clean URL
                        clean = href.split("?")[0].rstrip("/")

                        if clean in seen_urls:
                            continue
                        seen_urls.add(clean)

                        # Extract name
                        if "/in/" in clean:
                            name = slug_to_name(clean)
                            profile_url = clean
                        else:
                            # It's a post URL — extract the profile from it if possible
                            name = ""
                            profile_url = ""

                        # Get snippet for context
                        snippet = extract_snippet(result) if result != driver else ""

                        found.append({
                            "full_name":      name,
                            "title":          "",
                            "company":        "",
                            "country":        "",
                            "linkedin_url":   profile_url or clean,
                            "twitter_handle": "",
                            "source":         "linkedin_post_google",
                            "notes":          snippet or f"Posted about: {query[:60]}",
                            "sectors":        "",
                        })
                        page_had_results = True
                        if name:
                            print(f"    ✅ {name} → {clean[:60]}")
                        else:
                            print(f"    ✅ Post found → {clean[:60]}")

            except Exception:
                continue

        if not page_had_results:
            break  # No point paginating further

        human_delay()  # between pages

    return found


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    queries = build_queries()
    done = load_progress()

    # Load existing
    existing_rows = []
    if os.path.exists(OUT_LI_POSTS):
        with open(OUT_LI_POSTS, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))

    results = list(existing_rows)
    seen_urls = {r["linkedin_url"] for r in results if r.get("linkedin_url")}

    remaining = [q for q in queries if q not in done]
    print(f"🔗 LinkedIn Posts via Google")
    print(f"   {len(queries)} queries total, {len(done)} done, {len(remaining)} remaining")
    print(f"   Already found: {len(results)} leads\n")

    driver = make_driver(headless=False)

    try:
        for idx, query in enumerate(remaining):
            print(f"\n[{idx+1}/{len(remaining)}] {query[:70]}...")

            found = search_google_for_posts(driver, query, seen_urls)
            results.extend(found)

            save_progress(query)

            # Save after every query
            with open(OUT_LI_POSTS, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(MASTER_COLUMNS))
                writer.writeheader()
                writer.writerows(results)

            print(f"   💾 Saved. Running total: {len(results)} leads")
            human_delay(DELAY_MIN + 1, DELAY_MAX + 2)

    except KeyboardInterrupt:
        print("\n⏹️  Interrupted. Progress saved — re-run to continue.")
    finally:
        driver.quit()

    print(f"\n✅ Script 3 done. {len(results)} leads saved to:")
    print(f"   {OUT_LI_POSTS}")


if __name__ == "__main__":
    main()