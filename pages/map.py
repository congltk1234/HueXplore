import streamlit as st
from streamlit_sortables import sort_items
import pandas as pd
import requests

domain = "http://localhost"
port = ":5000"

if "candidate_points" in st.session_state:
    candidates = st.session_state["candidate_points"]
if "interests_can" in st.session_state:
    interests_can = st.session_state["interests_can"]
if "moods_can" in st.session_state:
    moods_can = st.session_state["moods_can"]


map_col1, map_col2 = st.columns([6, 4])
with map_col1:
    with st.container():
        st.write(candidates)
    with st.container(height=800):
        res_obj = {
            "moods_can": moods_can,
            "interests_can": interests_can,
            "name_res": [i["name"] for i in candidates]
        }
        response = requests.post(domain + port + "/dynamic-loc", json = res_obj)

        df = pd.DataFrame({
            "name": response.json()["names_res"],
            "img": response.json()["img_res"],
            "coordinate": response.json()["coor_res"],
            "gg_map": response.json()["ggmap_res"],
            "interests": response.json()["interests_res"],
            "moods": response.json()["moods_res"],
            "isshow": response.json()["isshow_res"],
        })
        df = df.sort_values(by='isshow', ascending=False)
        def display_additional_grid(df):
            card_height = 160
            num_columns = 4
            num_rows = len(df)

            rows = [df.iloc[i:i + num_columns] for i in range(0, num_rows, num_columns)]

            for row in rows:
                cols = st.columns(num_columns)
                for col, (index, item) in zip(cols, row.iterrows()):
                    name = item['name']
                    img = item['img']
                    with col:
                        mark_color = "background: rgba(0, 0, 0, 0.5); color: white;"
                        if not item["isshow"]:
                            mark_color = "background: rgba(0, 0, 0, 0.8); color: red; font-weight: 900"
                        st.markdown(f"""
                            <style>
                                #item{index}::before {{
                                content: "{name}";
                                font-size: larger;
                                padding:2px;
                                position: absolute;
                                top: 0;
                                left: 0;
                                {mark_color}
                                padding: 2px;
                                font-size: 16px;
                            }}
                            </style>
                        """,  unsafe_allow_html=True)

                        col.markdown(f"""
                                <div id = "item{index}" style="padding: 2px; height: {card_height}px; display: flex; justify-content: left; align-items: left;">
                                    <img src="{img}" style="max-width: 250px; min-width: 250px; min-height: 150px; max-height: 150px;">
                                </div>
                        """, unsafe_allow_html=True)
                        add_btn =  st.button(f"Thêm", key=f"add_{name}")      
                        # if add_btn:
                        #     st.                 
        display_additional_grid(df)

with map_col2:
    st.write("this is map")