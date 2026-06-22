import requests
import json
import csv
import base64
import time
import re
import os 
from dotenv import load_dotenv 
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# WordPress API
WP_API_COLLECTION_URL = "https://*****************" 
WP_API_UPDATE_URL_BASE = "https://*****************" 

WP_USERNAME = os.getenv("WP_USERNAME")
WP_APPLICATION_PASSWORD = os.getenv("WP_APPLICATION_PASSWORD")

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key=GEMINI_API_KEY)
GEMINI_MODEL = genai.GenerativeModel('models/gemini-1.5-flash-latest') 

# File paths
INPUT_CSV_FILE = "Glossary_Low_Word_Count.csv"
OUTPUT_LOG_FILE = "glossary_update_log.txt"

# --- Authentication Headers for WordPress ---
if not WP_USERNAME or not WP_APPLICATION_PASSWORD:
    raise ValueError("WordPress username or application password not found in environment variables. Please check your .env file.")

wp_credentials = f"{WP_USERNAME}:{WP_APPLICATION_PASSWORD}"
wp_encoded_credentials = base64.b64encode(wp_credentials.encode()).decode()
wp_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {wp_encoded_credentials}"
}

# --- Functions (remain the same as before) ---

def get_glossary_term_details_by_slug(slug):
    """
    Fetches a glossary term's ID, title, and content using its slug via WP REST API.
    Returns (id, title_rendered, content_rendered) or (None, None, None) on failure.
    """
    params = {"slug": slug, "per_page": 1}
    try:
        response = requests.get(WP_API_COLLECTION_URL, headers=wp_headers, params=params, timeout=10)
        response.raise_for_status()
        terms = response.json()
        if terms:
            term = terms[0]
            return (
                term.get("id"),
                term.get("title", {}).get("rendered", ""),
                term.get("content", {}).get("rendered", ""),
                term.get("excerpt", {}).get("rendered", "")
            )
        else:
            return None, None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching details for slug '{slug}': {e}")
        return None, None, None, None

def extract_slug_from_url(url):
    """Extracts the slug from a typical WordPress glossary URL."""
    match = re.search(r'/glossary/([^/]+)/?$', url)
    if match:
        return match.group(1)
    return None

def expand_text_with_gemini(term_title, original_content, original_excerpt, target_word_count=600):
    """
    Sends text to Gemini API for expansion and contextualization.
    """
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables. Cannot call Gemini API.")
        return None, None

    combined_original_text = f"Title: {term_title}\n\nExcerpt: {original_excerpt}\n\nFull Definition:\n{original_content}"

    prompt = f"""
    You are an expert SEO content writer for a business glossary for a company named Beem.
    Your task is to expand and re-write the following glossary term definition.
    Provide a detailed, professional, and comprehensive explanation that is suitable for a business/telecommunications/tech audience.
    Where possible add internal and external links but under no circumstances should you link to competitors..
    
    **Glossary Term:** {term_title}
    **Current Definition and Context:**
    {combined_original_text}

    **Instructions:**
    1.  **Expand and enrich** the definition significantly, aiming for approximately {target_word_count} words for the main content.
    2.  **Contextualize** the term within a business/telecommunications/tech environment, given Beem's focus.
    3.  **Include relevant sub-sections** like "How it Works," "Benefits," "Use Cases," "Key Features," or "Challenges" if applicable, using <h4> headings.
    4.  Maintain a **professional, informative, and clear tone**.
    5.  Use **proper HTML formatting** for paragraphs (`<p>...</p>`), headings (`<h4>...</h4>`), ordered lists (`<ol><li>...</li></ol>`), and unordered lists (`<ul><li>...</ul>`).
    6.  Ensure the new content is **more detailed and comprehensive** than the original.
    7.  Do not introduce irrelevant information or repeat the term excessively.
    8.  Generate a new, concise **excerpt** (around 20-30 words) from the expanded content. The excerpt should also be in HTML `<p>...</p>` tags.
    9.  Provide the output in a JSON object with two keys: `full_content_html` and `excerpt_html`.
    10. **IMPORTANT:** Ensure the output is PURE JSON, without any markdown code block fences (like ```json or ```).
    """
    
    try:
        response = GEMINI_MODEL.generate_content(prompt)
        
        if response._result.candidates[0].finish_reason == 4:
            print(f"Gemini API blocked content for '{term_title}' due to safety reasons.")
            return None, None
        
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[len("```json"):].strip()
        if response_text.endswith("```"):
            response_text = response_text[:-len("```")].strip()

        try:
            gemini_output = json.loads(response_text)
            return gemini_output.get("full_content_html"), gemini_output.get("excerpt_html")
        except json.JSONDecodeError:
            print(f"Gemini API response for '{term_title}' was not valid JSON after stripping. Raw response: {response.text[:200]}... Processed: {response_text[:200]}...")
            return response_text, None 
            
    except Exception as e:
        print(f"Error calling Gemini API for '{term_title}': {e}")
        return None, None
def update_wordpress_term(term_id, new_content, new_excerpt):
    """
    Updates a glossary term in WordPress via REST API.
    """
    update_url = f"{WP_API_UPDATE_URL_BASE}{term_id}"
    payload = {
        "content": new_content,
        "excerpt": new_excerpt,
        "status": "publish", 
        "type": "glossary" 
    }

    try:
        response = requests.post(update_url, headers=wp_headers, data=json.dumps(payload))
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        print(f"Error updating WP term ID {term_id}: HTTP {e.response.status_code} - {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error updating WP term ID {term_id}: {e}")
        return False

# --- Main Script Logic ---
if __name__ == "__main__":
    if not all([WP_USERNAME, WP_APPLICATION_PASSWORD, GEMINI_API_KEY]):
        print("ERROR: One or more required environment variables (WP_USERNAME, WP_APPLICATION_PASSWORD, GEMINI_API_KEY) are not set.")
        print("Please ensure your .env file is correctly configured in the same directory as the script.")
        exit()

    successful_updates = 0
    failed_updates = 0
    
    log_messages = []

    print("Starting glossary term expansion and update process...")

    try:
        with open(INPUT_CSV_FILE, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            if 'Url' not in csv_reader.fieldnames:
                print(f"Error: Input CSV file must contain a 'Url' column.")
                log_messages.append(f"Error: Input CSV file must contain a 'Url' column.")
                exit()
            
            for i, row in enumerate(csv_reader):
                term_url = row['Url'].strip()

                # Filter for glossary URLs only
                if "/glossary/" not in term_url:
                    msg = f"Skipping row {i+2}: Not a glossary URL ({term_url})."
                    print(msg)
                    log_messages.append(msg)
                    continue

                slug = extract_slug_from_url(term_url)
                if not slug:
                    msg = f"Skipping row {i+2}: Could not extract slug from URL ({term_url})."
                    print(msg)
                    log_messages.append(msg)
                    failed_updates += 1
                    continue
                
                print(f"\nProcessing URL: {term_url} (Slug: {slug})")

                # 1. Fetch term details (ID, title, content) from WP API using slug
                term_id, term_title, original_content, original_excerpt = get_glossary_term_details_by_slug(slug)
                
                if not term_id:
                    msg = f"Could not find term ID for slug '{slug}'. Skipping update for {term_url}."
                    print(msg)
                    log_messages.append(msg)
                    failed_updates += 1
                    continue
                
                if not original_content:
                    msg = f"Term ID {term_id} (Slug: {slug}) has no original content. Skipping Gemini expansion."
                    print(msg)
                    log_messages.append(msg)
                    failed_updates += 1
                    continue
                
                print(f"Fetched term '{term_title}' (ID: {term_id}). Original content length: {len(original_content)} chars.")

                # 2. Expand text with Gemini
                expanded_content, expanded_excerpt = expand_text_with_gemini(term_title, original_content, original_excerpt)
                
                if not expanded_content:
                    msg = f"Gemini API failed to generate expanded content for '{term_title}' (ID: {term_id}). Skipping update."
                    print(msg)
                    log_messages.append(msg)
                    failed_updates += 1
                    continue
                
                if expanded_excerpt is None:
                    expanded_excerpt = original_excerpt
                    print(f"Warning: Gemini failed to generate excerpt. Using original excerpt for '{term_title}'.")
                
                print(f"Gemini expansion complete. New content length: {len(expanded_content)} chars.")

                # 3. Update WordPress term
                if update_wordpress_term(term_id, expanded_content, expanded_excerpt):
                    successful_updates += 1
                    msg = f"SUCCESS: Updated '{term_title}' (ID: {term_id})."
                    print(msg)
                    log_messages.append(msg)
                else:
                    failed_updates += 1
                    msg = f"FAILED: Update for '{term_title}' (ID: {term_id}). See console for details."
                    print(msg)
                    log_messages.append(msg)
                
                time.sleep(3)

    except FileNotFoundError:
        print(f"Error: Input CSV file not found at '{INPUT_CSV_FILE}'")
        log_messages.append(f"Error: Input CSV file not found at '{INPUT_CSV_FILE}'")
    except Exception as e:
        print(f"An error occurred during script execution: {e}")
        log_messages.append(f"An error occurred during script execution: {e}")

    finally:
        print("\n--- Process Summary ---")
        summary_msg = f"Total successful updates: {successful_updates}\nTotal failed updates: {failed_updates}"
        print(summary_msg)
        log_messages.append(summary_msg)

        with open(OUTPUT_LOG_FILE, mode='w', encoding='utf-8') as log_file:
            log_file.write("\n".join(log_messages))
        print(f"Detailed log saved to '{OUTPUT_LOG_FILE}'")