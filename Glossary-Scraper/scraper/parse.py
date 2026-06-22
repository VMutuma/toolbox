from bs4 import BeautifulSoup
import html
import logging
from scraper.utils import clean_text

def parse_glossary(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    sections = soup.find_all("section", id=True)
    logging.info(f"Found {len(sections)} sections to scrape.")

    base_url = "https://www.twilio.com"  #all links should be absolute
    glossary_data = []

    for section in sections:
        term_tag = section.find("h3")
        link_tag = term_tag.find("a") if term_tag else None
        definition_tag = section.find("p")

        term_name = clean_text(term_tag.get_text(strip=True)) if term_tag else "N/A"

        term_link = link_tag["href"] if link_tag else "N/A"
        
        # Convert relative link to absolute URL
        if term_link.startswith("/"):
            term_link = base_url + term_link

        term_definition = clean_text(definition_tag.get_text(strip=True)) if definition_tag else "N/A"

        term_name = html.unescape(term_name)
        term_link = html.unescape(term_link)
        term_definition = html.unescape(term_definition)

        glossary_data.append({
            "term": term_name,
            "link": term_link,
            "definition": term_definition
        })

    return glossary_data
