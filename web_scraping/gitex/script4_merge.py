#!/usr/bin/env python3
"""
Script 4 — Merge & Deduplicate
────────────────────────────────
Combines all output CSVs from scripts 1-3 into one
clean master_leads.csv, deduplicated by LinkedIn URL
and Twitter handle.

Also adds a priority score to each lead:
  - Has LinkedIn URL + came from exhibitor dork = HIGH
  - Self-identified via post = HIGH
  - Twitter only = MEDIUM

Output: data/master_leads.csv

Usage:
    python3 script4_merge.py
"""

import csv
import os
from config import (
    OUT_GOOGLE_DORK, OUT_TWITTER, OUT_LI_POSTS,
    OUT_MASTER, MASTER_COLUMNS
)


# ── Priority scoring ──────────────────────────────────────────────────────────

def score_lead(row: dict) -> str:
    source = row.get("source", "")
    has_linkedin = bool(row.get("linkedin_url", "").strip())
    has_name = bool(row.get("full_name", "").strip())
    has_company = bool(row.get("company", "").strip())

    if source == "google_dork" and has_linkedin and has_name:
        return "HIGH"
    if source == "linkedin_post_google" and has_linkedin:
        return "HIGH"
    if source == "twitter_search" and has_name:
        return "MEDIUM"
    if has_linkedin and has_name:
        return "MEDIUM"
    return "LOW"


# ── Deduplication key ─────────────────────────────────────────────────────────

def dedup_key(row: dict) -> str:
    """Primary key: LinkedIn URL. Fallback: twitter handle. Last resort: name+company."""
    li = row.get("linkedin_url", "").strip().lower().rstrip("/")
    tw = row.get("twitter_handle", "").strip().lower().lstrip("@")
    name = row.get("full_name", "").strip().lower()
    company = row.get("company", "").strip().lower()

    if li:
        return f"li:{li}"
    if tw:
        return f"tw:{tw}"
    return f"nc:{name}|{company}"


# ── Main ──────────────────────────────────────────────────────────────────────

def load_csv(path: str) -> list[dict]:
    if not os.path.exists(path):
        print(f"   ⚠️  Not found (skipping): {path}")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"   📄 {os.path.basename(path)}: {len(rows)} rows")
    return rows


def main():
    print("🔀 Merging all lead sources...\n")

    sources = [
        (OUT_GOOGLE_DORK, "google_dork"),
        (OUT_TWITTER,     "twitter_search"),
        (OUT_LI_POSTS,    "linkedin_post_google"),
    ]

    all_rows = []
    for path, source_label in sources:
        rows = load_csv(path)
        # Ensure source field is set
        for r in rows:
            if not r.get("source"):
                r["source"] = source_label
        all_rows.extend(rows)

    print(f"\n   Total before dedup: {len(all_rows)}")

    # Deduplicate
    seen_keys = {}
    deduped = []

    for row in all_rows:
        key = dedup_key(row)
        if key not in seen_keys:
            seen_keys[key] = True
            deduped.append(row)

    print(f"   Total after dedup:  {len(deduped)}")

    # Add priority + clean up fields
    final_columns = list(MASTER_COLUMNS) + ["priority"]
    final_rows = []

    for row in deduped:
        clean = {col: row.get(col, "").strip() if isinstance(row.get(col), str) else row.get(col, "") for col in MASTER_COLUMNS}
        clean["priority"] = score_lead(row)
        final_rows.append(clean)

    # Sort: HIGH first, then MEDIUM, then LOW; then by company
    priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    final_rows.sort(key=lambda r: (priority_order.get(r["priority"], 3), r.get("company", "")))

    # Write master CSV
    with open(OUT_MASTER, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=final_columns)
        writer.writeheader()
        writer.writerows(final_rows)

    # Print summary
    high   = sum(1 for r in final_rows if r["priority"] == "HIGH")
    medium = sum(1 for r in final_rows if r["priority"] == "MEDIUM")
    low    = sum(1 for r in final_rows if r["priority"] == "LOW")

    print(f"\n{'='*50}")
    print(f"✅ MASTER FILE: {OUT_MASTER}")
    print(f"{'='*50}")
    print(f"   🔴 HIGH priority:   {high}")
    print(f"   🟡 MEDIUM priority: {medium}")
    print(f"   ⚪ LOW priority:    {low}")
    print(f"   📊 TOTAL leads:     {len(final_rows)}")
    print(f"\n   Sources breakdown:")

    by_source = {}
    for r in final_rows:
        src = r.get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
    for src, count in sorted(by_source.items()):
        print(f"     {src}: {count}")

    print(f"\n🚀 Ready to load into Apollo for email enrichment!")


if __name__ == "__main__":
    main()