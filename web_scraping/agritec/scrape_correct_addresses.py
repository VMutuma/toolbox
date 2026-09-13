from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)

# Get all exhibitor links
driver.get("https://www.agritecafrica.com/directory/")
time.sleep(5)

exhibitor_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/participate/']")
urls = list(dict.fromkeys([link.get_attribute('href') for link in exhibitor_links if link.get_attribute('href')]))
print(f"Found {len(urls)} exhibitors")

all_data = []

for i, url in enumerate(urls):
    print(f"\n[{i+1}/{len(urls)}] Processing...")
    
    try:
        driver.get(url)
        time.sleep(2)
        
        data = {
            'company_name': '',
            'company_address': '',
            'venue_address': '',
            'organizer_address': '',
            'website': '',
            'facebook': '',
            'instagram': '',
            'linkedin': '',
            'description': '',
            'profile_url': url
        }
        
        # Company Name
        try:
            name_elem = driver.find_element(By.CSS_SELECTOR, "h1.elementor-heading-title")
            data['company_name'] = name_elem.text.strip()
            print(f"  Name: {data['company_name'][:40]}")
        except:
            pass
        
        # Find ALL map-marker addresses
        address_items = driver.find_elements(By.CSS_SELECTOR, ".elementor-icon-list-items .elementor-icon-list-item")
        
        address_count = 0
        for item in address_items:
            try:
                icon = item.find_element(By.CSS_SELECTOR, "i")
                icon_class = icon.get_attribute('class')
                if 'fa-map-marker-alt' in icon_class:
                    text_elem = item.find_element(By.CSS_SELECTOR, ".elementor-icon-list-text")
                    address_text = text_elem.text.strip()
                    address_count += 1
                    
                    if address_count == 1:
                        # First address is the venue
                        data['venue_address'] = address_text
                    elif address_count == 2:
                        # Second address is the COMPANY address
                        data['company_address'] = address_text
                        print(f"  Company Address: {address_text[:60]}...")
                    elif address_count == 3:
                        # Third address is the organizer
                        data['organizer_address'] = address_text
            except:
                continue
        
        # Social links and website
        try:
            social_links = driver.find_elements(By.CSS_SELECTOR, ".elementor-icon-list-items.elementor-inline-items .elementor-icon-list-item a")
            for link in social_links:
                href = link.get_attribute('href')
                if href:
                    if 'facebook.com' in href:
                        data['facebook'] = href
                    elif 'instagram.com' in href:
                        data['instagram'] = href
                    elif 'linkedin.com' in href:
                        data['linkedin'] = href
                    elif 'http' in href and not any(x in href for x in ['facebook', 'instagram', 'linkedin']):
                        if not data['website']:
                            data['website'] = href
                            if data['website']:
                                print(f"  Website: {href}")
        except:
            pass
        
        # Description
        try:
            desc_elem = driver.find_element(By.CSS_SELECTOR, ".elementor-widget-theme-post-content")
            data['description'] = desc_elem.text.strip()[:500]
            if data['description']:
                print(f"  Description: {len(data['description'])} chars")
        except:
            pass
        
        all_data.append(data)
        
    except Exception as e:
        print(f"  ERROR: {e}")
        all_data.append({'company_name': 'ERROR', 'profile_url': url})

driver.quit()

# Save to CSV
output_file = 'agritec_company_addresses.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['company_name', 'company_address', 'venue_address', 'organizer_address', 'website', 'facebook', 'instagram', 'linkedin', 'description', 'profile_url']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

# Print summary
companies_with_address = sum(1 for d in all_data if d['company_address'])
print(f"\n✅ Saved to {output_file}")
print(f"   Total companies: {len(all_data)}")
print(f"   Companies with address found: {companies_with_address}")