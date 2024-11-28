import pandas as pd
import streamlit as st
import psycopg2  # PostgreSQL adapter

DATABASE_URL = st.secrets["my_database"]["DATABASE_URL"]

def insert_words_to_db(csv_file, db_url):
    """Inserts data from a CSV file into a PostgreSQL database."""
    try:
        # Establish database connection
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Iterate over DataFrame rows and insert into the database
        for index, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO words (french_word, german_word, category, subcategory, example_sentence)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    row["French"],
                    row["Allemand"],
                    row["Category"],
                    row["Subcategory"],
                    row["Phrase"],
                ),
            )

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        print("Data insertion successful.")

    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting data: {error}")



# csv_file = "data.csv"  # Replace with your CSV file path
csv_file = "/Users/cclave/projets/st-vocab-allemand/data.csv"
insert_words_to_db(csv_file, DATABASE_URL)


