import psycopg2
import streamlit as st

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
