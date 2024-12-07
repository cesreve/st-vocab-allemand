CREATE TABLE IF NOT EXISTS answers (
    answer_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    word_id INT NOT NULL,
    is_correct BOOLEAN,
    answer_date TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() at time zone 'utc'),
    FOREIGN KEY (user_id) REFERENCES users(user_id),  -- Assuming 'users' table exists
    FOREIGN KEY (word_id) REFERENCES words(word_id) -- Assuming 'words' table exists
);