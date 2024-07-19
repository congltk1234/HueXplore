import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide")

st.markdown("Location Result")
st.sidebar.header("Location Result")
st.title("Grid Location")

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

client = MongoClient("mongodb://localhost:27017")
db = client["location"]
collection = db["main_loc"]

select_col1, select_col2 = st.columns(2)

with select_col1:
    interests_select = st.multiselect("What is your interest", interests, key="interests")

with select_col2:
    mood_select = st.multiselect("Your moods", moods, key="moods")

cfirm_btn = st.button("Confirm Selected Items")

mongo_results = []

query = {}
if interests_select:
    query["interests"] = {"$all": interests_select}
if mood_select:
    query["moods"] = {"$all": mood_select}

names_res, img_res, coor_res, address_res = [], [], [], []

if interests_select or mood_select:
    mongo_results = list(collection.find(query))

    for index, result in enumerate(mongo_results, start=1):
        result["order"] = index
        names_res.append(result["name"])
        img_res.append(result["img_url"])
        coor_res.append(result["coordinate"])
        address_res.append(result["address"])


df = pd.DataFrame({
    "name": names_res,
    "img": img_res,
    "coordinate": coor_res,
    "address": address_res
    })

selected_names = []
selected_items = []

def display_location_grid(df):
    card_height = 200
    num_columns = 5
    num_rows = len(df)

    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):
            name = item['name']
            img = item['img']
            with col:
                checkbox_value = st.checkbox(name, key=name)

                if checkbox_value:
                    if name not in selected_names:
                        selected_names.append(name)
                        selected_items.append(item)
                elif name in selected_names:
                    selected_names.remove(name)
                    selected_items.remove(item)


                col.markdown(f"""
                        <div style="border: 2px solid #000; padding: 10px; border-radius: 10px; background-color: #fff; height: {card_height}px; display: flex; justify-content: center; align-items: center;">
                            <img src="{img}" style="max-width: 215px; min-height: 150px; max-height: 150px;">
                        </div>
                """, unsafe_allow_html=True)

                
display_location_grid(df)  

if selected_items:
    if cfirm_btn:
        st.session_state["selected_names"] = selected_names
        st.session_state["selected_items"] = selected_items
        st.experimental_set_query_params(page="planner")
