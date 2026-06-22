from scraper.fetch import fetch_html, fetch_term_page
from scraper.parse import parse_glossary
from scraper.parse_term import parse_term_page
from scraper.save import save_to_csv, csv_to_json
from scraper.utils import setup_logging
from scraper.save_word import save_to_word


url = "https://www.infobip.com/glossary"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
csv_filename = "infobip_glossary.csv"
json_filename = "infobip_glossary.json"
word_filename = "infobip_glossary.docx"

setup_logging()

html_content = fetch_html(url, headers)

glossary_data = parse_glossary(html_content)


for entry in glossary_data:
    if entry["link"] != "N/A":
        term_html = fetch_term_page(entry["link"], headers)
        if term_html:
            term_details = parse_term_page(term_html)
            entry.update(term_details)
        else:
            entry.update({"header": "N/A", "paragraphs": []})
    else:
        entry.update({"header": "N/A", "paragraphs": []})


save_to_csv([[d["term"], d["link"], d["definition"], d["header"], " | ".join(d["paragraphs"])] for d in glossary_data], csv_filename)


save_to_csv([[d["term"], d["link"], d["definition"], d["header"], " | ".join(d["paragraphs"])] for d in glossary_data], csv_filename)


csv_to_json(csv_filename, json_filename)

save_to_word(glossary_data, word_filename)