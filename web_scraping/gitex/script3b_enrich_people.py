#!/usr/bin/env python3
"""
script_enrich_and_merge.py
───────────────────────────
1. Loads out_google_dork.csv (exhibitor staff — source: google_dork)
2. Extracts individual LinkedIn /in/ URLs from out_linkedin_posts.csv
   (event posters — source: linkedin_post)
3. For every unique LinkedIn URL, Googles the slug to get:
      - Real full name
      - Title
      - Company
4. Outputs one clean master CSV with all columns including source

Output columns:
    full_name | title | company | country | linkedin_url |
    source | source_detail | sectors | notes

Usage:
    python3 script_enrich_and_merge.py
"""

import csv
import os
import re
import time
import urllib.parse
import random
from selenium.webdriver.common.by import By
from config import (
    OUT_GOOGLE_DORK, OUT_LI_POSTS, DATA_DIR,
    DELAY_MIN, DELAY_MAX
)
from browser import make_driver, human_delay, safe_get

# ── Output files ──────────────────────────────────────────────────────────────
OUTPUT       = os.path.join(DATA_DIR, "master_leads.csv")
PROGRESS_FILE= os.path.join(DATA_DIR, "enrich_progress.txt")

# ── Output columns ────────────────────────────────────────────────────────────
COLUMNS = [
    "full_name",
    "title",
    "company",
    "country",
    "linkedin_url",
    "source",           # "google_dork" or "linkedin_post"
    "source_detail",    # e.g. "Exhibitor: Asprime Software Ltd" or "Posted about AI Everything Kenya"
    "sectors",
    "notes",
]

# ── Company page slugs to skip ────────────────────────────────────────────────
SKIP_SLUGS = {
    "aieverythingkenya", "startupkenya", "omnicomm", "cloudmon",
    "top-africa-news-media", "allconfsbot", "mavinagency1",
    "motoseenafrica", "nabzn", "kaoun", "gitexkenya",
    "pny-technologies-europe", "zoho-africa", "tally-solutions-africa",
    "computech-limited", "redingtonafrica", "mart-networks-group",
    "tlminternational", "red-dot-distribution-ltd", "seceon",
    "fintech-newsbyte", "womeninai", "moringa-school", "qhalahq",
    "anganilimited", "a-a-collective", "dtonesolution", "awarri",
    "open-innovation-ai", "indatacore", "gitexafrica", "gitexeurope",
    "gitexasia", "compulynx", "tech-first-gulf", "socradar",
    "id-vision-uae", "joat-kenya-jack-urban-services-ltd",
    "associationofwomeninenergyandextractivesinkenyaaweik",
    "azubi-africa", "creware-technologies-pvt-ltd", "sisgain",
    "peoplelinkcompany", "droomdroom", "digifeat", "wmsspl",
    "rwanda-gbs-growth-inititative", "catalystsocial", "rosethiga",
    "arden-bouet", "imranchaudhrey", "jaspergrosskurth",
    "africa-sustainability-matters", "namibiannews", "smooth-professional",
    "ultra-momentum-mk", "sustainabilitymagazine", "nextplay-media-a25670324",
    "rebecca-murimi", "trixie-lohmirmand", "maherdara",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_progress() -> set:
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE) as f:
        return set(line.strip() for line in f if line.strip())

def save_progress(url: str):
    with open(PROGRESS_FILE, "a") as f:
        f.write(url.strip().rstrip("/").lower() + "\n")

def clean_linkedin_url(url: str) -> str:
    """Strip tracking fragments and trailing slashes."""
    url = url.split("#")[0].split("?")[0].rstrip("/")
    return url

def slug_from_in_url(url: str) -> str | None:
    """Extract slug from linkedin.com/in/SLUG"""
    if "/in/" not in url:
        return None
    slug = url.split("/in/")[-1].rstrip("/").split("/")[0]
    return slug if slug else None

def slug_from_post_url(url: str) -> str | None:
    """Extract person slug from linkedin.com/posts/SLUG_..."""
    if "/posts/" not in url:
        return None
    after = url.split("/posts/")[-1]
    slug = after.split("_")[0].rstrip("/")
    return slug if slug else None

def is_company_slug(slug: str) -> bool:
    """Skip known company slugs and single-word slugs with no numbers."""
    if slug.lower() in SKIP_SLUGS:
        return True
    # Single word, no numbers = likely a company
    parts = slug.split("-")
    word_parts = [p for p in parts if not re.match(r'^[0-9a-f]+$', p, re.I)]
    if len(word_parts) <= 1:
        return True
    return False

def clean_name(name: str) -> str:
    """Remove URL artifacts and hex suffixes from extracted names."""
    # Remove anything after # 
    name = name.split("#")[0].strip()
    # Remove trailing hex-like segments (e.g. "A59451119", "B49456124")
    name = re.sub(r'\s+[A-Fa-f0-9]{6,}$', '', name).strip()
    # Remove trailing single letters that came from hex (e.g. "Sandeep Bhatt A")
    name = re.sub(r'\s+[A-F]$', '', name).strip()
    # Remove URL encoding artifacts
    name = urllib.parse.unquote(name)
    # Capitalize properly
    parts = name.split()
    name = " ".join(p.capitalize() for p in parts if p)
    return name

def google_profile(driver, linkedin_url: str) -> dict:
    """
    Google a LinkedIn /in/ URL to get real name, title, company.
    Parses Google h3: "Firstname Lastname - Title at Company | LinkedIn"
    """
    slug = slug_from_in_url(linkedin_url) or linkedin_url.split("linkedin.com")[-1].strip("/")
    query = f'site:linkedin.com/in "{slug}"'
    encoded = urllib.parse.quote_plus(query)
    search_url = f"https://www.google.com/search?q={encoded}&num=3&hl=en"

    safe_get(driver, search_url)
    human_delay()

    result = {"full_name": "", "title": "", "company": ""}

    try:
        h3_els = driver.find_elements(By.CSS_SELECTOR, "h3")
        for el in h3_els:
            text = el.text.strip()
            if not text or "linkedin" not in text.lower():
                continue

            # Remove "| LinkedIn" or "- LinkedIn" suffix
            text = re.sub(r'\s*[|\-–]\s*LinkedIn\s*$', '', text, flags=re.IGNORECASE).strip()

            # Split on " - " → ["John Doe", "Head of Sales at Acme"]
            dash_parts = re.split(r'\s+[-–]\s+', text, maxsplit=1)
            name_part = dash_parts[0].strip()
            rest_part = dash_parts[1].strip() if len(dash_parts) > 1 else ""

            # Validate name
            name_words = name_part.split()
            if len(name_words) < 2:
                continue
            # Skip if starts with a title word
            skip_words = {"head", "director", "manager", "ceo", "cto", "vp",
                         "founder", "experience", "view", "join", "linkedin"}
            if name_words[0].lower() in skip_words:
                continue
            # Must not be all numbers
            if all(w.isdigit() for w in name_words):
                continue

            result["full_name"] = name_part

            # Parse "Title at Company"
            if rest_part:
                at_match = re.split(r'\s+at\s+', rest_part, maxsplit=1, flags=re.IGNORECASE)
                if len(at_match) == 2:
                    result["title"]   = at_match[0].strip()
                    result["company"] = at_match[1].strip()
                else:
                    result["title"] = rest_part

            break

    except Exception:
        pass

    return result

# ── Load leads ────────────────────────────────────────────────────────────────

def load_google_dork_leads() -> list[dict]:
    """Load exhibitor staff from Script 1."""
    if not os.path.exists(OUT_GOOGLE_DORK):
        print("   ⚠️  out_google_dork.csv not found")
        return []

    leads = []
    with open(OUT_GOOGLE_DORK, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url = clean_linkedin_url(row.get("linkedin_url", ""))
            if not url or "/in/" not in url:
                continue
            # Skip anchor/fragment URLs (duplicates)
            if "#" in row.get("linkedin_url", ""):
                continue

            leads.append({
                "full_name":     clean_name(row.get("full_name", "")),
                "title":         "",
                "company":       row.get("company", "").strip(),
                "country":       row.get("country", "").strip(),
                "linkedin_url":  url,
                "source":        "google_dork",
                "source_detail": f"Exhibitor: {row.get('company', '').strip()}",
                "sectors":       row.get("sectors", "").strip(),
                "notes":         "Staff at GITEX Kenya 2026 exhibitor",
                "_needs_enrich": not row.get("title", "").strip(),
            })
    print(f"   ✅ google_dork: {len(leads)} leads loaded")
    return leads


def load_linkedin_post_leads() -> list[dict]:
    """Extract individual people from LinkedIn post URLs in Script 3 output."""
    if not os.path.exists(OUT_LI_POSTS):
        print("   ⚠️  out_linkedin_posts.csv not found")
        return []

    leads = []
    seen_slugs = set()

    with open(OUT_LI_POSTS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url = row.get("linkedin_url", "").strip()
            if not url:
                continue

            # Case 1: Already a /in/ profile URL
            if "/in/" in url:
                clean_url = clean_linkedin_url(url)
                slug = slug_from_in_url(clean_url)
                if not slug or is_company_slug(slug):
                    continue
                if slug in seen_slugs:
                    continue
                seen_slugs.add(slug)

                leads.append({
                    "full_name":     clean_name(row.get("full_name", "")),
                    "title":         "",
                    "company":       "",
                    "country":       "",
                    "linkedin_url":  clean_url,
                    "source":        "linkedin_post",
                    "source_detail": "Self-identified: posted about AI Everything Kenya",
                    "sectors":       "",
                    "notes":         row.get("notes", "").strip(),
                    "_needs_enrich": True,
                })

            # Case 2: Post URL — extract person slug
            elif "/posts/" in url:
                slug = slug_from_post_url(url)
                if not slug or is_company_slug(slug):
                    continue
                if slug in seen_slugs:
                    continue
                seen_slugs.add(slug)

                profile_url = f"https://www.linkedin.com/in/{slug}"
                leads.append({
                    "full_name":     "",
                    "title":         "",
                    "company":       "",
                    "country":       "",
                    "linkedin_url":  profile_url,
                    "source":        "linkedin_post",
                    "source_detail": "Self-identified: posted about AI Everything Kenya",
                    "sectors":       "",
                    "notes":         row.get("notes", "").strip(),
                    "_needs_enrich": True,
                })

    print(f"   ✅ linkedin_post: {len(leads)} individual leads extracted")
    return leads

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("📋 Loading all leads...\n")

    dork_leads = load_google_dork_leads()
    post_leads = load_linkedin_post_leads()

    # Merge and deduplicate by LinkedIn URL
    seen_urls = {}
    all_leads = []

    for lead in dork_leads + post_leads:
        url = lead["linkedin_url"].lower().rstrip("/")
        if url not in seen_urls:
            seen_urls[url] = True
            all_leads.append(lead)

    print(f"\n   Total unique leads: {len(all_leads)}")

    # Load progress
    done = load_progress()

    # Load existing enriched results
    existing = {}
    if os.path.exists(OUTPUT):
        with open(OUTPUT, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                url = row.get("linkedin_url", "").lower().rstrip("/")
                if url:
                    existing[url] = row
        print(f"   Already enriched: {len(existing)}")

    # Split into needs enrichment vs already done
    to_enrich = []
    ready     = []

    for lead in all_leads:
        url = lead["linkedin_url"].lower().rstrip("/")
        if url in existing:
            ready.append(existing[url])
        elif url in done:
            # Was processed but no result saved — add with what we have
            ready.append(lead)
        elif lead.get("_needs_enrich"):
            to_enrich.append(lead)
        else:
            ready.append(lead)

    print(f"   Need Google enrichment: {len(to_enrich)}")
    print(f"   Already complete:       {len(ready)}\n")

    results = list(ready)

    if to_enrich:
        driver = make_driver(headless=False)
        print("🌐 Browser open. Enriching leads via Google...\n")

        try:
            for idx, lead in enumerate(to_enrich):
                url   = lead["linkedin_url"]
                clean = url.lower().rstrip("/")

                print(f"[{idx+1}/{len(to_enrich)}] {url[:65]}")

                enriched = google_profile(driver, url)

                # Use Google result if better than slug guess
                final_name    = enriched["full_name"] or lead.get("full_name", "")
                final_title   = enriched["title"]     or lead.get("title", "")
                final_company = enriched["company"]   or lead.get("company", "")

                # Clean name
                final_name = clean_name(final_name)

                lead["full_name"] = final_name
                lead["title"]     = final_title
                if final_company and not lead.get("company"):
                    lead["company"] = final_company

                status = "✅" if final_name else "⚠️ "
                print(f"    {status} {final_name or 'No name'} | {final_title or '-'} | {lead.get('company') or '-'}")

                results.append(lead)
                save_progress(url)

                # Save after every lead
                _write_output(results)

                human_delay(DELAY_MIN, DELAY_MAX)

        except KeyboardInterrupt:
            print("\n⏹️  Interrupted. Progress saved — re-run to continue.")
        finally:
            driver.quit()

    # Final save
    _write_output(results)

    # Summary
    by_source = {}
    for r in results:
        src = r.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1

    print(f"\n{'='*55}")
    print(f"✅  MASTER FILE: {OUTPUT}")
    print(f"{'='*55}")
    print(f"   📊 Total leads:      {len(results)}")
    for src, count in sorted(by_source.items()):
        label = "Exhibitor staff (Google Dork)" if src == "google_dork" else "Event posters (LinkedIn Posts)"
        print(f"   └─ {label}: {count}")
    print(f"\n🚀 Ready for Apollo email enrichment!")


def _write_output(rows: list[dict]):
    """Write results to master CSV."""
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()