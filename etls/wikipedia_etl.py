import os
import time
import pandas as pd
import requests
from lxml import html
from utils.constants import OUTPUT_PATH,START_YEAR,END_YEAR,PROCESSED_PATH

def connect_wikipedia(year: int):
    subject = f'List_of_Hindi_films_of_{year}'
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'parse',
        'format': 'json',
        'page': subject,
        'prop': 'text',
        'redirects': ''
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['parse']['text']['*']
    except Exception:
        return None

def extract_yearly_tables(start_year: int=START_YEAR,end_year: int=END_YEAR,output_dir: str=OUTPUT_PATH):
    os.makedirs(output_dir, exist_ok=True)

    for year in range(start_year,end_year + 1):
        raw_html = connect_wikipedia(year)
        if not raw_html:
            continue

        try:
            document = html.fromstring(raw_html)
            tables = document.xpath('//table[contains(@class, "wikitable")]')
            yearly_dfs = []

            for idx, table in enumerate(tables):
                try:
                    df = pd.read_html(html.tostring(table, encoding='unicode'))[0]
                    df['Year'] = year
                    df['Table_Number'] = idx + 1
                    yearly_dfs.append(df)
                except Exception:
                    continue

            if yearly_dfs:
                year_df = pd.concat(yearly_dfs, ignore_index=True)
                output_path = os.path.join(output_dir, f"hindi_films_{year}.csv")
                year_df.to_csv(output_path, index=False)

        except Exception:
            continue

        time.sleep(3)  # polite delay

def transform_yearly_data(input_folder: str = OUTPUT_PATH) -> pd.DataFrame:
    combined_df = pd.DataFrame()

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(input_folder, file_name)
            try:
                df = pd.read_csv(file_path)
                df.columns = [col.lower().strip() for col in df.columns]

                selected = pd.DataFrame()
                selected['Title'] = df.get('title', pd.Series(["NA"] * len(df)))
                selected['Movie_Cast'] = df.get('cast', pd.Series(["NA"] * len(df)))
                selected['Director'] = df.get('director', pd.Series(["NA"] * len(df)))
                selected['Genre'] = df.get('genre', pd.Series(["NA"] * len(df)))
                selected['Year'] = df.get('year', pd.Series(["NA"] * len(df)))

                selected.fillna("NA", inplace=True)
                combined_df = pd.concat([combined_df, selected], ignore_index=True)
            except Exception:
                continue

    return combined_df

#pip freeze >requirements.txt

# -------------------- LOAD --------------------

def load_combined_data_to_csv(df, path=os.path.join(PROCESSED_PATH,f"combined_hindi_films.csv")):
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Final combined DataFrame shape: {df.shape}")


