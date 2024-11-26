import psycopg2

def create_users_table(db_url):
  """Crée une table 'users' dans la base de données PostgreSQL.
  Args:
    conn: Un objet de connexion psycopg2 à la base de données.
  """
  try:
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    # Définition de la requête SQL pour créer la table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """

    # Exécution de la requête
    cursor.execute(create_table_query)

    # Validation des changements
    conn.commit()
    print("Table 'users' créée avec succès.")

  except (Exception, psycopg2.Error) as error:
    print(f"Erreur lors de la création de la table: {error}")

  finally:
    if conn:
      cursor.close()