import psycopg2
import streamlit as st
from datetime import datetime

# Get the database URL from environment variable
DATABASE_URL = st.secrets["my_database"]["DATABASE_URL"]

def connect_to_db():
    """Connects to PostgreSQL, creates a table, and queries it."""
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_answer(user_id, german_word, is_correct):
    """Inserts the user's answer into the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create the answers table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                german_word VARCHAR(255) NOT NULL,
                is_correct BOOLEAN,
                answer_date TIMESTAMP
            );
        """)

        # Insert the answer data
        cur.execute("""
            INSERT INTO answers (user_id, german_word, is_correct, answer_date)
            VALUES (%s, %s, %s, %s);
        """, (user_id, german_word, is_correct, datetime.now()))

        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        st.error(f"Database error: {e}")
