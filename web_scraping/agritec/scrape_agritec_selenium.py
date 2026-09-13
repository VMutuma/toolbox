from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')

# Initialize the driver
print("Starting browser...")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Load the directory page
    print("Loading directory page...")
    driver.get("https://www.agritecafrica.com/directory/")
    
    # Wait longer for page to load
    time.sleep(5)
    
    # Try multiple possible selectors for exhibitor links
    print("Looking for exhibitor links...")
    
    # First, let's see what's actually on the page
    page_title = driver.title
    print(f"Page title: {page_title}")
    
    # Try different selectors
    selectors_to_try = [
        "a[href*='/participate/']",
        ".elementor-widget-heading a",
        ".e-loop-item a",
        ".elementor-loop-grid a",
        "h2 a",
        ".elementor-heading-title a"
    ]
    
    exhibitor_links = []
    for selector in selectors_to_try:
        links = driver.find_elements(By.CSS_SELECTOR, selector)
        if links:
            print(f"  Found {len(links)} links with selector: {selector}")
            exhibitor_links = links
            break
    
    if not exhibitor_links:
        # If still no links, let's check the page source for any links
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute('href')
            if href and '/participate/' in href:
                exhibitor_links.append(link)
        
        if exhibitor_links:
            print(f"  Found {len(exhibitor_links)} participate links by scanning all links")
    
    if not exhibitor_links:
        # Save the page source for debugging
        with open('debug_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("No exhibitor links found! Saved page source to debug_page_source.html")
        print("Please check if you can see the exhibitor grid when visiting the page manually.")
        exit()
    
    # Extract URLs
    urls = []
    for elem in exhibitor_links:
        url = elem.get_attribute('href')
        if url and '/participate/' in url:
            urls.append(url)
    
    # Remove duplicates
    urls = list(dict.fromkeys(urls))
    print(f"\n✅ Found {len(urls)} unique exhibitor URLs")
    
    if len(urls) > 0:
        print("First few URLs:")
        for url in urls[:5]:
            print(f"  {url}")
    
    # Now scrape each exhibitor page
    all_data = []
    
    for i, url in enumerate(urls):
        print(f"\n[{i+1}/{len(urls)}] Scraping: {url}")
        
        try:
            driver.get(url)
            time.sleep(2)  # Wait for page to load
            
            # Extract data
            data = {
                'company_name': '',
                'address': '',
                'website': '',
                'facebook': '',
                'instagram': '',
                'linkedin': '',
                'description': '',
                'profile_url': url
            }
            
            # Company Name
            try:
                name_elem = driver.find_element(By.CSS_SELECTOR, "h1.elementor-heading-title, h1.entry-title, h1")
                data['company_name'] = name_elem.text.strip()
                print(f"    Name: {data['company_name'][:50]}")
            except:
                print("    Could not find company name")
            
            # Address - try multiple approaches
            try:
                # Method 1: Look for specific address pattern
                address_items = driver.find_elements(By.CSS_SELECTOR, ".elementor-icon-list-items .elementor-icon-list-item")
                for item in address_items:
                    try:
                        icon = item.find_element(By.CSS_SELECTOR, "i")
                        icon_class = icon.get_attribute('class')
                        if 'map-marker' in icon_class or 'location' in icon_class:
                            text_elem = item.find_element(By.CSS_SELECTOR, ".elementor-icon-list-text")
                            data['address'] = text_elem.text.strip()
                            print(f"    Address: {data['address'][:50]}...")
                            break
                    except:
                        continue
            except:
                pass
            
            # If address not found, try other patterns
            if not data['address']:
                try:
                    address_elem = driver.find_element(By.CSS_SELECTOR, "[class*='address'], [class*='location']")
                    data['address'] = address_elem.text.strip()
                except:
                    pass
            
            # Social links and website
            try:
                social_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='facebook'], a[href*='instagram'], a[href*='linkedin'], a[href*='http']")
                for link in social_links:
                    href = link.get_attribute('href')
                    if href:
                        if 'facebook.com' in href:
                            data['facebook'] = href
                        elif 'instagram.com' in href:
                            data['instagram'] = href
                        elif 'linkedin.com' in href:
                            data['linkedin'] = href
                        elif 'http' in href and not any(x in href for x in ['facebook', 'instagram', 'linkedin', 'twitter']):
                            if data['website'] == '':
                                data['website'] = href
            except:
                pass
            
            # Description
            try:
                desc_selectors = [".elementor-widget-theme-post-content", ".entry-content", ".post-content", "article .content"]
                for selector in desc_selectors:
                    desc_elem = driver.find_elements(By.CSS_SELECTOR, selector)
                    if desc_elem:
                        data['description'] = desc_elem[0].text.strip()
                        if data['description']:
                            print(f"    Description length: {len(data['description'])} chars")
                            break
            except:
                pass
            
            all_data.append(data)
            
        except Exception as e:
            print(f"    ERROR: {e}")
            all_data.append({
                'company_name': 'ERROR',
                'address': '',
                'website': '',
                'facebook': '',
                'instagram': '',
                'linkedin': '',
                'description': f'Failed to scrape: {e}',
                'profile_url': url
            })
    
    # Save to CSV
    if all_data:
        output_file = 'agritec_exhibitors_full.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['company_name', 'address', 'website', 'facebook', 'instagram', 'linkedin', 'description', 'profile_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"\n Done! Saved {len(all_data)} exhibitors to {output_file}")
    else:
        print("\n No data was collected!")

finally:
    driver.quit()