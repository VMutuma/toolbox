import html
import logging
import re

def setup_logging(log_file="scraper.log"):
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def clean_text(text):
    text = html.unescape(text)
    text = re.sub(r"\s*-\s*", " ", text)
        # Remove '... Read more' and any variation like '… ... Read more'
    text = re.sub(r'…\s*\.\.\.\s*Read more', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\.\.\.\s*Read more', '', text, flags=re.IGNORECASE)
    
    # Remove everything after "Keep exploring"
    text = re.split(r'Keep exploring', text, flags=re.IGNORECASE)[0]
    text = text.strip()
    return text