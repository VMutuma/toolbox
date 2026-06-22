import html
import logging
import re

def setup_logging(log_file="scraper.log"):
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def clean_text(text):
    """Cleans extracted text by removing extra dashes, spaces, and decoding HTML entities."""
    text = html.unescape(text)
    text = re.sub(r"\s*-\s*", " ", text)
    # Remove everything after "We all do sometimes"
    text = re.split(r'We all do sometimes', text, flags=re.IGNORECASE)[0]
    text = re.split(r'Copyright ', text, flags=re.IGNORECASE)[0]
    text = text.strip()
    return text
