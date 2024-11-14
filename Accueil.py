import streamlit as st


st.set_page_config(page_title="Vocabulaire Allemand", page_icon=":de:", layout="centered")

st.title("Bienvenue sur l'application de vocabulaire français-allemand !")

st.write("""
Cette application web simple vous aide à apprendre et à pratiquer le vocabulaire français-allemand. 
Elle charge les données de vocabulaire à partir d'un fichier CSV (`data.csv`) et fournit une interface conviviale 
pour parcourir, filtrer et écouter les mots et les phrases.
""")

st.header("Fonctionnalités")
st.markdown("""
- **Filtrer le vocabulaire :** Filtrez les mots et les phrases par catégorie et sous-catégorie.
- **Écouter la prononciation :** Écoutez la prononciation allemande de chaque mot ou expression à l'aide de la synthèse vocale.
- **Afficher/Masquer les colonnes :** Choisissez d'afficher les colonnes français, allemand ou les deux.
- **Contrôler le nombre de mots :** Utilisez un curseur pour ajuster le nombre d'éléments de vocabulaire affichés.
""")

st.write("Commencez votre apprentissage dès aujourd'hui !")
