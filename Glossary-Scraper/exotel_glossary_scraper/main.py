from bs4 import BeautifulSoup
import html
from scraper.utils import clean_text, setup_logging
from scraper.fetch import fetch_html, fetch_term_page
from scraper.save import save_to_csv, csv_to_json
from scraper.save_word import save_to_word
from scraper.parse import parse_glossary

setup_logging()

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
    
    
    return {
        "title": title,
        "sections": sections
    }


def main():
    url = "https://www.exotel.com/glossary"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    csv_filename = "Exotel_glossary.csv"
    json_filename = "Exotel_glossary.json"
    word_filename = "Exotel_glossary.docx"
        
    html_content = fetch_html(url, headers)
    glossary_data = parse_glossary(html_content)
    
    for entry in glossary_data:
        if entry["link"] != "N/A":
            term_html = fetch_term_page(entry["link"], headers)
            if term_html:
                term_details = parse_term_page(term_html)
                entry.update(term_details)
            else:
                entry.update({"title": "N/A", "sections": {}})
        else:
            entry.update({"title": "N/A", "sections": {}})
    
    save_to_csv([[d["term"], d["link"], d["definition"], d["title"], " | ".join([f"{k}: {' '.join(v)}" for k, v in d["sections"].items()])] for d in glossary_data], csv_filename)
    
    csv_to_json(csv_filename, json_filename)
    
    save_to_word(glossary_data, word_filename)
        
if __name__ == "__main__":
    main()
