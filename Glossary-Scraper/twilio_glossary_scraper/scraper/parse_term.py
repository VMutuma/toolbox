from bs4 import BeautifulSoup
import logging
import html
from scraper.utils import clean_text

def parse_term_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract Header
    header_tag = soup.find("h1")
    header = clean_text(header_tag.get_text(strip=True)) if header_tag else "N/A"

    # Extract Paragraphs
    paragraphs = [clean_text(p.get_text(strip=True)) for p in soup.find_all("p")]

    # Unescape HTML entities
    header = html.unescape(header)
    paragraphs = [html.unescape(p) for p in paragraphs]

    if not paragraphs:
        logging.warning(f"No paragraphs found for header: {header}")

    logging.info(f"Extracted header: {header}, {len(paragraphs)} paragraphs found.")

    return {
        "header": header,
        "paragraphs": paragraphs
    }
