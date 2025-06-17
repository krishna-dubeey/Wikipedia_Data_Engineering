import requests
import pandas as pd
from lxml import html
from bs4 import BeautifulSoup
import time
import re
import logging
import os
from utils.constants import START_YEAR,END_YEAR,PROCESSED_PATH

# Set up logging
logging.basicConfig(filename='movie_scraper_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Basic genre keyword list (expanded)
GENRE_KEYWORDS = [
    'action', 'drama', 'comedy', 'thriller', 'romance', 'romantic', 'horror',
    'biographical', 'biography', 'dance', 'historical', 'musical', 'fantasy',
    'mystery', 'crime', 'sci-fi', 'science fiction', 'adventure', 'family',
    'sports', 'war', 'political', 'memoir', 'anthology', 'masala', 'documentary',
    'animation', 'psychological', 'rom-com', 'superhero'
]

# List of month names and abbreviations to exclude
MONTH_NAMES = {
    'jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april',
    'may', 'jun', 'june', 'jul', 'july', 'aug', 'august', 'sep', 'september',
    'oct', 'october', 'nov', 'november', 'dec', 'december'
}


def clean_text(text):
    """Remove Wikipedia citations, backlinks, and extra whitespace."""
    text = re.sub(r'\[\d+\]', '', text)  # Remove [1], [2], etc.
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
    return text.strip()


def get_movie_summary(url, max_retries=3):
    """Fetch and clean the first valid sentence from a Wikipedia page, handling abbreviations and parenthetical text."""
    for attempt in range(max_retries):
        try:
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            paragraphs = soup.select("div.mw-parser-output > p")

            for para in paragraphs:
                text = clean_text(para.text.strip())
                if text and len(text.split()) > 10:  # Ensure paragraph is substantial
                    # Split on periods, but exclude those in abbreviations or parentheses
                    sentences = re.split(r'(?<!\btransl)(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bDr)\.\s+(?![^\(]*\))', text)
                    sentences = [s.strip() for s in sentences if s.strip()]
                    if sentences:
                        first_sentence = sentences[0]
                        # Ensure the sentence is meaningful (e.g., > 5 words)
                        if len(first_sentence.split()) > 5:
                            return first_sentence + '.'  # Add period for proper punctuation
                        # If first sentence is too short, try the next one
                        elif len(sentences) > 1 and len(sentences[1].split()) > 5:
                            return sentences[1] + '.'
                        # Fallback to full paragraph if no valid sentence
                        return text

            logging.warning(f"No valid summary found for {url}")
            return "Summary not available"
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == max_retries - 1:
                return "Error fetching summary"
            time.sleep(2 ** attempt)  # Exponential backoff
    return "Error fetching summary"


def get_movie_genre(url):
    """Attempt to extract genre from infobox or summary."""
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Try infobox first
        infobox = soup.select_one("table.infobox")
        if infobox:
            genre_row = infobox.find("th", string=re.compile("Genre", re.I))
            if genre_row:
                genre_text = genre_row.find_next("td").text.lower()
                found_genres = [genre for genre in GENRE_KEYWORDS if genre in genre_text]
                if found_genres:
                    return ', '.join(found_genres)

        # Fallback to summary
        summary = get_movie_summary(url)
        summary_lower = summary.lower()
        found_genres = [genre for genre in GENRE_KEYWORDS if genre in summary_lower]
        return ', '.join(found_genres) if found_genres else 'Unknown'
    except Exception as e:
        logging.error(f"Failed to fetch genre for {url}: {e}")
        return 'Unknown'


def scrape_movie_summaries(start_year:int=START_YEAR, end_year:int=END_YEAR):
    base_url = 'https://en.wikipedia.org/w/api.php'
    all_movies = []

    for year in range(start_year, end_year + 1):
        print(f"Scraping year {year}...")
        logging.info(f"Scraping year {year}")
        page_name = f'List_of_Hindi_films_of_{year}'
        params = {
            'action': 'parse',
            'format': 'json',
            'page': page_name,
            'prop': 'text',
            'redirects': ''
        }

        try:
            response = requests.get(base_url, params=params, timeout=15)
            response.raise_for_status()
            raw_html = response.json()['parse']['text']['*']
        except Exception as e:
            logging.error(f"Failed to fetch Wikipedia page for {year}: {e}")
            print(f"Failed to fetch page for {year}: {e}")
            continue

        try:
            doc = html.fromstring(raw_html)
            tables = doc.xpath('//table[contains(@class, "wikitable")]')

            for table_idx, table in enumerate(tables):
                try:
                    rows = table.xpath('.//tr')[1:]  # Skip header
                    for row_idx, row in enumerate(rows):
                        # Try multiple columns for title/link
                        cells = row.xpath('.//td')
                        movie_title = None
                        relative_url = None

                        # Search for the first cell with a link or plain text
                        for cell_idx, cell in enumerate(cells):
                            # Try to find a link first
                            link = cell.xpath('.//a')
                            if link and link[0].text_content().strip():
                                movie_title = link[0].text_content().strip()
                                relative_url = link[0].get('href')
                                break
                            # If no link, try plain text in the first column
                            elif cell_idx == 0:  # Only consider the first column for plain text
                                text = cell.text_content().strip()
                                # Validate: not a month, not a number, reasonable length, and preferably multi-word
                                if (text and not text.isdigit() and len(text) > 2 and
                                        text.lower() not in MONTH_NAMES and len(text.split()) > 1):
                                    movie_title = text
                                    relative_url = None
                                    break

                        if movie_title:
                            if relative_url:
                                full_url = f"https://en.wikipedia.org{relative_url}"
                                summary = get_movie_summary(full_url)
                                genre = get_movie_genre(full_url)
                            else:
                                full_url = "Unknown"
                                summary = "No Wikipedia page available"
                                genre = "Unknown"

                            all_movies.append({
                                'Title': movie_title,
                                'Year': year,
                                'Summary': summary,
                                'Genre': genre
                            })
                            logging.info(f"Successfully scraped: {movie_title} ({year})" +
                                         ("" if relative_url else " [No link]"))
                        else:
                            logging.warning(
                                f"Skipped row {row_idx} in table {table_idx} for {year}: No valid title found")

                    time.sleep(1)  # Short delay between tables
                except Exception as e:
                    logging.error(f"Error processing table {table_idx} for {year}: {e}")
                    continue

        except Exception as e:
            logging.error(f"Error parsing tables for {year}: {e}")
            print(f"Error parsing tables for {year}: {e}")
            continue

        time.sleep(2)  # Delay between years

    df = pd.DataFrame(all_movies)
    output_file = os.path.join(PROCESSED_PATH,f"genre_combined_hindi_films.csv")
    df.to_csv(output_file, index=False)
    print(f"✅ All movie summaries and genres saved to {output_file}")
    #logging.info(f"Saved {len(all_movies)} movies to {output_file}")


# Run it
#scrape_movie_summaries(2019, 2019)