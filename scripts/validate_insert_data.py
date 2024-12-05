import csv
from typing import List

import psycopg2
from pydantic import BaseModel, ValidationError


# 1. Define your Pydantic model to match the table structure
class Word(BaseModel):
    word_id: int
    french_word: str
    german_word: str
    category: str
    subcategory: str
    example_sentence: str


# 2. Function to read data from CSV and validate it with Pydantic
def read_and_validate_csv(csv_file):
    """
    Reads data from a CSV file and validates each row using the Pydantic model.

    Args:
        csv_file (str): Path to the CSV file.

    Returns:
        List[Word]: A list of validated Word objects.
    """
    valid_data = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                word = Word(**row)  # Validate the row
                valid_data.append(word)
            except ValidationError as e:
                print(f"Validation error for row: {row}")
                print(e)
    return valid_data


# 3. Function to insert data into PostgreSQL
def insert_data_into_db(db_url, data):
    """
    Inserts validated data into the PostgreSQL table.

    Args:
        conn: psycopg2 connection object.
        data (List[Word]): List of validated Word objects.
    """
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    for word in data:
        try:
            insert_query = """
                INSERT INTO words (word_id, french_word, german_word, category, subcategory, example_sentence) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                word.word_id, word.french_word, word.german_word, word.category, word.subcategory,
                word.example_sentence
            ))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()  # Rollback in case of error
    cursor.close()