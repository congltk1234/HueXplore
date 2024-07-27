import streamlit as st
import pandas as pd
# from pymongo import MongoClient
# from streamlit_sortables_local import sort_items
import folium
import json
from folium import IFrame, plugins
from streamlit_folium import st_folium

import networkx as nx
import osmnx as ox
from streamlit_extras.grid import grid
import streamlit.components.v1 as components

import io
from PIL import Image

st.write("this is planner")

if "final_locations" in st.session_state:
    final_locations = st.session_state["final_locations"]
# ox.config(use_cache=True, log_console=True)
# @st.cache_data(show_spinner=False)
# def fetch_graphml_data(path='graph.graphml'):
#     return ox.load_graphml(path)

# G = fetch_graphml_data('graph.graphml')

# @st.cache_resource
# def find_routes(graph, start, end):
#     return ox.routing.shortest_path(graph, start, end, weight="length")



# # if 'sidebar_state' not in st.session_state:
# # st.set_page_config(page_title="Tourism Planner", page_icon="🌍", layout="wide", initial_sidebar_state='collapsed')
# st.markdown("Tourism Planner")
# st.sidebar.header("Tourism Planner")

# st.title("Planner")
m = folium.Map(location=[39.949610, -75.150282], zoom_start=16)
folium.Marker(
    [39.949610, -75.150282], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

col1, col2 = st.columns(spec=[4,6])

with col2:
    with st.container():
        for i, location in enumerate(final_locations):
            with st.expander(location["name"]):
                inside_col1, inside_col2 = st.columns(spec=[2,8])
                with inside_col1:
                    st.image(location["img"])
                with inside_col2:
                    st.subheader(f"Mô tả của địa điểm", divider="gray")
                    long_text = f"Địa điểm thứ {i+1} trong lịch trình"
                    # https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream
                    st.write(long_text)


with col1:
    st_folium(m, width=725, returned_objects=[])
    # đổi sang GoogleMApEngine
    exp_btn = st.button("Đồng bộ hóa lịch trình trên google map")

st.write(final_locations)

if exp_btn:
    url = "https://www.google.com/maps/dir"
    for location in final_locations:
        url += "/" + location["name"] + location["address"]
    st.write(f'''
        <a target="_self" href="{url}">
            <button>
                Đồng bộ hóa thành công, chuyển đến map
            </button>
        </a>
        ''',
        unsafe_allow_html=True
    )    
    # components.iframe(url+"&output=embed")