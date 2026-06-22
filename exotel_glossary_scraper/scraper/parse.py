from bs4 import BeautifulSoup
import html
import logging
from scraper.utils import clean_text

def parse_glossary(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    glossary_data = []
    
    glossary_entries = soup.find_all("div", class_="glossary-content-box")
    logging.info(f"Found {len(glossary_entries)} glossary entries")
    
    for entry in glossary_entries:
        # Extract term
        term_tag = entry.find("h4")
        term_name = clean_text(term_tag.get_text(strip=True)) if term_tag else "N/A"
        
        # Extract definition
        definition_tag = entry.find("p")
        term_definition = clean_text(definition_tag.get_text(" ", strip=True)) if definition_tag else "N/A"
        
        # Extract link
        link_tag = entry.find("a", href=True)
        term_link = link_tag["href"] if link_tag else "N/A"
        
        # Unescape HTML entities
        term_name = html.unescape(term_name)
        term_link = html.unescape(term_link)
        term_definition = html.unescape(term_definition)
        
        glossary_data.append({
            "term": term_name,
            "link": term_link,
            "definition": term_definition
        })
    
    return glossary_data
