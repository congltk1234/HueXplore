import streamlit as st
from pymongo import MongoClient
import pandas as pd
from fixed_header import st_fixed_container


# Configure page settings
st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide", initial_sidebar_state='collapsed')
st.sidebar.header("Location Result")

st.markdown(
    """
    <div style = "height: 220px">
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

names_res, img_res, coor_res, ggmap_res, interests_res, moods_res = [], [], [], [], [], []

if interests_select or moods_select:
    mongo_results = list(collection.find(query))

    for index, result in enumerate(mongo_results, start=1):
        result["order"] = index
        names_res.append(result["name"])
        img_res.append(result["img_url"])
        coor_res.append(result["coordinate"])
        ggmap_res.append(result["gg_map"])
        interests_res.append(result["interests"])
        moods_res.append(result["moods"])

df = pd.DataFrame({
    "name": names_res,
    "img": img_res,
    "coordinate": coor_res,
    "gg_map": ggmap_res,
    "interests": interests_res,
    "moods": moods_res
})

# Initialize session state for start and end selections
if "origin_point" not in st.session_state:
    st.session_state["origin_point"] = None
if "destination_point" not in st.session_state:
    st.session_state["destination_point"] = None
if "origin_object" not in st.session_state:
    st.session_state["origin_object"] = None
if "destination_object" not in st.session_state:
    st.session_state["destination_object"] = None

point_dict = {
    'point1': 'Đàn Nam Giao',
    'point2': 'Chùa Thiên Mụ',
    'point3': 'Lăng Tự Đức',
}

with st_fixed_container(mode="fixed", position="top", border=True):
    st.title("Grid Location")
    st.markdown(f"""
        <p style = "color: red; font-size: larger; font-weight: 600">Origin: {st.session_state['origin_point']}</p>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(f"""
        <p style = "color: green; font-size: larger; font-weight: 600">Destination: {st.session_state['destination_point']}</p>
    """,
        unsafe_allow_html=True,
    )
    st.write(f"S_Object: {st.session_state['origin_object']}")
    st.write(f"E_Object: {st.session_state['destination_object']}")
    st.write(f"{point_dict['point1']} --> {point_dict['point2']} --> {point_dict['point3']}")
    map_btn = st.button("Confirm List")

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
                        st.session_state["origin_point"] = name
                        st.session_state["origin_object"] = item
                with col_end:
                    if st.button(f"Set as End", key=f"end_{name}"):
                        st.session_state["destination_point"] = name
                        st.session_state["destination_object"] = item

display_location_grid(df)

if map_btn:
    st.session_state["candidate_point"] = df
    st.experimental_set_query_params(page="map")
    st.switch_page("pages/map.py")