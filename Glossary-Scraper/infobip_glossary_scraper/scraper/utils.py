import html
import logging
import re
from collections import Counter

def setup_logging(log_file="scraper.log"):
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

def clean_text(text):
    """Cleans extracted text by removing extra dashes, spaces, decoding HTML entities, and removing redundant content."""
    text = html.unescape(text)
    text = re.sub(r"\s*-\s*", " ", text)
    text = text.strip()

    # Remove duplicate paragraphs
    paragraphs = text.split("\n")
    seen_paragraphs = set()
    unique_paragraphs = []
    
    for para in paragraphs:
        para_clean = re.sub(r'\s+', ' ', para.strip())  # Normalize spaces
        if para_clean and para_clean.lower() not in seen_paragraphs:
            seen_paragraphs.add(para_clean.lower())
            unique_paragraphs.append(para_clean)

    text = "\n".join(unique_paragraphs)

    # Remove duplicate sentences while preserving order
    seen_sentences = set()
    sentences = []
    for sentence in re.split(r'(?<=[.!?])\s+', text):  # Split by sentence-ending punctuation
        sentence_clean = sentence.strip()
        if sentence_clean.lower() not in seen_sentences:
            seen_sentences.add(sentence_clean.lower())
            sentences.append(sentence_clean)

    text = " ".join(sentences).strip()

    return text
