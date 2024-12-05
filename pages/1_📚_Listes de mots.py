import streamlit as st
import pandas as pd
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

if 'username' in st.session_state:
    if len(st.session_state.username)>0:
        st.write(f"Vous êtes authenthifié en tant que {st.session_state.username}!")

# --- Initial Values for Filters and Checkbox ---
if "show_french" not in st.session_state:
    st.session_state.show_french = True

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

filtered_df = get_words(selected_categories, selected_subcategories)

# --- Rename columns ---
filtered_df = filtered_df.rename(columns={
    'category': 'Catégorie',
    'subcategory': 'Sous-catégorie',
    'french_word': 'Français',
    'german_word': 'Allemand',
    'example_sentence': 'Exemple'
})

# --- Add TTS Column --- (unchanged)
filtered_df.loc[:, 'Écouter'] = filtered_df['Allemand'].apply(get_audio_base64)

# --- Show/Hide Columns ---
col1, col2 = st.columns(2)
with col1:
    show_allemand = st.checkbox('Montrer Allemand', value=True)
with col2:
    show_french = st.checkbox('Montrer Français', value=st.session_state.show_french)

columns_to_show = ['Catégorie', 'Sous-catégorie', 'Écouter', 'Exemple'] 
if show_french and not show_allemand:
    columns_to_show = ['Français', 'Écouter'] 
if show_allemand and not show_french:
    columns_to_show = ['Allemand', 'Écouter', 'Exemple'] 
if show_allemand and show_french:
    columns_to_show = ['Français', 'Allemand', 'Écouter', 'Exemple'] 

# --- Slider ---
if len(filtered_df) > 0:
    num_words = st.slider('Nombre de mots', min_value=1, max_value=len(filtered_df), value=5)
    displayed_df = filtered_df[columns_to_show].head(num_words)

# --- Display DataFrame with HTML for Audio ---
if not filtered_df.empty:
    st.write(
        displayed_df.to_html(
            escape=False, formatters={"Écouter": lambda x: x}
        ),
        unsafe_allow_html=True,
    )