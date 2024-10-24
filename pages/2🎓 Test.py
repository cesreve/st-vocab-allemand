import streamlit as st
import pandas as pd
import random


############################
# 1. Charger et préparer les données
# Remplacez 'votre_dataset.csv' par le nom de votre fichier
df = pd.read_csv('data2.csv')  
categories = df["Category"].unique()  
subcategories = df["Subcategory"].unique()

# --- Sidebar ---
with st.sidebar:
    st.header("Filtres")
    # --- Filter Available Categories ---
    selected_categories = st.multiselect(
        "Categories",
        df["Category"].unique(),
        default=None,
        key="selected_categories",
    )
    available_subcategories = df.loc[df["Category"].isin(selected_categories), "Subcategory"].unique()
    selected_subcategories = st.multiselect('Sous-categories', available_subcategories, default=None)
# --- Filter DataFrame ---
if not len(selected_categories)>0 and not len(available_subcategories)>0:
    st.warning("Please select at least one category or subcategory.")
    filtered_df = pd.DataFrame(columns=df.columns)  # Empty DataFrame
else:
    filtered_df = df[
        (df["Category"].isin(selected_categories))
        & (df["Subcategory"].isin(selected_subcategories))
    ].copy()
#######################################
mots_francais = df['French'].tolist()
mots_allemands = df['Allemand'].tolist()
vocabulaire = dict(zip(mots_francais, mots_allemands))
#######################################
def on_change_callback():
    """This function will be called when the text input's value changes."""
    print(vocabulaire[st.session_state.mot_francais])
    if st.session_state.input_text == vocabulaire[st.session_state.mot_francais]:
        st.success('Bien joué!', icon="✅")
        st.session_state.answers.append(st.session_state.input_text)
        st.session_state.questions.append(st.session_state.mot_francais)
    else:
        st.error('À réviser!', icon="🚨")
        st.session_state.answers.append(st.session_state.input_text)
        st.session_state.questions.append(st.session_state.mot_francais)

# Initialize session state
if "mot_francais" not in st.session_state:
    st.session_state.mot_francais = ""
if "mot_allemand" not in st.session_state:
    st.session_state.mot_allemand = ""
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "answers" not in st.session_state:
    st.session_state.answers = []
if "questions" not in st.session_state:
    st.session_state.questions = []

# 2. Initialiser les compteurs de bonnes/mauvaises réponses
if 'bonnes_reponses' not in st.session_state:
    st.session_state.bonnes_reponses = 0
if 'mauvaises_reponses' not in st.session_state:
    st.session_state.mauvaises_reponses = 0

# 3. Fonction pour choisir un mot français aléatoire
def choisir_mot():
    return random.choice(mots_francais)

# Reset button
if st.button("Nouveau mot", type="secondary", icon="💥"):
    st.session_state.mot_francais = choisir_mot()
    st.session_state.input_text = ""
    st.write("Entrez la traduction en allemand (ß):")
    st.write(st.session_state.mot_francais)
    st.text_input("Enter some text:", key="input_text", on_change=on_change_callback)
    

if st.button("Nouvelle session", type="primary"):
    st.session_state.answers = []
    st.session_state.questions = []

# Create a dataframe from session state data
df_answers = pd.DataFrame({
    "Question (Français)": st.session_state.questions,
    "Réponse de l'utilisateur": st.session_state.answers,
})

# Add a column to indicate correct/incorrect answers
df_answers["Correct ?"] = df_answers["Question (Français)"].apply(lambda x: vocabulaire.get(x)) == df_answers["Réponse de l'utilisateur"]

# Display the dataframe
st.dataframe(df_answers)
