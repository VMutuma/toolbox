#!/usr/bin/env python3
"""
Apollo ABM Scraper — Main
═════════════════════════
Searches Apollo for decision-makers at target companies.

Uses hybrid approach:
1. Smart API search with multiple name variations
2. Fallback to manual company name mappings
3. Progress tracking for resumability
4. Deduplication and clean output

Usage:
    source venv/bin/activate
    python3 apollo_scraper.py

Output:
    data/apollo_leads_[timestamp].csv
    data/apollo_not_found_[timestamp].csv
"""

import csv
import os
import sys
import json
import time
import requests
from datetime import datetime
import pandas as pd

from abm_config import (
    APOLLO_API_KEY, APOLLO_ORG_SEARCH_URL, APOLLO_PEOPLE_SEARCH_URL,
    DATA_DIR, PROGRESS_FILE, MASTER_COLUMNS, VERTICAL_TITLES,
    COMPANY_NAME_MAPPINGS, DELAY_MIN, DELAY_MAX, load_mappings
)


# ─────────────────────────────────────────────────────────────────────────────
# TARGET COMPANIES (by vertical)
# ─────────────────────────────────────────────────────────────────────────────

ACCOUNTS = {
    "Healthcare": [
        "3rd Park Hospital", "Metropolitan Hospital", "Pathcare Laboratories",
        "Medicrest Plus Pharmacy", "Mater Hospital", "Westlands Specialist Hospital",
        "Karen Hospital", "Rayhaan Hospital", "MP Shah Hospital", "Premier Hospital",
        "Luton Hospital", "Khawaja Dentistry", "Nairobi West Hospital",
        "Westlands Medical", "Doctors of Hearing", "Gold Star Healthcare",
        "Avenue Hospital", "Coptic Hospital", "Guru Nanak Hospital",
        "Agha Khan Hospital", "Chiromo Hospital", "Parklands Ambulatory Surgical Center",
        "Mariakani Cottage Hospital", "Imara Hospital", "Menorah Hospital",
        "Nairobi South Hospital", "Bristol Park Hospital", "AIC Kijabe",
        "Meridian Hospital", "AAR Hospital", "Mediheal Hospital",
        "St Lukes Orthopaedic", "Masaba Hospital", "Marie Stopes",
        "Goodlife Pharmacy", "Grand Royal Hospital", "Aster Hospital",
        "Tenwek Hospital", "Meditest Hospital", "Cedar Hospital",
        "Oakwood Hospital", "Malibu Pharmacy", "Dovey Pharmacy",
        "KCMC Hospital", "Aga Khan Hospital Tanzania", "Muhimbili Hospital",
        "Kairuki Hospital", "Regency Medical Centre", "Sanitas Hospital",
        "Shree Hindu Mandal Hospital", "Burhani Charitable Hospital",
        "Africa Healthcare Network", "Medinova Specialized Polyclinic",
        "Ocean Road Cancer Institute", "Ifakara Health Institute",
        "Diabetes Management Medical Center", "Shabaha Cancer Center",
        "Snr Hearing", "Shifa Hospital", "CCBRT", "IST Clinic",
        "Premier Care Clinic", "London Health", "Urban Care Clinic",
        "Livia Health", "Peak Physiology", "Dawa Mkononi", "Afyalink"
    ],
    "Banking & Insurance": [
        "CRDB Bank", "NMB Bank", "Equity Bank", "Access Bank", "Stanbic Bank",
        "UBA Bank", "Azania Bank", "NBC Bank", "Eco Bank", "TCB Bank",
        "NCBA Bank", "DCB Bank", "Mwanga Hakika", "Letshego Bank",
        "Mkombozi Bank", "MCB Bank", "Universal Merchant Bank Ghana",
        "Asa Microfinance", "Absa Bank Kenya", "Co-operative Bank of Kenya",
        "KCB Bank Kenya", "Standard Chartered Bank Kenya", "I&M Bank",
        "Diamond Trust Bank Kenya", "Family Bank", "Prime Bank",
        "SBM Bank Kenya", "National Bank of Kenya", "Bank of Africa",
        "Guaranty Trust Bank", "Victoria Commercial Bank", "Gulf African Bank",
        "Bank of Baroda Kenya", "Credit Bank", "Sidian Bank",
        "Kingdom Bank", "Postbank Kenya", "Development Bank of Kenya",
        "Britam Insurance", "Madison Insurance", "Jubilee Insurance",
        "CIC General Insurance", "APA Insurance", "ICEA LION Insurance",
        "Heritage Insurance", "GA Insurance", "Turaco Microinsurance",
        "AAR Insurance Kenya", "Britam General Insurance",
        "Unaitas Sacco", "Stima Sacco", "Mwalimu National Sacco",
        "Harambee Sacco", "Imarisha Sacco", "Tembo Sacco", "Boresha Sacco",
        "MoFinance", "Lolc Microfinance", "Boresha Credit", "Acorn Investment"
    ],
    "Betting & Gaming": [
        "WezaBet", "SportyBet", "Melbet", "Betwinner", "Paripesa",
        "Megapari", "Mozzartbet", "Linebet", "Maybets", "EuroVirtuals",
        "iGaming Consult", "Ocean Gaming Consult", "Gaminglabs", "Kayzalbet",
        "MulaSport", "W88 Africa", "1win", "888starz", "Dafabet",
        "Kwikbet", "Bangbet", "BC Game", "Betway", "Betika",
        "BwinBet", "Optimove", "Entain", "WekaWin"
    ],
    "EV & Clean Energy": [
        "Spiro", "Roam", "Arc Ride", "eBee", "Kibo", "Zembo Bikes",
        "Jiwambe", "Greenwheels", "E-bikes Africa", "Powerhive",
        "Ampersand", "G-Rani", "Equator Mobility", "E-moti", "Ndai",
        "Chargebyte", "Solar Panda", "Zola Electric", "Azuri Technologies",
        "Bboxx", "Lesso Solar", "UEDCL", "Innovex Uganda", "Aquasol", "Instollar"
    ],
    "Agri & Food": [
        "Advanta Seeds", "Chiromo Fert", "Western Seeds", "Amiran Kenya",
        "Amiran Tanzania", "Yara", "Balton TZ Seed", "Seedco",
        "Corteva", "Apollo Agriculture", "Pula Advisors",
        "Shamba Pride", "Coamana", "Farm to Feed", "OneAcre Fund"
    ],
    "Logistics & Cargo": [
        "Kargo 360", "Horse Cargo", "CargoLink", "Logistix Africa",
        "Fox Cargo", "GNM Cargo", "Bei Poa Air Cargo", "Kargo Tanzania",
        "Epic Cargo", "Cargofasta Logistics", "Jamaty Cargo",
        "TanAir Cargo", "Skyport Cargo", "Rapid Cargo", "SAS Logistics",
        "Usangu Logistics", "AGL Logistics", "Allmol Freight",
        "DP World", "Mantrac", "Millennial Cargo"
    ],
    "ISPs & Telecom": [
        "Savannah Fiber", "ATC", "Habarinode", "Maisha Broadband",
        "WIACOM TZ", "Flashnet Technologies", "WORLDLINK", "Istore", "ISP"
    ],
    "Other": [
        "Haco Industries", "G4S", "Mwaliko Events", "Go Promotion",
        "Smart Events", "ChapBuy", "Hafele", "MSD", "CTrack",
        "KoraPay", "Niobi", "Kentrade", "Kwanza SMS",
        "Pyramid Creative Concepts", "DMJot", "Dcash Africa",
        "Royal Notify Africa", "AfroPari", "OPAY", "Korapay"
    ]
}


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS TRACKING
# ─────────────────────────────────────────────────────────────────────────────

def load_progress() -> set:
    """Load set of companies already processed."""
    if not os.path.exists(PROGRESS_FILE):
        return set()
    with open(PROGRESS_FILE) as f:
        return set(line.strip() for line in f if line.strip())


def save_progress(company: str):
    """Append company to progress file."""
    with open(PROGRESS_FILE, "a") as f:
        f.write(company + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# APOLLO API SEARCH
# ─────────────────────────────────────────────────────────────────────────────

def search_organization(api_key: str, company_name: str) -> str | None:
    """
    Search Apollo for company org ID using multiple name variations.
    
    Tries:
    1. Manual mapping (if exists)
    2. Exact name
    3. Remove common suffixes
    4. First word only
    5. With country codes (KE, TZ, UG, etc.)
    6. Acronyms
    """
    
    # Check manual mapping first
    if company_name in COMPANY_NAME_MAPPINGS:
        search_names = [COMPANY_NAME_MAPPINGS[company_name]]
    else:
        # Generate variations
        search_names = [company_name]
        
        # Remove common suffixes
        cleaned = company_name
        for suffix in [" Bank", " Hospital", " Limited", " Ltd", " Inc", " Plc", " PLC"]:
            cleaned = cleaned.replace(suffix, "")
        if cleaned != company_name:
            search_names.append(cleaned.strip())
        
        # First word only
        first_word = company_name.split()[0]
        if first_word != company_name:
            search_names.append(first_word)
        
        # With country codes
        for code in ["KE", "TZ", "UG", "RW", "BI"]:
            search_names.append(f"{company_name} {code}")
            if cleaned != company_name:
                search_names.append(f"{cleaned} {code}")
        
        # Acronym
        words = company_name.split()
        if len(words) > 1:
            acronym = "".join(w[0] for w in words if w)
            search_names.append(acronym)
        
        # Deduplicate
        search_names = list(dict.fromkeys(search_names))
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    
    # Try each variation
    for i, search_name in enumerate(search_names):
        payload = {
            "q_organization_name": search_name,
            "per_page": 1
        }
        
        try:
            resp = requests.post(APOLLO_ORG_SEARCH_URL, headers=headers, json=payload, timeout=15)
            
            if resp.status_code == 200:
                data = resp.json()
                orgs = data.get("organizations", [])
                if orgs:
                    return orgs[0].get("id")
            
            elif resp.status_code == 429:
                print(f"  ⚠ Rate limited — waiting 10s...")
                time.sleep(10)
                return search_organization(api_key, company_name)
            
            elif resp.status_code == 401:
                print("\n✗ Invalid API key")
                sys.exit(1)
            
            # Small delay between attempts
            if i < len(search_names) - 1:
                time.sleep(0.3)
        
        except requests.exceptions.RequestException as e:
            continue
    
    return None


def search_people(api_key: str, org_id: str, titles: list) -> dict | None:
    """Search for people at organization with given titles."""
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    payload = {
        "organization_ids": [org_id],
        "person_titles": titles,
        "per_page": 10
    }
    
    try:
        resp = requests.post(APOLLO_PEOPLE_SEARCH_URL, headers=headers, json=payload, timeout=15)
        
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 429:
            print(f"  ⚠ Rate limited — waiting 10s...")
            time.sleep(10)
            return search_people(api_key, org_id, titles)
        elif resp.status_code == 401:
            print("\n✗ Invalid API key")
            sys.exit(1)
        else:
            return None
    
    except requests.exceptions.RequestException:
        return None


def extract_leads(data: dict, company_name: str, vertical: str) -> list[dict]:
    """Parse Apollo response into lead dicts."""
    leads = []
    if not data or "people" not in data:
        return leads
    
    for person in data.get("people", []):
        org = person.get("organization") or {}
        email = person.get("email") or ""
        
        # Skip invalid emails
        if person.get("email_status") == "invalid":
            continue
        
        lead = {
            "vertical": vertical,
            "target_company": company_name,
            "first_name": person.get("first_name", ""),
            "last_name": person.get("last_name", ""),
            "title": person.get("title", ""),
            "email": email,
            "email_status": person.get("email_status", ""),
            "phone": person.get("sanitized_phone", ""),
            "linkedin_url": person.get("linkedin_url", ""),
            "company_name": org.get("name", company_name),
            "company_website": org.get("website_url", ""),
            "company_industry": org.get("industry", ""),
            "company_size": org.get("estimated_num_employees", ""),
            "company_country": org.get("country", ""),
            "company_city": org.get("city", ""),
            "seniority": person.get("seniority", ""),
            "departments": ", ".join(person.get("departments", [])),
        }
        leads.append(lead)
    
    return leads


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SCRAPER
# ─────────────────────────────────────────────────────────────────────────────

def run_scrape(api_key: str) -> tuple[list, list]:
    """Run the scraper across all companies."""
    all_leads = []
    not_found = []
    total_companies = sum(len(v) for v in ACCOUNTS.values())
    processed = 0
    
    print(f"\n{'='*55}")
    print(f"  Apollo ABM Scraper — {total_companies} companies across {len(ACCOUNTS)} verticals")
    print(f"{'='*55}\n")
    
    done = load_progress()
    
    for vertical, companies in ACCOUNTS.items():
        titles = VERTICAL_TITLES.get(vertical, [])
        print(f"▶ {vertical} ({len(companies)} accounts)")
        
        for company in companies:
            processed += 1
            print(f"  [{processed}/{total_companies}] {company}...", end=" ", flush=True)
            
            if company in done:
                print("(skipped - already done)")
                continue
            
            # Find org ID
            org_id = search_organization(api_key, company)
            if not org_id:
                print("✗ not found")
                not_found.append({"company": company, "vertical": vertical})
                save_progress(company)
                time.sleep(0.5)
                continue
            
            # Find people
            data = search_people(api_key, org_id, titles)
            leads = extract_leads(data, company, vertical)
            
            if leads:
                print(f"✓ {len(leads)}")
                all_leads.extend(leads)
            else:
                print("— no results")
            
            save_progress(company)
            time.sleep(1.1)
        
        print(f"  → {vertical} done\n")
    
    return all_leads, not_found


def save_results(leads: list, not_found: list):
    """Save leads and not-found companies to CSV."""
    if not leads:
        print("\n⚠ No leads found.")
        return
    
    df = pd.DataFrame(leads)
    
    # Deduplicate by email
    df_dedup = df.drop_duplicates(subset=["email"], keep="first")
    dupes = len(df) - len(df_dedup)
    
    # Sort
    df_dedup = df_dedup.sort_values(["vertical", "target_company"])
    
    # Save leads
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    leads_file = f"{DATA_DIR}/apollo_leads_{timestamp}.csv"
    df_dedup.to_csv(leads_file, index=False)
    
    # Save not found
    if not_found:
        not_found_file = f"{DATA_DIR}/apollo_not_found_{timestamp}.csv"
        df_nf = pd.DataFrame(not_found).sort_values(["vertical", "company"])
        df_nf.to_csv(not_found_file, index=False)
    else:
        not_found_file = None
    
    # Summary
    print(f"\n{'='*55}")
    print(f"  ✓ Done!")
    print(f"  Leads found:          {len(df)}")
    print(f"  After dedup:          {len(df_dedup)}")
    print(f"  Dupes removed:        {dupes}")
    print(f"  Output:               {leads_file}")
    if not_found_file:
        print(f"  Not found:            {not_found_file}")
        print(f"  Companies to investigate: {len(not_found)}")
    print(f"{'='*55}\n")
    
    # Breakdown by vertical
    print("  Breakdown by vertical:")
    summary = df_dedup.groupby("vertical").size().reset_index(name="leads")
    for _, row in summary.iterrows():
        print(f"    {row['vertical']:<25} {row['leads']} leads")
    
    if not_found:
        print(f"\n  Not found by vertical:")
        summary_nf = pd.DataFrame(not_found).groupby("vertical").size().reset_index(name="companies")
        for _, row in summary_nf.iterrows():
            print(f"    {row['vertical']:<25} {row['companies']} companies")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not APOLLO_API_KEY:
        print("✗ APOLLO_API_KEY not found in environment")
        print("  Create .env file with: APOLLO_API_KEY=your_key")
        sys.exit(1)
    
    # Load company name mappings
    load_mappings()
    
    # Run scraper
    leads, not_found = run_scrape(APOLLO_API_KEY)
    
    # Save results
    save_results(leads, not_found)