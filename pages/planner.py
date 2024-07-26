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
import pyautogui


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


my_grid = grid([2, 4, 1], vertical_align="bottom")
# Row 2:
my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
my_grid.text_input("Your name")
my_grid.button("Send", use_container_width=True)
    # pyautogui.hotkey("ctrl", "p")
col1, col2 = st.columns(spec=[4,6])

with col2:
    with st.container():
        for i, location in enumerate(final_locations):
            with st.expander(f"Place {i+1}", expanded=True):
                inside_col1, inside_col2 = st.columns(spec=[2,8])
                with inside_col1:
                    st.image(location["img"])
                with inside_col2:
                    st.subheader(location["name"], divider="gray")
                    long_text = f"Địa điểm thứ {i+1} trong lịch trình"
                    # https://docs.streamlit.io/develop/api-reference/write-magic/st.write_stream
                    st.write(long_text)


with col1:
    st_folium(m, width=725, returned_objects=[])
    # đổi sang GoogleMApEngine

from streamlit_star_rating import st_star_rating
stars = st_star_rating('Bạn đánh giá lộ trình này như thế nào?', 5, 0, size=60, emoticons=True, read_only=False, dark_theme=False, 
                    #    resetButton=reset_btn, resetLabel=reset_label,
                    #    customCSS=css_custom, on_click=function_to_run_on_click if enable_on_click else None
                       )

st.markdown(
    """
    <style type="text/css" media="print">
    div.page-break
    {
        page-break-after: always;
        page-break-inside: avoid;
    }
    </style>
    <div class="page-break">
        <!-- Content goes here -->
    </div>
""",
    unsafe_allow_html=True,
)
from PIL import ImageGrab
im = ImageGrab.grab()
# Capture a specific region (left, top, right, bottom)
# screenshot = ImageGrab.grab(bbox=(100, 100, 500, 500))
st.image(im)