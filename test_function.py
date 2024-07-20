import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_sortables_local import sort_items

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
st.set_page_config(
    layout="wide",
)

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

# client = MongoClient("mongodb://localhost:27017")
# db = client["location"]
# collection = db["location"]

genre_select = st.multiselect("Select Genres", genres, key="genres")

if genre_select:
    query = {"genres": {"$all": genre_select}}
    mongo_results = list(collection.find(query))

    for index, result in enumerate(mongo_results, start=1):
        result["order"] = index
        data.append(result["name"])

items = [
    {'header': 'location_results', 'items': data},
    # rộng hơn, thêm time dựa trên order
    # alt sol: clone git
    {'header': 'planner_results', 'items': []},
]

sorted_items = sort_items(items, multi_containers=True, direction="vertical")
# st.write(sorted_items, unsafe_allow_html=True)