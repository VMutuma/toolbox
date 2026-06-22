import requests
import logging
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_html(url, headers=None):
    """Fetches HTML content from a given URL"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch {url}: {e}")
        return None

def auto_detect_glossary(html, base_url):
    """Automatically detects glossary terms and their links from a given HTML page"""
    soup = BeautifulSoup(html, "html.parser")
    glossary_terms = []

    # Check for headings with links (e.g., <h2><a href="...">Term</a></h2>)
    for tag in soup.find_all(["h2", "h3", "h4", "li"]):
        link = tag.find("a")
        if link and link.get_text(strip=True):
            term_name = link.get_text(strip=True)
            term_link = link["href"]

            # Convert relative links to absolute
            if term_link.startswith("/"):
                term_link = base_url.rstrip("/") + term_link

            glossary_terms.append({
                "term": term_name,
                "link": term_link
            })

    # If no terms found, check for table-based glossaries
    if not glossary_terms:
        for row in soup.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) >= 2:  # Assuming first column is the term, second is the definition
                term_name = columns[0].get_text(strip=True)
                term_link = columns[0].find("a")["href"] if columns[0].find("a") else "N/A"

                # Convert relative links to absolute
                if term_link.startswith("/"):
                    term_link = base_url.rstrip("/") + term_link

                glossary_terms.append({
                    "term": term_name,
                    "link": term_link
                })

    logging.info(f"Detected {len(glossary_terms)} glossary terms")
    return glossary_terms

if __name__ == "__main__":
    # Example site with a glossary
    url = "https://www.infobip.com/glossary"
    headers = {"User-Agent": "Mozilla/5.0"}

    html_content = fetch_html(url, headers)
    if html_content:
        glossary_terms = auto_detect_glossary(html_content, url)
        for term in glossary_terms[:10]:  # Print first 10 terms for verification
            print(term)
