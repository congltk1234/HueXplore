import streamlit as st
import pandas as pd
from pymongo import MongoClient
import folium
import json
from folium import IFrame, plugins
from streamlit_folium import st_folium
from st_draggable_list import DraggableList

import networkx as nx
import osmnx as ox

st.markdown("Tourism Planner")
st.sidebar.header("Tourism Planner")
import streamlit as st
import pandas as pd
import requests

url = "https://huexploreapi-2sc3g5mmrq-uc.a.run.app/"
domain = "http://localhost"
port = ":5000"

if "candidate_points" in st.session_state:
    candidates = st.session_state["candidate_points"]
if "interests_can" in st.session_state:
    interests_can = st.session_state["interests_can"]
if "moods_can" in st.session_state:
    moods_can = st.session_state["moods_can"]
place_show = st.session_state.get("place_show", [])

def update_orders(data):
    for index, item in enumerate(data):
        item["order"] = index + 1
    return data

def create_draggable_list():
    return DraggableList(st.session_state.data, width="100%")

initial_data = candidates

for index, item in enumerate(initial_data):
    item["order"] = index + 1

if "data" not in st.session_state:
    st.session_state.data = initial_data

map_col1, map_col2 = st.columns([5, 5])
with map_col1:
    with st.container():

        
        dynamic_list = create_draggable_list()

        if dynamic_list is not None:
            st.session_state.data = update_orders(dynamic_list)
        else:
            dynamic_list = st.session_state.data

    with st.container(height=800):
        res_obj = {
            "moods_can": moods_can,
            "interests_can": interests_can,
            "name_res": [i["name"] for i in candidates]
        }
        # response = requests.post(url+ "/dynamic-loc", json = res_obj)
        response = requests.post(domain + port+ "/dynamic-loc", json = res_obj)

        df = pd.DataFrame({
            "name": response.json()["names_res"],
            "img": response.json()["img_res"],
            "coordinate": response.json()["coor_res"],
            "gg_map": response.json()["ggmap_res"],
            "interests": response.json()["interests_res"],
            "moods": response.json()["moods_res"],
            "isshow": response.json()["isshow_res"],
            "node_id": response.json()["node_id"]
        })
        df = df.sort_values(by='isshow', ascending=False)
        st.session_state["place_show"] = df[df['isshow']==True].to_dict(orient='records')
        def display_additional_grid(df):
            card_height = 150
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
                        if item["isshow"]:
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
                                    <img src="{img}" style="max-width: 220px; min-width: 220px; min-height: 140px; max-height: 140px;">
                                </div>
                        """, unsafe_allow_html=True)
                        add_btn =  st.button(f"Thêm", key=f"add_{name}")
                        if add_btn:
                            item_dict = item.to_dict()
                            # st.session_state["candidate_points"].append(item_dict)
                            item_dict["order"] = len(st.session_state.data) + 1
                            st.session_state.data.append(item_dict)
                            st.session_state.data = update_orders(st.session_state.data)
                            st.session_state["candidate_points"] = update_orders(st.session_state.data)
        display_additional_grid(df)
st.write(st.session_state.data)
import json
start=[16.4683,107.5786]
with map_col2:
    st.markdown("### Map")
    m = folium.Map(location=start, zoom_start=10)
    gg_res=st.session_state["candidate_points"]
    if len(gg_res)!=0:
        place_show = st.session_state["place_show"]
        for index,place in enumerate(place_show):
            name = place['name']
            website = "#"
            directions = place['gg_map']
            pub_html = folium.Html(f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
            <p style="text-align: center;"><img src="{place['img']}" width="220" height="250">
            <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 14px;">{name} Website</span></a></p>
            <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 14px;">Directions to {name}</span></a></p>
            """, script=True)
            popup = folium.Popup(pub_html, max_width=220)
            icon = folium.Icon(color='blue', prefix='fa',icon=f'map-pin', width='50%')
            folium.Marker(location=place['coordinate'], tooltip=name, icon=icon, popup = popup).add_to(m)
        for index,place in enumerate(gg_res):
            if index>0:
                res_obj = {
                "origin_node": gg_res[index-1]['node_id'],
                "destination_node": gg_res[index]['node_id'],
                }
                # response = requests.post(url + "/find-route", json = res_obj)
                response = requests.post(domain + port + "/find-route", json = res_obj)
                points_list= response.json()
                folium.PolyLine(locations=points_list, color='blue', dash_array='5, 5',
                                tooltip=f"From a to b", smooth_factor=0.1,).add_to(m)
            # Define marker variables
            name = place['name']
            website = "#"
            directions = place['gg_map']
            pub_html = folium.Html(f"""<p style="text-align: center;"><b><span style="font-family: Didot, serif; font-size: 18px;">{name}</b></span></p>
            <p style="text-align: center;"><img src="{place['img']}" width="220" height="250">
            <p style="text-align: center;"><a href={website} target="_blank" title="{name} Website"><span style="font-family: Didot, serif; font-size: 14px;">{name} Website</span></a></p>
            <p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><span style="font-family: Didot, serif; font-size: 14px;">Directions to {name}</span></a></p>
            """, script=True)
            popup = folium.Popup(pub_html, max_width=220)
            icon = folium.Icon(color='red', prefix='fa',icon=f'{index+1}')
            folium.Marker(location=place['coordinate'], tooltip=name, icon=icon, popup = popup).add_to(m)
   
    folium.FitOverlays().add_to(m)
    st_data = st_folium(m, width=1000, returned_objects=[])
    
st.write(st_data)