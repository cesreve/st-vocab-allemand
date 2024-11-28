import psycopg2

def create_trigger_and_function(conn):
    """
    Creates the trigger and function in PostgreSQL to update user_word_learning.

    Args:
        conn: psycopg2 connection object.
    """
    try:
        cursor = conn.cursor()

        # Create the function
        function_sql = """
        CREATE OR REPLACE FUNCTION update_user_word_learning()
        RETURNS TRIGGER AS $$
        BEGIN
          -- Vérifier si la réponse est correcte
          IF NEW.is_correct THEN
            -- Si la réponse est correcte, incrémenter le compteur
            UPDATE user_word_learning
            SET compteur = compteur + 1,
                derniere_date_mise_a_jour = NOW()
            WHERE user_id = NEW.user_id AND word_id = NEW.word_id;

            -- Si aucune ligne correspondante n'existe, en insérer une nouvelle
            IF NOT FOUND THEN
              INSERT INTO user_word_learning (user_id, word_id, compteur, derniere_date_mise_a_jour)
              VALUES (NEW.user_id, NEW.word_id, 1, NOW());
            END IF;
          ELSE
            -- Si la réponse est incorrecte, réinitialiser le compteur à 0
            UPDATE user_word_learning
            SET compteur = 0,
                derniere_date_mise_a_jour = NOW()
            WHERE user_id = NEW.user_id AND word_id = NEW.word_id;

            -- Si aucune ligne correspondante n'existe, en insérer une nouvelle
            IF NOT FOUND THEN
              INSERT INTO user_word_learning (user_id, word_id, compteur, derniere_date_mise_a_jour)
              VALUES (NEW.user_id, NEW.word_id, 0, NOW());
            END IF;
          END IF;

          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
        cursor.execute(function_sql)

        # Create the trigger
        trigger_sql = """
        CREATE TRIGGER update_user_word_learning_trigger
        AFTER INSERT ON answers
        FOR EACH ROW
        EXECUTE PROCEDURE update_user_word_learning();
        """
        cursor.execute(trigger_sql)

        conn.commit()
        print("Trigger and function created successfully!")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        conn.rollback()

    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    # Database connection parameters
    conn_params = {
        'host': 'your_host',
        'database': 'your_database',
        'user': 'your_user',
        'password': 'your_password'
    }

    try:
        conn = psycopg2.connect(**conn_params)
        create_trigger_and_function(conn)

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")

    finally:
        if conn:
            conn.close()