import streamlit as st
import pandas as pd
import folium
import json
from folium import IFrame, plugins
from streamlit_folium import st_folium
import requests
import networkx as nx
import osmnx as ox
from streamlit_extras.grid import grid
from streamlit_star_rating import st_star_rating


import io
from PIL import Image

st.write("this is planner")
url = "https://huexploreapi-2sc3g5mmrq-uc.a.run.app/"
domain = "http://localhost"
port = ":8080"
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

# my_grid = grid([2, 4, 1], vertical_align="bottom")
# # Row 2:
# my_grid.selectbox("Select Country", ["Germany", "Italy", "Japan", "USA"])
# my_grid.text_input("Your name")
# my_grid.button("Send", use_container_width=True)
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

start=[16.4683,107.5786]
with col1:
    m = folium.Map(location=start, zoom_start=10)
    gg_res= st.session_state["final_locations"] 
    if len(gg_res)!=0:
        place_show = st.session_state["place_show"]
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
    folium.plugins.MiniMap(width=100, height=100).add_to(m)
    st_data = st_folium(m, width=600, height=400, returned_objects=[])


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
# from PIL import ImageGrab
# im = ImageGrab.grab()
# # Capture a specific region (left, top, right, bottom)
# # screenshot = ImageGrab.grab(bbox=(100, 100, 500, 500))
# st.image(im)