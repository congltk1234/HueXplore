import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_sortables_local import sort_items
import folium
import json
import base64
from folium import IFrame, plugins
from streamlit_folium import st_folium

import networkx as nx
import osmnx as ox
ox.config(use_cache=True, log_console=True)
@st.cache_data(show_spinner=False)
def fetch_graphml_data(path='graph.graphml'):
    return ox.load_graphml(path)

G = fetch_graphml_data('graph.graphml')

@st.cache_resource
def find_routes(graph, start, end):
    return ox.routing.shortest_path(graph, start, end, weight="length")



# if 'sidebar_state' not in st.session_state:
# st.set_page_config(page_title="Tourism Planner", page_icon="🌍", layout="wide", initial_sidebar_state='collapsed')
st.markdown("Tourism Planner")
st.sidebar.header("Tourism Planner")

st.title("Planner")

col1, col2 = st.columns(spec=[0.6, 0.4])

with col1:
    if "selected_items" in st.session_state:
        selected_items = st.session_state["selected_items"]
        selected_names = st.session_state["selected_names"]
        items = [
        {'header': 'location_results', 'items': selected_names},
        {'header': 'planner_results', 'items': []},
    ]   
        sorted_items = sort_items(items, multi_containers=True, direction="vertical")
    else:
        st.write("No items selected.")

def map_result(list2, dict1):
    item_set = set(dict1['items'])
    filtered_list = [item for item in list2 if item['name'] in item_set]
    filtered_list.sort(key=lambda x: dict1['items'].index(x['name']))
    return filtered_list

add_cafe = st.button("add cafe")

if add_cafe:
    text = "HUET"
    sorted_items[1]["items"].append(text)
    st.write(sorted_items[1]["items"])
    
gg_res = map_result(selected_items, sorted_items[1]) 
start=[16.4683,107.5786]

# f = open('api-response2.json')
# data = json.load(f)
st.write(gg_res)

with col2:
    st.markdown("### Map")
    m = folium.Map(location=start, zoom_start=10)
    if len(gg_res)!=0:
        for index,place in enumerate(gg_res):
            destination_point = gg_res[index]['coordinate']
            if index>0:
                origin_point = gg_res[index-1]['coordinate']
                origin_node = ox.distance.nearest_nodes(G, float(origin_point[1]), float(origin_point[0])) 
                destination_point = gg_res[index]['coordinate']
                destination_node = ox.distance.nearest_nodes(G, float(destination_point[1]), float(destination_point[0]))
                route_nodes = ox.routing.shortest_path(G, origin_node, destination_node, weight="length")
                # route_data = data['data']['routes'][0]['legs'][index-1]['points']
                # points_list = [[point['latitude'], point['longitude']] for point in route_data]

                # print(route_nodes)
                points_list = [[G.nodes[node]['y'],G.nodes[node]['x']] for node in route_nodes]
                folium.PolyLine(locations=points_list, color='blue', dash_array='5, 5',
                                tooltip="From Shikarpur to Binaur",
                        smooth_factor=0.1,  #  for making poliyline straight
                        ).add_to(m)
            html_name= popup_html = f"<b>{place['name']}</b> <br/>"
            # popup_html = f"<b>Date:</b> {data['Date']}<br/>"
            popup_html += f"<b>Place:</b> {index}<br/>"
            # popup_html += f"<b>Time:</b> {data['Time']}<br/>"
            popup_html += '<b><a href="{}" target="_blank">Event Page</a></b>'.format(place['gg_map'])
            if  isinstance(place['img'], str):
                popup_html += f'''<img src="{place['img']}">'''
            else:
                encoded = base64.b64encode(open('biena.png', 'rb').read())
                html = '<img src="data:image/png;base64,{}">'.format
                popup_html += html(encoded.decode('UTF-8'))
            popup_iframe = folium.IFrame(width=200, height=110, html=popup_html)
            popup = folium.Popup(popup_iframe,  width=400, height=350)
            folium.Marker(location=place['coordinate'], tooltip=html_name, icon=folium.Icon(icon='stop'), popup = popup).add_to(m)
            # folium.Marker(location=place['coordinate'], tooltip=f'Place {index}', icon=folium.Icon(icon='play'), popup='Start').add_to(m)

    minimap = plugins.MiniMap()
    m.add_child(minimap)
    folium.FitOverlays().add_to(m)
    st_data = st_folium(m, width=800)

# st.write(points_list)
st.write(gg_res)

