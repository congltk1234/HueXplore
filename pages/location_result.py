# import streamlit as st
# from pymongo import MongoClient
# import pandas as pd

# # st.session_state.sidebar_state = 
# st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide",
#                     initial_sidebar_state='collapsed')
# st.sidebar.header("Location Result")

# st.markdown("Location Result")
# st.title("Grid Location")

# interests = [
#     "architecture", "art", "culture", "heritage", "history",
#     "market", "museum", "nature", "wellness", "ruin", "workshop"
# ]

# moods = [
#     "roadtrip", "vintage", "romantic", "spiritual", "city explorer",
#     "shopping", "photography", "beach-loving", "sightseeing",
#     "cuisine", "relax", "entertain", "memorial"
# ]

# client = MongoClient("mongodb://localhost:27017")
# db = client["unihack"]
# collection = db["locations"]

# is_moods = st.session_state["is_moods"]
# is_interests = st.session_state["is_interests"]
# moods_select = st.session_state["moods_select"]
# interests_select = st.session_state["interests_select"]


# mongo_results = []

# query = {}
# if is_interests:
#     query["interests"] = {"$all": interests_select}
# if is_moods:
#     query["moods"] = {"$all": moods_select}

# names_res, img_res, coor_res, ggmap = [], [], [], []

# if interests_select or moods_select:
#     mongo_results = list(collection.find(query))

#     for index, result in enumerate(mongo_results, start=1):
#         result["order"] = index
#         names_res.append(result["name"])
#         img_res.append(result["img_url"])
#         coor_res.append(result["coordinate"])
#         ggmap.append(result["gg_map"])


# df = pd.DataFrame(
#     {
#         "name": names_res,
#         "img": img_res,
#         "coordinate": coor_res,
#         "gg_map": ggmap
#     }
# )

# # Initialize session state for start and end selections
# if "start_location" not in st.session_state:
#     st.session_state["start_location"] = None
# if "end_location" not in st.session_state:
#     st.session_state["end_location"] = None
# if "selecting" not in st.session_state:
#     st.session_state["selecting"] = None

# def select_start():
#     st.session_state["selecting"] = "start"

# def select_end():
#     st.session_state["selecting"] = "end"

# st.button("Start", on_click=select_start)
# st.button("End", on_click=select_end)

# st.write(f"Start: {st.session_state['start_location']}")
# st.write(f"End: {st.session_state['end_location']}")

# def display_location_grid(df):
#     card_height = 200
#     num_columns = 5
#     num_rows = len(df)

#     rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

#     for row in rows:
#         cols = st.columns(num_columns)
#         for col, (index, item) in zip(cols, row.iterrows()):
#             name = item['name']
#             img = item['img']
#             with col:
#                 checkbox_value = st.checkbox(name, key=name)

#                 if checkbox_value:
#                     if st.session_state["selecting"] == "start":
#                         st.session_state["start_location"] = name
#                         st.session_state["selecting"] = None
#                     elif st.session_state["selecting"] == "end":
#                         st.session_state["end_location"] = name
#                         st.session_state["selecting"] = None


#                 col.markdown(f"""
#                         <div style="border: 2px solid #000; padding: 10px; border-radius: 10px; background-color: #fff; height: {card_height}px; display: flex; justify-content: center; align-items: center;">
#                             <img src="{img}" style="max-width: 215px; min-height: 150px; max-height: 150px;">
#                         </div>
#                 """, unsafe_allow_html=True)

                
# display_location_grid(df)

import streamlit as st
from pymongo import MongoClient
import pandas as pd
from fixed_header import st_fixed_container


# Configure page settings
st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide", initial_sidebar_state='collapsed')
st.sidebar.header("Location Result")

st.markdown(
    """
    <div style = "height: 200px">
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
button {
    height: auto;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


interests = [
    "architecture", "art", "culture", "heritage", "history",
    "market", "museum", "nature", "wellness", "ruin", "workshop"
]

moods = [
    "roadtrip", "vintage", "romantic", "spiritual", "city explorer",
    "shopping", "photography", "beach-loving", "sightseeing",
    "cuisine", "relax", "entertain", "memorial"
]

client = MongoClient("mongodb://localhost:27017")
db = client["unihack"]
collection = db["locations"]

is_moods = st.session_state.get("is_moods", False)
is_interests = st.session_state.get("is_interests", False)
moods_select = st.session_state.get("moods_select", [])
interests_select = st.session_state.get("interests_select", [])

mongo_results = []

query = {}
if is_interests:
    query["interests"] = {"$all": interests_select}
if is_moods:
    query["moods"] = {"$all": moods_select}

names_res, img_res, coor_res, ggmap = [], [], [], []

if interests_select or moods_select:
    mongo_results = list(collection.find(query))

    for index, result in enumerate(mongo_results, start=1):
        result["order"] = index
        names_res.append(result["name"])
        img_res.append(result["img_url"])
        coor_res.append(result["coordinate"])
        ggmap.append(result["gg_map"])

df = pd.DataFrame({
    "name": names_res,
    "img": img_res,
    "coordinate": coor_res,
    "gg_map": ggmap
})

# Initialize session state for start and end selections
if "start_location" not in st.session_state:
    st.session_state["start_location"] = None
if "end_location" not in st.session_state:
    st.session_state["end_location"] = None


with st_fixed_container(mode="fixed", position="top", border=True):
    st.title("Grid Location")
    st.write(f"Start: {st.session_state['start_location']}")
    st.write(f"End: {st.session_state['end_location']}")

def display_location_grid(df):
    card_height = 300
    num_columns = 5
    num_rows = len(df)

    rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

    for row in rows:
        cols = st.columns(num_columns)
        for col, (index, item) in zip(cols, row.iterrows()):
            name = item['name']
            img = item['img']
            with col:
                # col.markdown(f"""
                #         <img src="{img}" style="width: {400}px; height: {300}px; object-fit: cover; border-radius: 10px; margin-bottom: 10px;">
                # """, unsafe_allow_html=True)
                col.markdown(f"""
                        <div style="padding: 5px; height: {card_height}px; display: flex; justify-content: left; align-items: left;">
                            <img src="{img}" style="max-width: 350px; min-width: 350px; min-height: 250px; max-height: 250px;">
                        </div>
                """, unsafe_allow_html=True)
                col_start, col_end = st.columns(2)
                # col.markdown(f"""
                #             <p style="width:{400}px; font-size: {20}px; text-align: center">{name}</p>
                # """, unsafe_allow_html=True)
                with col_start:
                    if st.button(f"Set as Start", key=f"start_{name}"):
                        st.session_state["start_location"] = name
                with col_end:
                    if st.button(f"Set as End", key=f"end_{name}"):
                        st.session_state["end_location"] = name

display_location_grid(df)