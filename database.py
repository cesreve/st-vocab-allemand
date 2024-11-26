import psycopg2
import streamlit as st
import pandas as pd
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

def fetch_answers_from_db(user_id):
    """Récupère les réponses de l'utilisateur depuis la base de données."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT german_word, answer_date, is_correct
            FROM (
                SELECT 
                    german_word, 
                    answer_date, 
                    is_correct,
                    RANK() OVER (PARTITION BY german_word ORDER BY answer_date DESC) as rank_number
                FROM answers
                WHERE user_id = %s
            ) AS ranked_answers
            WHERE 1=1
                AND rank_number = 1
                AND is_correct;
                    """, (user_id,))
        answers_data = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df_answers = pd.DataFrame(answers_data, columns=columns)
        cur.close()
        conn.close()
        return df_answers
    except psycopg2.Error as e:
        st.error(f"Erreur de base de données: {e}")
        return None
    
def update_user_word_learning(conn, user_id, word_id):
    """Met à jour la table 'user_word_learning' avec la réponse de l'utilisateur.
    Args:
    user_id: L'ID de l'utilisateur.
    word_id: L'ID du mot.
    """
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        update_query = """
        INSERT INTO user_word_learning (user_id, word_id) 
        VALUES (%s, %s)
        ON CONFLICT (user_id, word_id) 
        DO UPDATE SET compteur = user_word_learning.compteur + 1, 
                        derniere_date_mise_a_jour = CURRENT_TIMESTAMP;
        """
        cursor.execute(update_query, (user_id, word_id))
        conn.commit()
        print(f"Table 'user_word_learning' mise à jour pour user_id: {user_id}, word_id: {word_id}")

    except (Exception, psycopg2.Error) as error:
        print(f"Erreur lors de la mise à jour de la table: {error}")

    finally:
        if conn:
            cursor.close()
            conn.close  