from bs4 import BeautifulSoup
import logging
import html
from scraper.utils import clean_text

def parse_term_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract Term Title
    title_tag = soup.find("h2")
    title = clean_text(title_tag.get_text(strip=True)) if title_tag else "N/A"
    
    # Extract Sections and Content
    sections = {}
    current_section = None
    
    for tag in soup.find_all(["h2", "p"]):
        if tag.name == "h2":
            current_section = clean_text(tag.get_text(strip=True))
            sections[current_section] = []
        elif tag.name == "p" and current_section:
            sections[current_section].append(clean_text(tag.get_text(strip=True)))
    
    # Unescape HTML entities
    title = html.unescape(title)
    sections = {html.unescape(k): [html.unescape(v) for v in vals] for k, vals in sections.items()}
    
    logging.info(f"Extracted title: {title}, {len(sections)} sections found.")
    
    return {
        "title": title,
        "sections": sections
    }
