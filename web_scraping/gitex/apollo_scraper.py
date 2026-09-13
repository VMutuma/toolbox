"""
Apollo.io Decision-Maker Scraper (Fixed)
=========================================
Searches Apollo for decision-makers at each account, exports to CSV.

Usage:
    python apollo_scraper.py --api-key YOUR_API_KEY

Output:
    apollo_leads_[timestamp].csv
"""

import requests
import pandas as pd
import time
import argparse
import sys
import json
from datetime import datetime

# ─── COMPANY NAME MAPPINGS ───────────────────────────────────────────────────
# If you create a file called 'company_name_mappings.csv' with columns:
# original_name,alternative_name
# It will use the alternative names instead of the original names.
# Example:
#   KCB Bank Kenya,KCB
#   Equity Bank,Equity Bank Group

COMPANY_MAPPINGS = {}

def load_company_mappings():
    """Load alternative company names from CSV if it exists."""
    import os
    if os.path.exists("./data/company_name_mappings.csv"):
        try:
            mapping_df = pd.read_csv("./data/company_name_mappings.csv")
            for _, row in mapping_df.iterrows():
                original = row.get("original_name", "").strip()
                alternative = row.get("alternative_name", "").strip()
                if original and alternative:
                    COMPANY_MAPPINGS[original] = alternative
            print(f"✓ Loaded {len(COMPANY_MAPPINGS)} company name mappings")
        except Exception as e:
            print(f"⚠ Could not load mappings: {e}")

# ─── CONFIG ──────────────────────────────────────────────────────────────────

# Target job titles per vertical — Apollo will match any of these
VERTICAL_TITLES = {
    "Healthcare": [
        "IT Director", "Chief Medical Officer", "CMO", "CEO", "Head of Patient Experience",
        "Chief Information Officer", "CIO", "Medical Director", "Hospital Director",
        "Head of Operations", "Chief Operating Officer"
    ],
    "Banking & Insurance": [
        "Head of Digital", "CTO", "Chief Technology Officer", "Head of Retail Banking",
        "IT Manager", "COO", "Chief Operating Officer", "Head of IT",
        "Digital Transformation", "Head of Innovation", "Chief Digital Officer",
        "Head of Insurance", "Chief Information Officer"
    ],
    "Betting & Gaming": [
        "CTO", "Head of CRM", "Head of Marketing", "Product Manager",
        "Chief Technology Officer", "Chief Marketing Officer", "CMO",
        "Head of Customer Retention", "Head of Product"
    ],
    "EV & Clean Energy": [
        "CEO", "Co-Founder", "Founder", "Head of Operations", "COO",
        "Customer Experience", "Head of Customer Success", "Operations Manager"
    ],
    "Agri & Food": [
        "CEO", "Founder", "Head of Farmer Engagement", "Operations Director",
        "Head of Operations", "Managing Director"
    ],
    "Logistics & Cargo": [
        "Operations Manager", "Head of Customer Service", "CEO", "Managing Director",
        "Head of Logistics", "COO", "General Manager"
    ],
    "ISPs & Telecom": [
        "CTO", "Head of Customer Experience", "Commercial Director",
        "Chief Technology Officer", "Head of Operations", "CEO"
    ],
    "Other": [
        "CMO", "Head of Communications", "Operations Lead", "CEO",
        "Managing Director", "Head of Marketing", "Chief Marketing Officer"
    ]
}

# All accounts mapped to verticals
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

# Apollo API endpoints
APOLLO_ORG_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_companies/search"
APOLLO_PEOPLE_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/api_search"

# ─── FUNCTIONS ───────────────────────────────────────────────────────────────

def search_organization(api_key, company_name):
    """Search for a company by name to get its Apollo organization ID.
    
    First checks if there's a manual mapping for the company.
    Then tries multiple strategies:
    1. Exact name
    2. Remove common suffixes (Bank, Hospital, Ltd, Limited, etc.)
    3. First word only
    4. Name with country code (KE, TZ, UG)
    5. Abbreviations (first letters of words)
    """
    
    # Check if there's a manual mapping for this company
    if company_name in COMPANY_MAPPINGS:
        search_names = [COMPANY_MAPPINGS[company_name]]
    else:
        # Generate search variations
        search_names = [company_name]  # Start with exact name
        
        # Remove common suffixes
        cleaned = company_name
        for suffix in [" Bank", " Hospital", " Limited", " Ltd", " Inc", " Plc", " PLC"]:
            cleaned = cleaned.replace(suffix, "")
        if cleaned != company_name:
            search_names.append(cleaned.strip())
        
        # Try first word only
        first_word = company_name.split()[0]
        if first_word != company_name:
            search_names.append(first_word)
        
        # Try with country codes (common in East Africa)
        for code in ["KE", "TZ", "UG", "RW", "BI"]:
            search_names.append(f"{company_name} {code}")
            if cleaned != company_name:
                search_names.append(f"{cleaned} {code}")
        
        # Try acronym (first letter of each word)
        words = company_name.split()
        if len(words) > 1:
            acronym = "".join(w[0] for w in words if w)
            search_names.append(acronym)
        
        # Remove duplicates while preserving order
        search_names = list(dict.fromkeys(search_names))
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    
    # Try each name variation
    for i, search_name in enumerate(search_names):
        payload = {
            "q_organization_name": search_name,
            "per_page": 1
        }
        
        try:
            resp = requests.post(APOLLO_ORG_SEARCH_URL, headers=headers, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                organizations = data.get("organizations", [])
                if organizations:
                    return organizations[0].get("id")
            elif resp.status_code == 429:
                print(f"  ⚠ Rate limited — waiting 10s...")
                time.sleep(10)
                return search_organization(api_key, company_name)
            elif resp.status_code == 401:
                print("\n✗ Invalid API key. Check your key and try again.")
                sys.exit(1)
            
            # Small delay between attempts
            if i < len(search_names) - 1:
                time.sleep(0.3)
        except requests.exceptions.RequestException as e:
            continue
    
    return None


def search_people(api_key, org_id, titles, vertical):
    """Search Apollo for people at an organization matching given titles."""
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
            return search_people(api_key, org_id, titles, vertical)
        elif resp.status_code == 401:
            print("\n✗ Invalid API key. Check your key and try again.")
            sys.exit(1)
        else:
            print(f"  ✗ Error {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Network error: {e}")
        return None


def extract_leads(data, company_name, vertical):
    """Parse Apollo response into a list of lead dicts."""
    leads = []
    if not data or "people" not in data:
        return leads

    for person in data.get("people", []):
        org = person.get("organization") or {}
        email = person.get("email") or ""
        
        # Skip if email is clearly invalid
        if person.get("email_status") == "invalid":
            continue

        lead = {
            "vertical":             vertical,
            "target_company":       company_name,
            "first_name":           person.get("first_name", ""),
            "last_name":            person.get("last_name", ""),
            "title":                person.get("title", ""),
            "email":                email,
            "email_status":         person.get("email_status", ""),
            "phone":                person.get("sanitized_phone", ""),
            "linkedin_url":         person.get("linkedin_url", ""),
            "company_name":         org.get("name", company_name),
            "company_website":      org.get("website_url", ""),
            "company_industry":     org.get("industry", ""),
            "company_size":         org.get("estimated_num_employees", ""),
            "company_country":      org.get("country", ""),
            "company_city":         org.get("city", ""),
            "seniority":            person.get("seniority", ""),
            "departments":          ", ".join(person.get("departments", [])),
        }
        leads.append(lead)

    return leads


def run_scrape(api_key):
    all_leads = []
    total_companies = sum(len(v) for v in ACCOUNTS.values())
    processed = 0
    not_found = []

    print(f"\n{'='*55}")
    print(f"  Apollo ABM Scraper — {total_companies} companies across {len(ACCOUNTS)} verticals")
    print(f"{'='*55}\n")

    for vertical, companies in ACCOUNTS.items():
        titles = VERTICAL_TITLES.get(vertical, [])
        print(f"▶ {vertical} ({len(companies)} accounts)")

        for company in companies:
            processed += 1
            print(f"  [{processed}/{total_companies}] {company}...", end=" ", flush=True)

            # Step 1: Find org ID
            org_id = search_organization(api_key, company)
            if not org_id:
                print("✗ not found in Apollo")
                not_found.append({"company": company, "vertical": vertical})
                time.sleep(0.5)
                continue

            # Step 2: Search for people at that org
            data = search_people(api_key, org_id, titles, vertical)
            leads = extract_leads(data, company, vertical)

            if leads:
                print(f"✓ {len(leads)} contacts")
                all_leads.extend(leads)
            else:
                print("— no results")

            time.sleep(1.1)

        print(f"  → {vertical} done\n")

    return all_leads, not_found


def save_csv(leads, not_found):
    import os
    
    # Create output directory if it doesn't exist
    output_dir = "./data"
    os.makedirs(output_dir, exist_ok=True)
    
    if not leads:
        print("\n⚠ No leads found. Check your API key or company names.")
        return None

    df = pd.DataFrame(leads)

    # Deduplicate on email (keep first occurrence)
    df_deduped = df.drop_duplicates(subset=["email"], keep="first")
    dupes_removed = len(df) - len(df_deduped)

    # Sort by vertical then company
    df_deduped = df_deduped.sort_values(["vertical", "target_company"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save leads
    leads_file = f"{output_dir}/apollo_leads_{timestamp}.csv"
    df_deduped.to_csv(leads_file, index=False)

    # Save not found companies for investigation
    if not_found:
        not_found_file = f"{output_dir}/apollo_not_found_{timestamp}.csv"
        df_not_found = pd.DataFrame(not_found)
        df_not_found = df_not_found.sort_values(["vertical", "company"])
        df_not_found.to_csv(not_found_file, index=False)
    else:
        not_found_file = None

    print(f"\n{'='*55}")
    print(f"  ✓ Done!")
    print(f"  Total leads found:    {len(df)}")
    print(f"  After deduplication:  {len(df_deduped)}")
    print(f"  Dupes removed:        {dupes_removed}")
    print(f"  Output file:          {leads_file}")
    if not_found_file:
        print(f"  Not found file:       {not_found_file}")
        print(f"  Companies to investigate: {len(not_found)}")
    print(f"{'='*55}\n")

    # Summary by vertical
    print("  Breakdown by vertical:")
    summary = df_deduped.groupby("vertical").size().reset_index(name="leads")
    for _, row in summary.iterrows():
        print(f"    {row['vertical']:<25} {row['leads']} leads")

    if not_found:
        print(f"\n  Not found by vertical:")
        summary_nf = pd.DataFrame(not_found).groupby("vertical").size().reset_index(name="companies")
        for _, row in summary_nf.iterrows():
            print(f"    {row['vertical']:<25} {row['companies']} companies")

    return leads_file, not_found_file


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apollo.io ABM Decision-Maker Scraper")
    parser.add_argument("--api-key", required=True, help="Your Apollo API key")
    args = parser.parse_args()

    # Load any manual company name mappings
    load_company_mappings()
    
    leads, not_found = run_scrape(args.api_key)
    save_csv(leads, not_found)