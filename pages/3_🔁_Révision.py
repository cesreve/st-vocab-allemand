import streamlit as st
import pandas as pd
import random
from database import get_words_to_review, get_categories_and_subcategories, insert_answer

# --- User Authentication Check ---
user_id = st.session_state.get("user_id")
if not user_id:
    st.warning("Please log in to view words to review.")
    st.stop()  # Stop execution if not logged in


st.title("Words to Review")

# --- Review Interval ---
review_interval = st.number_input("Review Interval (Days)", min_value=1, value=3, key="review_interval")

# --- Category and Subcategory Selection ---
with st.sidebar:
    st.header("Filtres")
    df_categories = get_categories_and_subcategories()
    selected_categories = st.multiselect("Categories", df_categories['category'].tolist(), key="categories")

    available_subcategories = []
    if selected_categories:
        subcategories_filtered = df_categories[df_categories['category'].isin(selected_categories)]['subcategories'].unique()
        available_subcategories = list(set(', '.join(subcategories_filtered).split(', '))) if subcategories_filtered.size > 0 else []
    selected_subcategories = st.multiselect("Subcategories", available_subcategories, key="subcategories")


# --- Fetch Words to Review ---
words_to_review_df = get_words_to_review(user_id, review_interval, selected_categories, selected_subcategories)

if words_to_review_df is not None and not words_to_review_df.empty:
    # --- Quiz Setup and Interaction ---
    mots_francais = words_to_review_df['french_word'].tolist()
    vocabulaire = dict(zip(mots_francais, words_to_review_df['german_word'].tolist()))
    word_ids = dict(zip(mots_francais, words_to_review_df['word_id'].tolist()))

    if "mot_francais" not in st.session_state:
        st.session_state.mot_francais = random.choice(mots_francais) # Initialize with a random word
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "questions" not in st.session_state:
        st.session_state.questions = []


    def on_change_callback():
        german_word = vocabulaire.get(st.session_state.mot_francais) # Handle potential KeyError
        word_id = word_ids.get(st.session_state.mot_francais) # Handle potential KeyError
        is_correct = st.session_state.input_text == german_word if german_word else False # Handle missing word case

        # Database insertion is done directly here
        insert_answer(user_id, word_id, is_correct)
        
        if is_correct:
             st.success('Bien joué!', icon="✅")
        elif german_word:  # Only show error if the word exists
             st.error('À réviser!', icon="🚨")

        st.session_state.answers.append(st.session_state.input_text)
        st.session_state.questions.append(st.session_state.mot_francais)

        # Choose a new random word after answering
        remaining_words = [word for word in mots_francais if word != st.session_state.mot_francais]
        if remaining_words:
            st.session_state.mot_francais = random.choice(remaining_words)
        else:
            st.warning("All words reviewed!")
        st.rerun()

    st.write(st.session_state.mot_francais)
    st.text_input("Enter some text:", key="input_text", on_change=on_change_callback)



    # --- Display Answers ---
    df_answers = pd.DataFrame({
        "Question (Français)": st.session_state.questions,
        "Réponse de l'utilisateur": st.session_state.answers,
    })
    df_answers["Correct ?"] = df_answers.apply(lambda row: vocabulaire.get(row["Question (Français)"]) == row["Réponse de l'utilisateur"], axis=1)
    st.dataframe(df_answers)


elif words_to_review_df is not None:
    st.write("No words to review based on your selection and review interval.")


