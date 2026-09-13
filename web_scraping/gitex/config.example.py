# ─────────────────────────────────────────────
# GITEX Kenya Lead Scraper — Shared Config
# ─────────────────────────────────────────────

import os

# ── Paths ──────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

EXHIBITORS_CSV     = os.path.join(BASE_DIR, "gitex_kenya_exhibitors_only.csv")
OUT_GOOGLE_DORK    = os.path.join(DATA_DIR, "out_google_dork.csv")
OUT_TWITTER        = os.path.join(DATA_DIR, "out_twitter.csv")
OUT_LI_POSTS       = os.path.join(DATA_DIR, "out_linkedin_posts.csv")
OUT_MASTER         = os.path.join(DATA_DIR, "master_leads.csv")

# ── Selenium / Browser ─────────────────────────
# Snap Chromium paths on WSL/Ubuntu
CHROMIUM_BINARY  = "/usr/bin/google-chrome"
CHROMEDRIVER_BIN = "/usr/local/bin/chromedriver"

# ── Delays (seconds) ───────────────────────────
DELAY_MIN        = 4     # min pause between requests
DELAY_MAX        = 9     # max pause between requests
CAPTCHA_WAIT     = 60    # seconds to wait before re-checking after captcha

# ── Target Titles ──────────────────────────────
TARGET_TITLES = [
    # C-Suite
    "CEO", "CTO", "COO", "Chief Executive",
    "Chief Technology", "Chief Operating",
    # Founders
    "Founder", "Co-Founder",
    # Management
    "Managing Director", "General Manager",
    "Country Manager", "Regional Director",
    "Africa Director", "East Africa",
    # Sales & Partnerships
    "Director of Sales", "Sales Director", "Head of Sales",
    "Business Development", "Head of Partnerships",
    "Partnerships Director", "VP Sales", "VP Partnerships",
    # CX
    "Customer Experience", "Customer Success",
    "Client Relations", "Customer Engagement",
    "Head of CX", "CX Director", "CX Manager",
    "Client Success",
]

# Shorter list for search queries (too many breaks Google)
SEARCH_TITLES = [
    "CEO", "Founder", "Managing Director", "Country Manager",
    "Business Development", "Head of Sales", "Director",
    "Customer Experience", "Customer Success", "CTO",
    "VP", "Partnerships", "Africa", "East Africa",
]

# ── Event Keywords (for Twitter + LinkedIn post search) ──
EVENT_KEYWORDS = [
    "AI Everything Kenya",
    "GITEX Kenya",
    "aieverythingkenya",
    "gitexkenya",
    "#AIEverythingKenya",
    "#GITEXKenya",
]

# ── Master CSV columns ─────────────────────────
MASTER_COLUMNS = [
    "full_name",
    "title",
    "company",
    "country",
    "linkedin_url",
    "twitter_handle",
    "source",
    "notes",
    "sectors",
]