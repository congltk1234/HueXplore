import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_sortables_local import sort_items


st.set_page_config(page_title="Tourism Planner", page_icon="🌍", layout="wide")
st.markdown("Tourism Planner")
st.sidebar.header("Tourism Planner")

st.title("Planner")

data = []

genres = [
    "architecturalmonument", 
    "art", 
    "architecture", 
    "nature", 
    "culture",
    "history",
    "historicalsites",
    "museums"
]

client = MongoClient("mongodb://localhost:27017")
db = client["location"]
collection = db["location"]





col1, col2 = st.columns(2)

with col1:
    genre_select = st.multiselect("Select Genres", genres, key="genres")

    if genre_select:
        query = {"genres": {"$all": genre_select}}
        mongo_results = list(collection.find(query))

        for index, result in enumerate(mongo_results, start=1):
            result["order"] = index
            data.append(result["name"])

    items = [
        {'header': 'location_results', 'items': data},
        {'header': 'planner_results', 'items': []},
    ]   
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

with col2:
    st.markdown("### Map")