from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import random
import json
import os
from datetime import datetime

# ============= CONFIGURATION =============

TARGET_ROLES = [
    "CEO", "Managing Director", "Chief Executive Officer",
    "COO", "Chief Operating Officer", "Head of Operations",
    "CTO", "Chief Technology Officer",
    "Head of Credit", "Credit Manager",
    "Chief Customer Officer", "Head of Customer Experience", "Customer Service Manager",
    "Head of Marketing", "Marketing Manager",
]

# MUCH LONGER DELAYS - helps avoid detection
MIN_DELAY = 20
MAX_DELAY = 40
BATCH_SIZE = 5
BATCH_BREAK = 300

ORGANIZATIONS = [
    "Mtoni Lutheran Church SACCOS",
    "Rukwa Farmers' Cooperative Society",
    "Same Kaya SACCOS",
    "Trias Tanzania",
    "Uwezeshaji SACCOS",
    "Opportunity for Social and Economic Progressive (OSEPO)",
    "Pamoja Entrepreneurship Support for Community Development (PESCODE)",
    "Tanzania Network of Religious Leaders Living with or Personally Affected by HIV and AIDS (TANERELA)",
    "Tanzania VICOBA Microfinance Ltd",
]

RESULTS_DIR = "selenium_dork_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============= FUNCTIONS =============

def load_progress():
    progress_file = os.path.join(RESULTS_DIR, "progress.json")
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            data = json.load(f)
            if "fully_processed_orgs" not in data:
                data["fully_processed_orgs"] = []
            if "partially_processed_orgs" not in data:
                data["partially_processed_orgs"] = {}
            if "processed_roles" not in data:
                data["processed_roles"] = {}
            return data
    return {"fully_processed_orgs": [], "partially_processed_orgs": {}, "processed_roles": {}}

def save_progress(fully_processed, partially_processed, processed_roles):
    progress = {
        "fully_processed_orgs": fully_processed,
        "partially_processed_orgs": partially_processed,
        "processed_roles": processed_roles,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(os.path.join(RESULTS_DIR, "progress.json"), 'w') as f:
        json.dump(progress, f, indent=2)

def extract_names_from_text(text):
    if not text:
        return []
    names = []
    pattern1 = r'(?:CEO|COO|CTO|Director|Manager|Head|Executive)[:\s]+([A-Z][a-z]+ [A-Z][a-z]+)'
    names.extend(re.findall(pattern1, text, re.IGNORECASE))
    
    pattern2 = r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'
    names.extend(re.findall(pattern2, text))
    
    pattern3 = r'(?:Mr\.|Ms\.|Mrs\.|Dr\.)\s+([A-Z][a-z]+ [A-Z][a-z]+)'
    names.extend(re.findall(pattern3, text))
    
    unique_names = list(dict.fromkeys(names))
    return unique_names[:3]

def search_organization(driver, org_name, role, wait):
    query = f'"{role}" "{org_name}" Tanzania -job -vacancy -intern'
    results = []
    
    try:
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(4, 8))
        
        page_source = driver.page_source.lower()
        if "captcha" in page_source or "unusual traffic" in page_source:
            print(f"\n  CAPTCHA DETECTED! Solve it in the browser, then press ENTER...")
            input()
            driver.refresh()
            time.sleep(5)
        
        result_blocks = []
        
        selectors_to_try = [
            ("div[data-sokoban-container]", "modern data attribute"),
            ("div.Gx5Zad", "div with Gx5Zad class"),
            ("div.g", "classic div.g"),
            ("article", "article tag"),
        ]
        
        for selector, description in selectors_to_try:
            result_blocks = driver.find_elements(By.CSS_SELECTOR, selector)
            if result_blocks:
                print(f"       Found {len(result_blocks)} results using: {description}")
                break
        
        if not result_blocks:
            print(f"        No results found with any selector.")
            return results
        
        for block in result_blocks[:5]:
            try:
                title = None
                title_selectors = ["h3", "h2", ".BNeawe"]
                for sel in title_selectors:
                    try:
                        title_elem = block.find_element(By.CSS_SELECTOR, sel)
                        title = title_elem.text
                        if title:
                            break
                    except:
                        continue
                
                if not title:
                    continue
                
                link = "N/A"
                try:
                    link_elem = block.find_element(By.CSS_SELECTOR, "a")
                    link = link_elem.get_attribute("href")
                except:
                    pass
                
                snippet = ""
                snippet_selectors = ["div.VwiC3b", ".BNeawe.deIvCb", ".s"]
                for sel in snippet_selectors:
                    try:
                        snippet_elem = block.find_element(By.CSS_SELECTOR, sel)
                        snippet = snippet_elem.text
                        if snippet:
                            break
                    except:
                        continue
                
                full_text = (title + " " + snippet).strip()
                extracted_names = extract_names_from_text(full_text)
                
                if extracted_names:
                    result = {
                        'organization': org_name,
                        'search_role': role,
                        'title': title[:100],
                        'url': link,
                        'snippet': snippet[:500],
                        'extracted_names': ','.join(extracted_names),
                        'timestamp': datetime.now().isoformat()
                    }
                    results.append(result)
                    print(f"      ✓ Found: {', '.join(extracted_names)}")
            
            except Exception as e:
                continue
    
    except Exception as e:
        print(f"       Error: {str(e)[:80]}")
    
    return results

def save_results(results):
    if not results:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    contacts_file = os.path.join(RESULTS_DIR, f"contacts_{timestamp}.csv")
    pd.DataFrame(results).to_csv(contacts_file, index=False)
    
    master_file = os.path.join(RESULTS_DIR, "all_contacts_master.csv")
    if os.path.exists(master_file):
        pd.DataFrame(results).to_csv(master_file, mode='a', header=False, index=False)
    else:
        pd.DataFrame(results).to_csv(master_file, index=False)
    
    print(f"  Saved {len(results)} contacts")

def main():
    print("=" * 70)
    print(" SELENIUM DORKING SCRIPT - FALLBACK VERSION (Regular Selenium)")
    print("=" * 70)
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Roles per organization: {len(TARGET_ROLES)}")
    print(f"\n  Using longer delays ({MIN_DELAY}-{MAX_DELAY}s) to avoid detection")
    print("  A browser window will open. Solve CAPTCHAs when they appear.")
    print("   Press ENTER after solving each CAPTCHA.\n")
    
    input("Press ENTER to start...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Add user agent to look more like a real browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    
    try:
        driver.get("https://www.google.com")
        time.sleep(3)
        
        progress = load_progress()
        fully_processed = set(progress.get("fully_processed_orgs", []))
        partially_processed = progress.get("partially_processed_orgs", {})
        processed_roles = progress.get("processed_roles", {})
        
        all_contacts = []
        
        for idx, org in enumerate(ORGANIZATIONS):
            if org in fully_processed:
                print(f"\n [{idx + 1}/{len(ORGANIZATIONS)}] {org} - SKIPPING (already completed)")
                continue
            
            print(f"\n [{idx + 1}/{len(ORGANIZATIONS)}] {org}")
            
            org_processed_roles = set(processed_roles.get(org, []))
            roles_to_search = [r for r in TARGET_ROLES if r not in org_processed_roles]
            
            if not roles_to_search:
                fully_processed.add(org)
                save_progress(list(fully_processed), partially_processed, processed_roles)
                continue
            
            org_contacts = []
            
            for role in roles_to_search:
                print(f"   {role}")
                results = search_organization(driver, org, role, wait)
                
                if results:
                    org_contacts.extend(results)
                    all_contacts.extend(results)
                
                org_processed_roles.add(role)
                processed_roles[org] = list(org_processed_roles)
                save_progress(list(fully_processed), partially_processed, processed_roles)
                
                delay = random.uniform(MIN_DELAY, MAX_DELAY)
                print(f"    Waiting {delay:.0f}s (avoiding detection)")
                time.sleep(delay)
            
            fully_processed.add(org)
            save_progress(list(fully_processed), partially_processed, processed_roles)
            
            print(f"  Completed - Found {len(org_contacts)} contacts")
            
            if len(all_contacts) >= 20:
                save_results(all_contacts)
                all_contacts = []
            
            if (idx + 1) % BATCH_SIZE == 0:
                print(f"\n Long break: {BATCH_BREAK}s (cooling down)")
                time.sleep(BATCH_BREAK)

                print("\n Restarting browser...")
                driver.quit()
                time.sleep(5)
                driver = webdriver.Chrome(options=options)
                wait = WebDriverWait(driver, 15)
                driver.get("https://google.com")
                time.sleep(3)
        
        if all_contacts:
            save_results(all_contacts)
        
        print("\n" + "=" * 70)
        print(" COMPLETE!")
        print(f"Processed: {len(fully_processed)}/{len(ORGANIZATIONS)} organizations")
        print(f"Results: {RESULTS_DIR}/all_contacts_master.csv")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n Interrupted! Progress saved.")
    finally:
        input("\nPress ENTER to close browser...")
        driver.quit()

if __name__ == "__main__":
    main()