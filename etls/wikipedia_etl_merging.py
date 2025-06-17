import os
from utils.constants import PROCESSED_PATH

def merging_csv(folder_path: str=PROCESSED_PATH):
    import pandas as pd
    # Load both CSV files
    file_path = os.path.join(folder_path, "combined_hindi_films.csv")
    file_path1 = os.path.join(folder_path, "genre_combined_hindi_films.csv")
    df1 = pd.read_csv(file_path)     # e.g., scraped movie table: Title, Cast, Director, Genre, Year
    df2 = pd.read_csv(file_path1)    # e.g., scraped summaries: Title, Year, Summary, Genre, Wiki Link

    # Normalize titles and years for safe matching
    df1['Title'] = df1['Title'].str.strip().str.lower()
    df2['Title'] = df2['Title'].str.strip().str.lower()

    #df1['Year'] = df1['Year'].astype(int).str.strip()
    #df2['Year'] = df2['Year'].astype(int).str.strip()

    # Merge based on Title and Year
    merged_df = pd.merge(df1, df2[['Title', 'Genre']],
                     on='Title',
                     how='left',
                     suffixes=('_df1', '_df2'))

    # If Genre in df1 is missing or "NA", use Genre from df2
    merged_df['Genre'] = merged_df.apply(
        lambda row: row['Genre_df2'] if pd.isna(row['Genre_df1']) or row['Genre_df1'] in ['NA', '', 'Unknown'] else row['Genre_df1'], axis=1
    )

    # Drop intermediate genre columns and rename
    merged_df.drop(['Genre_df2'], axis=1, inplace=True)

    # Reorder columns
    final_cols = merged_df[['Title', 'Movie_Cast', 'Director', 'Genre', 'Year']]
    existing_cols = [col for col in final_cols if col in merged_df.columns]
    merged_df = merged_df[existing_cols]
    # Save the merged file
    output_file = os.path.join(folder_path, "merged_movies_with_genre.csv")
    merged_df.to_csv(output_file, index=False)
    print("✅ Merged CSV saved as 'merged_movies_with_genre.csv'")
