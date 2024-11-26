import psycopg2

def create_answers_table(db_url):
    """Creates the 'answers' table in the PostgreSQL database.

    Args:
        db_url: The URL for connecting to the database.
    """
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Create the answers table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                answer_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                word_id INT NOT NULL,
                answer_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
                FOREIGN KEY (user_id) REFERENCES users(user_id),  -- Assuming 'users' table exists
                FOREIGN KEY (word_id) REFERENCES words(word_id) -- Assuming 'words' table exists
            );
        """)
        conn.commit()
        print("Table 'answers' created successfully.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()