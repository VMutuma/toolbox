# ─────────────────────────────────────────────
# Apollo ABM Scraper — Config
# ─────────────────────────────────────────────
# Separate from GITEX config — ABM scraper is independent

import os
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ── Apollo API ─────────────────────────────────
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
APOLLO_ORG_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_companies/search"
APOLLO_PEOPLE_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/api_search"

# ── Browser / Selenium ─────────────────────────
CHROMIUM_BINARY = "/usr/bin/google-chrome"
CHROMEDRIVER_BIN = "/usr/local/bin/chromedriver"

# ── Delays (seconds) ───────────────────────────
DELAY_MIN = 1
DELAY_MAX = 2
CAPTCHA_WAIT = 60

# ── Company Name Overrides ─────────────────────
# When a company isn't found by exact name, try these alternatives
# Load from CSV: data/company_name_mappings.csv
# Format: original_name,alternative_name
COMPANY_NAME_MAPPINGS = {}

def load_mappings():
    """Load company name mappings from CSV if it exists."""
    import csv
    mapping_file = os.path.join(DATA_DIR, "company_name_mappings.csv")
    if os.path.exists(mapping_file):
        try:
            with open(mapping_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    original = row.get("original_name", "").strip()
                    alternative = row.get("alternative_name", "").strip()
                    if original and alternative:
                        COMPANY_NAME_MAPPINGS[original] = alternative
            print(f"✓ Loaded {len(COMPANY_NAME_MAPPINGS)} company name mappings")
        except Exception as e:
            print(f"⚠ Could not load mappings: {e}")

# ── Decision-maker Titles ──────────────────────
# Target job titles per vertical
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

# ── Master CSV columns ─────────────────────────
MASTER_COLUMNS = [
    "vertical",
    "target_company",
    "first_name",
    "last_name",
    "title",
    "email",
    "email_status",
    "phone",
    "linkedin_url",
    "company_name",
    "company_website",
    "company_industry",
    "company_size",
    "company_country",
    "company_city",
    "seniority",
    "departments",
]

# ── Output files ───────────────────────────────
OUTPUT_LEADS = os.path.join(DATA_DIR, "apollo_leads_{timestamp}.csv")
OUTPUT_NOT_FOUND = os.path.join(DATA_DIR, "apollo_not_found_{timestamp}.csv")
PROGRESS_FILE = os.path.join(DATA_DIR, "scraper_progress.txt")