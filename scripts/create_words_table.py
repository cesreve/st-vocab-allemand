import psycopg2

def create_words_table(db_url):
    """Creates the 'words' table in the PostgreSQL database.

    Args:
        db_url: The URL for connecting to the database.
    """
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Create the words table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS words (
                word_id SERIAL PRIMARY KEY,
                french_word TEXT,
                german_word TEXT,
                category TEXT,
                subcategory TEXT,
                example_sentence TEXT
            );
        """)
        conn.commit()
        print("Table 'words' created successfully.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()