def wikipedia_pipeline():
    from etls.wikipedia_etl import extract_yearly_tables, transform_yearly_data, load_combined_data_to_csv
    from utils.constants import OUTPUT_PATH, START_YEAR, END_YEAR

    extract_yearly_tables(START_YEAR, END_YEAR, OUTPUT_PATH)
    print("Extraction complete.")

    df = transform_yearly_data(OUTPUT_PATH)
    print(f"Transformation complete. Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    load_combined_data_to_csv(df)
    print("Data loaded successfully.")

def wikipedia_pipeline2():
    from etls.wikipedia_etl2 import scrape_movie_summaries
    from utils.constants import START_YEAR, END_YEAR

    scrape_movie_summaries(START_YEAR, END_YEAR)

def wikipedia_pipeline3():
    from etls.wikipedia_etl_merging import merging_csv
    merging_csv()
