import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state='collapsed')


st.write("# Welcome to Hue! 👋")

st.sidebar.success("Select a trip.")

st.sidebar.header("Location Result")

st.markdown("Location Result")
interests = [
    "architecture", 
    "art", 
    "culture", 
    "heritage", 
    "history",
    "market",
    "museum",
    "nature",
    "wellness",
    "ruin",
    "workshop"
]

moods = [
    "roadtrip", 
    "vintage", 
    "romantic", 
    "spiritual", 
    "city explorer",
    "shopping",
    "photography",
    "beach-loving",
    "sightseeing",
    "cuisine",
    "relax",
    "entertain",
    "memorial"
]

select_col1, select_col2 = st.columns(2)

with select_col1:
    interests_select = st.multiselect("What is your interest", interests, key="interests")

with select_col2:
    moods_select = st.multiselect("Your moods", moods, key="moods")

cfirm_btn = st.button("Okela")

if cfirm_btn:
    st.session_state["interests_select"] = interests_select
    st.session_state["moods_select"] = moods_select
    st.session_state["is_interests"] = True if len(interests_select) > 0 else False
    st.session_state["is_moods"] = True if len(moods_select) > 0 else False
    st.experimental_set_query_params(page="locations")
    st.switch_page("pages/locations.py")