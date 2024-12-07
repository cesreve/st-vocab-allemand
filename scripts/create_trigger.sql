-- Fonction pour mettre à jour la table user_learning
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

-- Create tigger for updateing the user_word_learning function
CREATE TRIGGER update_user_word_learning_trigger
AFTER INSERT ON answers
FOR EACH ROW
EXECUTE PROCEDURE update_user_word_learning();
