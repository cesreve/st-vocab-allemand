import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO
from database import get_words, get_categories_and_subcategories

##################################
st.set_page_config(page_title="Vocabulaire Allemand", page_icon=":de:", layout="centered")
##################################
# --- Helper Function for TTS ---
@st.cache_data
def get_audio_base64(text):
    tts = gTTS(text=text, lang='de') 
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    b64 = base64.b64encode(fp.read()).decode()
    return f'<audio controls src="data:audio/mpeg;base64,{b64}"/>'

# --- Streamlit App ---
st.title(':flag-fr: Français-Allemand :flag-de:')

st.write("Sélectionner au moins une catégorie ou sous-catégorie.")

if 'username' in st.session_state:
    if len(st.session_state.username)>0:
        st.write(f"Vous êtes authenthifié en tant que {st.session_state.username}!")  

# --- Sidebar ---
with st.sidebar:
    st.header("Filtres")
    df_categories = get_categories_and_subcategories()
    selected_categories = st.multiselect("Categories", df_categories['category'].tolist(), key="categories")

    available_subcategories = []
    if selected_categories:
        subcategories_filtered = df_categories[df_categories['category'].isin(selected_categories)]['subcategories'].unique()
        available_subcategories = list(set(', '.join(subcategories_filtered).split(', '))) if subcategories_filtered.size > 0 else []
    selected_subcategories = st.multiselect("Subcategories", available_subcategories, key="subcategories")

    if st.button("Load data"):
        st.session_state.filtered_df = get_words(selected_categories, selected_subcategories)
    else:
        st.warning("Sélectionner au moins une catégorie ou sous-catégorie pour charger les données.")
        st.stop()

# --- Rename columns ---
filtered_df = st.session_state.filtered_df.rename(columns={
    'category': 'Catégorie',
    'subcategory': 'Sous-catégorie',
    'french_word': 'Français',
    'german_word': 'Allemand',
    'example_sentence': 'Exemple'
})

# --- Add TTS Column ---
filtered_df.loc[:, 'Écouter'] = filtered_df['Allemand'].apply(get_audio_base64)

# --- Display DataFrame with HTML for Audio ---
if not filtered_df.empty:
    filtered_df = filtered_df.sample(frac=1).reset_index(drop=True)
    st.write(
        filtered_df[['Français', 'Allemand', 'Écouter', 'Exemple']].to_html(
            escape=False, formatters={"Écouter": lambda x: x}, index=False
        ),
        unsafe_allow_html=True,
    )