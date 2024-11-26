import psycopg2

def create_user_word_learning_table(conn):
  """Crée la table 'user_word_learning' dans la base de données PostgreSQL.

  Args:
    conn: Un objet de connexion psycopg2 à la base de données.
  """
  try:
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_word_learning (
        user_id INT NOT NULL,
        word_id INT NOT NULL,
        compteur INT DEFAULT 1,
        derniere_date_mise_a_jour TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id)
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'user_word_learning' créée avec succès.")

  except (Exception, psycopg2.Error) as error:
    print(f"Erreur lors de la création de la table: {error}")

  finally:
    if conn:
      cursor.close()