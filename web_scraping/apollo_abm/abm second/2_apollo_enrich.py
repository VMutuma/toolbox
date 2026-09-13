"""
Step 2: Apollo enrichment — discover people by domain, then enrich for emails.

Two-step flow (per Apollo docs):
  Step A — mixed_people/api_search  : find people by domain + title filters.
            FREE — does not consume credits. Returns Apollo IDs + LinkedIn URLs.
  Step B — people/bulk_match        : enrich up to 10 people per call.
            COSTS CREDITS. Returns verified work emails (and optionally phones).

Run after 1_crawl_domains.py has produced domains_final.csv.

Usage:
    export APOLLO_API_KEY="your_key_here"
    python 2_apollo_enrich.py
"""

import csv
import json
import os
import time
from pathlib import Path

import requests

# ── CONFIG ───────────────────────────────────────────────────────────────────
APOLLO_API_KEY    = os.getenv("APOLLO_API_KEY", "YOUR_API_KEY_HERE")
DOMAINS_FILE      = "domains_final.csv"

PEOPLE_RAW_FILE   = "apollo_people_raw.csv"     # Step A output (no emails yet)
PEOPLE_FINAL_FILE = "apollo_people_final.csv"   # Step B output (with emails)

CHECKPOINT_SEARCH  = "ckpt_search.json"          # which domains are searched
CHECKPOINT_ENRICH  = "ckpt_enrich.json"          # which apollo IDs are enriched

# Search filters — edit titles/seniorities to match your ICP
TARGET_TITLES = [
    "CEO", "Chief Executive Officer",
    "CTO", "Chief Technology Officer",
    "CFO", "Chief Financial Officer",
    "COO", "Chief Operating Officer",
    "Managing Director", "General Manager",
    "Head of IT", "IT Manager", "IT Director",
    "Head of Operations", "Operations Manager",
    "Head of Finance", "Finance Manager", "Finance Director",
    "Procurement Manager", "Head of Procurement",
    "HR Manager", "Head of HR", "HR Director",
    "Director", "VP", "Vice President",
]
TARGET_SENIORITIES = ["c_suite", "vp", "director", "manager", "head"]

PAGE_SIZE        = 100    # max per page for search endpoint
MAX_SEARCH_PAGES = 5      # up to 500 people per domain
ENRICH_BATCH     = 10     # bulk_match accepts max 10 per call

# Apollo endpoints
SEARCH_URL  = "https://api.apollo.io/api/v1/mixed_people/api_search"
ENRICH_URL  = "https://api.apollo.io/api/v1/people/bulk_match"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": APOLLO_API_KEY,
}

# ── GENERIC HELPERS ──────────────────────────────────────────────────────────

def load_domains(path: str) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("domain"):
                rows.append(row)
    return rows


def load_checkpoint(path: str) -> dict:
    if Path(path).exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_checkpoint(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def append_csv(path: str, rows: list[dict], fieldnames: list[str]):
    exists = Path(path).exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerows(rows)


def apollo_post(url: str, payload: dict, retries: int = 4) -> dict:
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=HEADERS, json=payload, timeout=30)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 60))
                print(f"      ⏳ Rate limited — waiting {wait}s…")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            print(f"      ⚠ Request error (attempt {attempt+1}/{retries}): {e}")
            time.sleep(6 * (attempt + 1))
    return {}


# ── STEP A: SEARCH ───────────────────────────────────────────────────────────

SEARCH_FIELDS = [
    "company", "domain",
    "apollo_id", "first_name", "last_name", "title",
    "seniority", "linkedin_url", "city", "country",
]


def search_people_for_domain(company: str, domain: str) -> list[dict]:
    """Discover people at a domain. No credits consumed."""
    results = []
    for page in range(1, MAX_SEARCH_PAGES + 1):
        payload = {
            "q_organization_domains": domain,
            "page": page,
            "per_page": PAGE_SIZE,
            "person_titles": TARGET_TITLES,
            "person_seniorities": TARGET_SENIORITIES,
        }
        data = apollo_post(SEARCH_URL, payload)
        batch = data.get("people") or []
        if not batch:
            break

        for p in batch:
            results.append({
                "company":      company,
                "domain":       domain,
                "apollo_id":    p.get("id", ""),
                "first_name":   p.get("first_name", ""),
                "last_name":    p.get("last_name", ""),
                "title":        p.get("title", ""),
                "seniority":    p.get("seniority", ""),
                "linkedin_url": p.get("linkedin_url", ""),
                "city":         p.get("city", ""),
                "country":      p.get("country", ""),
            })

        pagination = data.get("pagination", {})
        if page >= pagination.get("total_pages", 1):
            break

        time.sleep(1.5)

    return results


# ── STEP B: ENRICH ───────────────────────────────────────────────────────────

ENRICH_FIELDS = [
    "company", "domain",
    "apollo_id", "first_name", "last_name", "title",
    "seniority", "linkedin_url",
    "email", "email_status",
    "city", "country",
]


def enrich_batch(people_batch: list[dict]) -> list[dict]:
    """
    Send up to 10 people to bulk_match with reveal_personal_emails=true.
    Returns enriched records with email fields populated.
    """
    details = []
    for p in people_batch:
        entry = {"id": p["apollo_id"]}
        # More identifiers = better match rate
        if p.get("linkedin_url"):
            entry["linkedin_url"] = p["linkedin_url"]
        if p.get("domain"):
            entry["domain"] = p["domain"]
        details.append(entry)

    payload = {
        "reveal_personal_emails": True,   # work + personal emails
        "details": details,
    }

    data = apollo_post(ENRICH_URL, payload)
    matched = data.get("matches") or []

    enriched = []
    for i, match in enumerate(matched):
        if not match:
            continue
        # Merge original search data with enriched fields
        original = people_batch[i] if i < len(people_batch) else {}
        enriched.append({
            "company":      original.get("company", ""),
            "domain":       original.get("domain", ""),
            "apollo_id":    match.get("id", original.get("apollo_id", "")),
            "first_name":   match.get("first_name", original.get("first_name", "")),
            "last_name":    match.get("last_name", original.get("last_name", "")),
            "title":        match.get("title", original.get("title", "")),
            "seniority":    match.get("seniority", original.get("seniority", "")),
            "linkedin_url": match.get("linkedin_url", original.get("linkedin_url", "")),
            "email":        match.get("email", ""),
            "email_status": match.get("email_status", ""),
            "city":         match.get("city", original.get("city", "")),
            "country":      match.get("country", original.get("country", "")),
        })

    return enriched


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    if APOLLO_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Set your APOLLO_API_KEY environment variable first.")
        return

    domains = load_domains(DOMAINS_FILE)
    print(f"Loaded {len(domains)} domains from {DOMAINS_FILE}\n")

    search_done = load_checkpoint(CHECKPOINT_SEARCH)
    enrich_done = load_checkpoint(CHECKPOINT_ENRICH)

    # ── STEP A: Search all domains ──────────────────────────────────────────
    print("=" * 55)
    print("STEP A — People discovery (no credits consumed)")
    print("=" * 55)

    all_people: list[dict] = []

    # Load already-searched people from raw file into memory
    if Path(PEOPLE_RAW_FILE).exists():
        with open(PEOPLE_RAW_FILE, newline="", encoding="utf-8") as f:
            all_people = list(csv.DictReader(f))
        print(f"Loaded {len(all_people)} previously discovered people from {PEOPLE_RAW_FILE}\n")

    already_searched_domains = {p["domain"] for p in all_people}

    for i, row in enumerate(domains):
        company = row["company"]
        domain  = row["domain"]

        if domain in search_done or domain in already_searched_domains:
            print(f"  [{i+1}/{len(domains)}] {company} — already searched, skipping")
            continue

        print(f"  [{i+1}/{len(domains)}] Searching: {company} ({domain})")
        people = search_people_for_domain(company, domain)

        if people:
            append_csv(PEOPLE_RAW_FILE, people, SEARCH_FIELDS)
            all_people.extend(people)
            print(f"    → {len(people)} people found")
        else:
            print(f"    → none found")

        search_done[domain] = len(people)
        save_checkpoint(CHECKPOINT_SEARCH, search_done)
        time.sleep(2)

    total_discovered = len(all_people)
    print(f"\nTotal people discovered: {total_discovered}")

    # ── STEP B: Enrich for emails ────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("STEP B — Email enrichment (consumes credits)")
    print("=" * 55)

    # Only enrich people not yet processed
    to_enrich = [p for p in all_people if p.get("apollo_id") and p["apollo_id"] not in enrich_done]
    print(f"People to enrich: {len(to_enrich)}  |  Already enriched: {len(enrich_done)}\n")

    enriched_count = 0
    for batch_num, batch in enumerate(chunks(to_enrich, ENRICH_BATCH)):
        ids_in_batch = [p["apollo_id"] for p in batch]
        print(f"  Batch {batch_num+1}: enriching {len(batch)} people…")

        enriched = enrich_batch(batch)

        if enriched:
            append_csv(PEOPLE_FINAL_FILE, enriched, ENRICH_FIELDS)
            enriched_count += len(enriched)

        # Mark all IDs in batch as done (even if no match returned)
        for apollo_id in ids_in_batch:
            enrich_done[apollo_id] = True
        save_checkpoint(CHECKPOINT_ENRICH, enrich_done)

        emails_in_batch = sum(1 for e in enriched if e.get("email"))
        print(f"    → {emails_in_batch}/{len(batch)} emails found")

        time.sleep(2)  # stay within rate limits

    print(f"\nEnrichment complete.")
    print(f"  People with emails written to: {PEOPLE_FINAL_FILE}")
    print(f"  Raw discovery data kept in:    {PEOPLE_RAW_FILE}")
    print(f"\nSummary:")
    print(f"  Domains processed : {len(search_done)}")
    print(f"  People discovered : {total_discovered}")
    print(f"  People enriched   : {enriched_count}")


if __name__ == "__main__":
    main()