import streamlit as st
import pandas as pd
import random
######
st.set_page_config(page_title="Vocabulaire Allemand", page_icon=":de:", layout="centered")


# 1. Charger et préparer les données
# Remplacez 'votre_dataset.csv' par le nom de votre fichier
df = pd.read_csv('data.csv')  

############
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
###########
mots_francais = df['French'].tolist()
mots_allemands = df['Allemand'].tolist()
vocabulaire = dict(zip(mots_francais, mots_allemands))

# 2. Initialiser les compteurs de bonnes/mauvaises réponses
if 'bonnes_reponses' not in st.session_state:
    st.session_state.bonnes_reponses = 0
if 'mauvaises_reponses' not in st.session_state:
    st.session_state.mauvaises_reponses = 0

# 3. Fonction pour choisir un mot français aléatoire
def choisir_mot():
    return random.choice(mots_francais)

# 4. Bouton pour générer une nouvelle question
if st.button("Nouvelle question"):
    st.session_state.mot_actuel = choisir_mot()

# 5. Afficher un mot français (seulement si un mot est sélectionné)
if 'mot_actuel' in st.session_state:
    st.write("Mot français :", st.session_state.mot_actuel)
    st.session_state.reponse = "" 

    # 6. Zone de saisie pour la réponse de l'utilisateur
    reponse_utilisateur = st.text_input("Entrez la traduction en allemand (ß):", value=None)

    # 7. Bouton de validation et vérification de la réponse
    if st.button("Valider"):
        if reponse_utilisateur == vocabulaire[st.session_state.mot_actuel]:
            st.session_state.bonnes_reponses += 1
            st.success("Correct !")
        else:
            st.session_state.mauvaises_reponses += 1
            st.error(f"Incorrect. La bonne réponse est : {vocabulaire[st.session_state.mot_actuel]}")
        st.session_state.reponse = "" 
        st.session_state.mot_actuel = choisir_mot() # Choisir un nouveau mot

# 8. Afficher le compteur de bonnes/mauvaises réponses
st.write("Bonnes réponses :", st.session_state.bonnes_reponses)
st.write("Mauvaises réponses :", st.session_state.mauvaises_reponses)