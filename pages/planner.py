import streamlit as st
import pandas as pd
from pymongo import MongoClient
from streamlit_sortables_local import sort_items


st.set_page_config(page_title="Tourism Planner", page_icon="🌍", layout="wide")
st.markdown("Tourism Planner")
st.sidebar.header("Tourism Planner")

st.title("Planner")

col1, col2 = st.columns(2)

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

with col2:
    st.markdown("### Map")

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
st.write(gg_res)
st.write(sorted_items[1]["items"])

