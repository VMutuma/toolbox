from bs4 import BeautifulSoup
import html
import logging
from scraper.utils import clean_text

def parse_glossary(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    base_url = "https://www.infobip.com/glossary"
    glossary_data = []

    glossary_entries = soup.find_all("div", {"role": "button"})

    logging.info(f"Found {len(glossary_entries)} glossary entries")

    for entry in glossary_entries:
        term_tag = entry.find("p")
        term_name = clean_text(term_tag.get_text(strip=True)) if term_tag else "N/A"

        # Get corresponding section for each term using aria controls
        section_id = entry.get("aria-controls")
        section = soup.find("section", {"id": section_id}) if section_id else None

        #Get Definition
        definition_tag = section.find("p") if section else None
        term_definition = clean_text(definition_tag.get_text(strip=True)) if definition_tag else "N/A"

        # Extract link
        link_tag = section.find("a", href=True) if section else None
        term_link = link_tag["href"] if link_tag else "N/A"

        # Convert relative link to absolute URL
        if term_link.startswith("/"):
            term_link = base_url + term_link

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
