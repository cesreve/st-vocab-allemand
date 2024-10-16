# French-German Vocabulary App

This is a simple Streamlit web application that helps you learn and practice French-German vocabulary. It loads vocabulary data from a CSV file (`data.csv`) and provides a user-friendly interface for browsing, filtering, and listening to the words and phrases.

## Features

- **Filter vocabulary:** Filter words and phrases by category and subcategory.
- **Listen to pronunciation:** Hear the German pronunciation of each word or phrase using text-to-speech.
- **Show/Hide columns:** Choose to display French, German, or both columns.
- **Control the number of words:** Use a slider to adjust the number of vocabulary items displayed.

## How to Use

1. **Install Streamlit:** If you don't have Streamlit installed, run `pip install streamlit`.
2. **Data File:** Make sure you have a CSV file named `data.csv` in the same directory as the app script (`app.py`). The CSV file should have the following columns:
    - **Category:** The main category of the vocabulary.
    - **Subcategory:** A more specific subcategory within the main category.
    - **French:** The French word or phrase.
    - **Allemand:** The German translation of the French word or phrase.
3. **Run the app:** Open your terminal, navigate to the directory containing `app.py`, and run `streamlit run app.py`.
4. **Use the filters:** Select the desired categories and subcategories from the sidebar to filter the vocabulary list.
5. **Listen and learn:** Click the play button in the "Listen" column to hear the German pronunciation of each word or phrase.
6. **Customize the display:** Use the checkboxes to show or hide the French and German columns. Adjust the slider to control the number of words displayed.

## Data File Format

The `data.csv` file should be a comma-separated value file with the following columns:

| Category | Subcategory | French | Allemand |
|---|---|---|---|
| Greetings | Basic | Bonjour | Guten Tag |
| Greetings | Formal | Bonsoir | Guten Abend |
| ... | ... | ... | ... |

## Future Improvements

- Add more languages.
- Implement spaced repetition for more effective learning.
- Allow users to create and save their own vocabulary lists.
- Make the app mobile-friendly.
