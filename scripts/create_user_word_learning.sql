CREATE TABLE IF NOT EXISTS user_word_learning (
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    compteur INT DEFAULT 1,
    derniere_date_mise_a_jour TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, word_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (word_id) REFERENCES words(word_id)
);