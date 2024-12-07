CREATE TABLE IF NOT EXISTS words (
    word_id SERIAL PRIMARY KEY,
    french_word TEXT,
    german_word TEXT,
    category TEXT,
    subcategory TEXT,
    example_sentence TEXT
);