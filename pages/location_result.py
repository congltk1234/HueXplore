import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide")

st.markdown("Location Result")
st.sidebar.header("Location Result")
st.title("Grid Location")

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

data = []

client = MongoClient("mongodb://localhost:27017")
db = client["location"]
collection = db["location"]

genre_select = st.multiselect("Select Genres", genres, key="genres")

if genre_select:
    query = {"genres": {"$all": genre_select}}
    mongo_results = list(collection.find(query))

    for index, result in enumerate(mongo_results, start=1):
        result["order"] = index
        data.append(result["name"])


df = pd.DataFrame(list(data), columns=['Name'])

selected_items = []

def display_location_grid(df):
    card_height = 200
    num_columns = 5
    num_rows = len(df)

    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):
            name = item['Name']
            with col:
                checkbox_value = st.checkbox(name, key=name)
                if checkbox_value:
                    if name not in selected_items:
                        selected_items.append(name)
                elif name in selected_items:
                    selected_items.remove(name)

                col.markdown(f"""
                        <div style="border: 2px solid #000; padding: 10px; border-radius: 10px; background-color: #fff; height: {card_height}px; display: flex; justify-content: center; align-items: center;">
                            <img src="https://file1.dangcongsan.vn/data/0/images/2024/04/11/upload_673/hue-imperial-gate-1024x683-754-17016811818591749547652.png" style="max-width: 215px; min-height: 150px; max-height: 150px;">
                        </div>
                """, unsafe_allow_html=True)

display_location_grid(df)  

if selected_items:
    st.write("location_result")
    st.write(selected_items)