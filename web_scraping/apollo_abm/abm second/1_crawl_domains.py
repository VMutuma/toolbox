"""
Step 1: Crawl company domains using Google Search via Selenium.
For each company, searches Google and picks the most likely official domain.
Results are checkpointed to CSV so you can resume if it crashes.
"""

import csv
import os
import time
import random
from dataclasses import dataclass, fields
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ── CONFIG ──────────────────────────────────────────────────────────────────
CHECKPOINT_FILE = "domains_checkpoint.csv"   # progress is saved here
OUTPUT_FILE     = "domains_final.csv"         # clean output at the end
HEADLESS        = False          # set True to run without a browser window
SLEEP_MIN       = 3              # seconds between searches (min)
SLEEP_MAX       = 7              # seconds between searches (max)
COUNTRY_HINT    = "Kenya Tanzania"  # appended to each search query

# ── COMPANY LIST ─────────────────────────────────────────────────────────────
# Paste your full list here. Duplicates are removed automatically.
RAW_COMPANIES = """
Khawaja Dentistry
Komarock Modern
E-moti
Ndai
CTrack
WezaBet
Kafika House
TanzMED
Afya Plus
CIHEB Tanzania
WAJAMAMA
ECSA
Ifakara Health Institute
Maisha Broadband
WIACOM TZ
Flashnet Technologies
WORLDLINK
AMBONI GROUP
BwinBet
Red Tech
Ocean Gaming
Optimove
Entain
KoraPay
Niobi
WekaWin
Kentrade
OneAcre Fund
Tembo Sacco
Mwito Sacco
Acorn Investment
Seedco
Lolc Microfinance
Boresha Credit
Corteva
Credit Bank
Family Bank
Childline Kenya
United Winners Sacco
My line Networks
Gig Secure
Pure Bliss
AvadaPay
Opes Technologies
Development Bank of Kenya
Soil Merchants
Opalnet Limited
Korapay
Postbank Kenya
Kenya Redcross
Absa Bank Kenya
Co-operative Bank of Kenya
KCB Bank Kenya
Standard Chartered Bank Kenya
I&M Bank
Diamond Trust Bank Kenya
Family Bank Ltd
Prime Bank
SBM Bank Kenya
Access Bank Kenya
Ecobank Kenya
National Bank of Kenya
Bank of Africa
ABC Bank Kenya
Guaranty Trust Bank
Victoria Commercial Bank
HFC Limited
Gulf African Bank
Bank of Baroda Kenya
Bank of India Kenya
M-Oriental Bank
Consolidated Bank of Kenya
Kingdom Bank Kenya
Sidian Bank
Guardian Bank Kenya
Middle East Bank Kenya
Paramount Bank Kenya
Premier Bank Kenya
CIB Bank KE
Wanandege Sacco
Unaitas Sacco
Stima Sacco
Boresha Sacco
Mwalimu National Sacco
Harambee Sacco
National Police Sacco
Imarisha Sacco
Caritas Sacco
Maisha Bora Sacco
K-Unity Sacco
Skyline Sacco
Gusii Mwalimu Sacco
Solution Sacco
Fortune Sacco
Madison Insurance
Britam General Insurance Kenya
Jubilee Allianz General Insurance Kenya
CIC General Insurance
APA Insurance
ICEA LION General Insurance
Heritage Insurance Kenya
GA Insurance
Kenya Orient Insurance
Directline Assurance
Old Mutual General Insurance Kenya
Sanlam General Insurance Kenya
First Assurance Kenya
Takaful Insurance of Africa
Turaco Microinsurance
AAR Insurance Kenya
Africa Merchant Assurance AMACO
NCBA Insurance Kenya
Bupa Global Insurance
Cannon General Insurance Kenya
Corporate Insurance Kenya
Fidelity Shield Insurance
Geminia Insurance
Jubilee Health Insurance
Kenindia Assurance
Mayfair Insurance Kenya
MUA Insurance Kenya
Pacis Insurance Kenya
Pioneer General Insurance
Tausi Assurance
The Kenyan Alliance Insurance
The Monarch Insurance Kenya
Trident Insurance Kenya
Birdview Micro Insurance
Star Discover Insurance
""".strip()

# ── HELPERS ──────────────────────────────────────────────────────────────────

def clean_companies(raw: str) -> list[str]:
    seen, result = set(), []
    for line in raw.splitlines():
        name = line.strip().strip('"').strip("'")
        if name and name.lower() not in seen:
            seen.add(name.lower())
            result.append(name)
    return result


def load_checkpoint(path: str) -> dict[str, str]:
    """Returns {company_name: domain} for already-processed companies."""
    done = {}
    if not os.path.exists(path):
        return done
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            done[row["company"]] = row["domain"]
    return done


def save_row(path: str, company: str, domain: str, write_header: bool = False):
    mode = "w" if write_header else "a"
    with open(path, mode, newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "domain"])
        if write_header:
            w.writeheader()
        w.writerow({"company": company, "domain": domain})


def make_driver(headless: bool) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


SKIP_DOMAINS = {
    "google.com", "facebook.com", "linkedin.com", "twitter.com",
    "instagram.com", "youtube.com", "wikipedia.org", "yelp.com",
    "tripadvisor.com", "bloomberg.com", "reuters.com", "businesswire.com",
    "crunchbase.com", "zoominfo.com", "apollo.io", "glassdoor.com",
}


def extract_domain_from_url(url: str) -> str:
    """Strip scheme, www, and path from a URL to get the bare domain."""
    import re
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"^www\.", "", url)
    url = url.split("/")[0].split("?")[0]
    return url.lower().strip()


def search_domain(driver: webdriver.Chrome, company: str) -> str:
    """Google the company and return the best matching domain."""
    query = f"{company} {COUNTRY_HINT} official website"
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    driver.get(search_url)

    # Wait for results
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#search"))
        )
    except Exception:
        return ""

    # Try to grab cite elements (shown URLs in results)
    candidates = []

    # Method 1: <cite> tags in organic results
    cites = driver.find_elements(By.CSS_SELECTOR, "cite")
    for cite in cites:
        text = cite.text.strip()
        if text:
            domain = extract_domain_from_url(text)
            if domain and not any(s in domain for s in SKIP_DOMAINS):
                candidates.append(domain)

    # Method 2: result anchor hrefs
    if not candidates:
        anchors = driver.find_elements(By.CSS_SELECTOR, "div#search a[href]")
        for a in anchors:
            href = a.get_attribute("href") or ""
            if href.startswith("http") and "google" not in href:
                domain = extract_domain_from_url(href)
                if domain and not any(s in domain for s in SKIP_DOMAINS):
                    candidates.append(domain)

    return candidates[0] if candidates else ""


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    companies = clean_companies(RAW_COMPANIES)
    print(f"Total companies: {len(companies)}")

    done = load_checkpoint(CHECKPOINT_FILE)
    print(f"Already processed: {len(done)} — resuming…\n")

    # Write header only if starting fresh
    if not done:
        save_row(CHECKPOINT_FILE, "company", "domain", write_header=True)

    driver = make_driver(HEADLESS)

    try:
        for i, company in enumerate(companies):
            if company in done:
                print(f"  [skip] {company} → {done[company]}")
                continue

            print(f"  [{i+1}/{len(companies)}] Searching: {company}")
            try:
                domain = search_domain(driver, company)
            except Exception as e:
                print(f"    ERROR: {e}")
                domain = ""

            done[company] = domain
            save_row(CHECKPOINT_FILE, company, domain)
            print(f"    → {domain or '(not found)'}")

            # Random sleep to avoid rate-limiting
            time.sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

    finally:
        driver.quit()

    # Write clean final output
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "domain"])
        w.writeheader()
        for company, domain in done.items():
            w.writerow({"company": company, "domain": domain})

    found = sum(1 for d in done.values() if d)
    print(f"\nDone. {found}/{len(done)} domains found.")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()