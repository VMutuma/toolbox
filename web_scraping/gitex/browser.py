import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import CHROMIUM_BINARY, CHROMEDRIVER_BIN, DELAY_MIN, DELAY_MAX, CAPTCHA_WAIT


def make_driver(headless: bool = False) -> webdriver.Chrome:
    options = Options()
    options.binary_location = CHROMIUM_BINARY
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    )
    if headless:
        options.add_argument("--headless=new")
    service = Service(executable_path=CHROMEDRIVER_BIN)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def human_delay(min_s: float = None, max_s: float = None):
    lo = min_s or DELAY_MIN
    hi = max_s or DELAY_MAX
    time.sleep(random.uniform(lo, hi))


def is_captcha_page(driver: webdriver.Chrome) -> bool:
    """Check if current page is actually a captcha/block page — not a results page."""
    try:
        page = driver.page_source.lower()
        url  = driver.current_url.lower()
        # Real captcha signals — these don't appear on normal result pages
        if "google.com/sorry" in url:
            return True
        if "unusual traffic" in page:
            return True
        if "why did this happen" in page:
            return True
        # Captcha page has no search result divs
        results = driver.find_elements(By.CSS_SELECTOR, "div.g, div#search")
        if not results and "captcha" in page:
            return True
        return False
    except Exception:
        return False


def wait_for_captcha(driver: webdriver.Chrome, check_phrase: str = "captcha"):
    """Pause if captcha detected, resume automatically once solved."""
    if not is_captcha_page(driver):
        return
    print("\n" + "="*60)
    print("⚠️  CAPTCHA DETECTED — Please solve it in the browser window.")
    print("    Checking every 5 seconds until resolved...")
    print("="*60 + "\n")
    while True:
        time.sleep(5)
        try:
            if not is_captcha_page(driver):
                break
        except Exception:
            break
    print("✅ Captcha cleared. Continuing...\n")


def safe_get(driver: webdriver.Chrome, url: str):
    driver.get(url)
    human_delay(2, 4)
    wait_for_captcha(driver)


def extract_links(driver: webdriver.Chrome, domain_filter: str = "") -> list[str]:
    anchors = driver.find_elements(By.TAG_NAME, "a")
    links = []
    for a in anchors:
        try:
            href = a.get_attribute("href") or ""
            if domain_filter and domain_filter not in href:
                continue
            if href and href not in links:
                links.append(href)
        except Exception:
            continue
    return links
