import streamlit as st
from pymongo import MongoClient
import pandas as pd
from fixed_header import st_fixed_container
import networkx as nx 
import osmnx as ox
from shapely import Point
import requests

# https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.simple_paths.shortest_simple_paths.html
from itertools import islice
def k_shortest_paths(G, source, target, k, weight=None):
    return list(
        islice(nx.shortest_simple_paths(G, source, target, weight=weight), k)
    )

url = "https://huexploreapi-2sc3g5mmrq-uc.a.run.app/"

# Configure page settings
st.set_page_config(page_title="Location Result", page_icon="🌍", layout="wide", initial_sidebar_state='collapsed')
st.sidebar.header("Location Result")

def recommend_routes(start, end, candidates_df, k=3,leng_path=4):
    print(start, end)
    df_mg = candidates_df
    df_mg = df_mg.reset_index(drop=True)
    name_list = [i['name'] for _,i in df_mg.iterrows()]
    geometry = [Point(float(i['coordinate'][1]),float(i['coordinate'][0])) for _,i in df_mg.iterrows()]
    # near_ID = [ox.distance.nearest_nodes(graph,float(i['coordinate'][1]),float(i['coordinate'][0])) for i in ggres]
    x = [float(i['coordinate'][1]) for _,i in df_mg.iterrows()]
    y = [float(i['coordinate'][0]) for _,i in df_mg.iterrows()]
    place_dict = {}
    for i in range(len(name_list)):
        place_dict[name_list[i]] = {'lat':x[i], 'long':y[i]}

    g = nx.complete_graph(df_mg['name'],nx.DiGraph())
    df = nx.to_pandas_edgelist(g)
    weights = []
    for index, row in df.iterrows():
        source = row['source']
        target = row['target']
        weight = ox.distance.euclidean(place_dict[source]['lat'], place_dict[source]['long'], 
                                       place_dict[target]['lat'], place_dict[target]['long'])
        weights.append(weight)
    df['weights'] = weights
    df = df.sort_values(['source', 'weights'], ascending=[False, True])
    df = df.reset_index(drop=True)

    n= len(place_dict)
    
    # index =[[int(i+n*0.1), int(i+n*0.3)] for i in range(0,1980, n)]
    index =[[i, int(i+n*0.3)] for i in range(0,n*(n-1), n)]
    new_index = []
    for i in index:
        for j in range(*i):
            new_index.append(j)
    df = df.iloc[new_index]

    g = nx.Graph()
    weighted_edges = list(zip(*[df[col] for col in df]))
    g.add_weighted_edges_from(weighted_edges)

    count=0
    recommend_routes = []
    for path in k_shortest_paths(g, start, end, 20, 'weights'):
        if len(path)==leng_path:
            # print(path)
            route = df_mg[df_mg.name.isin(path) == True]
            sorterIndex = dict(zip(path, range(len(path))))
            route['order'] = route['name'].map(sorterIndex)
            route.sort_values(['order'],inplace = True)
            recommend_routes.append(route.to_dict(orient='records'))
            count+=1
        if count==k:
            break 
    st.session_state["recommend_routes"] = recommend_routes


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

is_moods = st.session_state.get("is_moods", False)
is_interests = st.session_state.get("is_interests", False)
moods_select = st.session_state.get("moods_select", [])
interests_select = st.session_state.get("interests_select", [])

query = {}
if is_interests:
    query["interests"] = {"$all": interests_select}
if is_moods:
    query["moods"] = {"$all": moods_select}

res_obj = {
    "is_moods": is_moods,
    "is_interests": is_interests,
    "moods_select": moods_select,
    "interests_select": interests_select,
}

response = requests.post(url + "/ind-loc", json = res_obj)

df = pd.DataFrame({
    "name": response.json()["names_res"],
    "img": response.json()["img_res"],
    "coordinate": response.json()["coor_res"],
    "gg_map": response.json()["ggmap_res"],
    "interests": response.json()["interests_res"],
    "moods": response.json()["moods_res"],
    "node_id": response.json()["node_id"]
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

if "interests_can" not in st.session_state:
    st.session_state["interests_can"] = []
if "moods_can" not in st.session_state:
    st.session_state["moods_can"] = []
if "bruh" not in st.session_state:
    st.session_state["bruh"] = []
    
def select_candidate_points(line_index):
    line_objects = st.session_state["recommend_routes"][line_index]
    st.session_state["candidate_points"] = line_objects

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
                st.markdown(f"""
                    <style>
                        #item{index}::before {{
                        content: "{name}";
                        font-size: larger;
                        padding:5px;
                        position: absolute;
                        top: 0;
                        left: 0;
                        background: rgba(0, 0, 0, 0.5);
                        color: white;
                        padding: 5px;
                        font-size: 16px;
                    }}
                    </style>
                """,  unsafe_allow_html=True)

                col.markdown(f"""
                        <div id = "item{index}" style="padding: 5px; height: {card_height}px; display: flex; justify-content: left; align-items: left;">
                            <img src="{img}" style="max-width: 350px; min-width: 350px; min-height: 250px; max-height: 250px;">
                        </div>
                """, unsafe_allow_html=True)

                col_start, col_end = st.columns(2)
                
                with col_start:
                    if st.button(f"Set as Start", key=f"start_{name}"):
                        st.session_state["origin_point"] = name
                        st.session_state["origin_object"] = item
                        if isinstance(st.session_state["destination_point"], str):
                            recommend_routes(st.session_state["origin_point"], st.session_state["destination_point"], df)
                            
                with col_end:
                    if st.button(f"Set as End", key=f"end_{name}"):
                        st.session_state["destination_point"] = name
                        st.session_state["destination_object"] = item
                        if isinstance(st.session_state["origin_point"], str):
                            recommend_routes(st.session_state["origin_point"], st.session_state["destination_point"], df)

display_location_grid(df)

with st_fixed_container(mode="fixed", position="top", border=True):
    
    fixed_col1, fixed_col2 = st.columns([2, 8])

    with fixed_col1:

        st.markdown(f"""
                <style>
                    @media only screen and (max-width: 600px) {{
                        .origin, .destination {{
                            font-size: 10px;
                        }}
                    }}
                    .origin {{
                        color: red; 
                        font-size: larger; 
                        font-weight: 600;
                    }}
                    .destination {{
                        color: green; 
                        font-size: larger; 
                        font-weight: 600;
                    }}
                </style>
                <p class="origin">Origin: {st.session_state['origin_point']}</p>
                <p class="destination">Destination: {st.session_state['destination_point']}</p>
            """, unsafe_allow_html=True,
            )
        go_btn = st.button("Xuất phát")
    with fixed_col2:
        if (isinstance(st.session_state["origin_point"], str)) and (isinstance(st.session_state["destination_point"], str)):
            css = """
                <style>
                    .flow-container {
                        display: flex;
                        align-items: center;
                        margin-bottom: 10px;
                    }
                    .flow-container div {
                        padding: 5px 10px;
                        background-color: #f0f0f0;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        margin-right: 5px;
                    }
                    .flow-container div.arrow {
                        background-color: transparent;
                        border: none;
                        margin-right: 0;
                    }
                    .add-line-button {
                        margin-bottom: 10px;
                    }
                </style>
            """
            st.markdown(css, unsafe_allow_html=True)

            for line_index, lobj in enumerate(st.session_state["recommend_routes"]):
                display_string = ""
                for i, obj in enumerate(lobj):
                    flow = "→" if i != 0 else ""
                    if flow:
                        display_string += f'<div class="arrow">{flow}</div>'
                    display_string += f'<div>{obj["name"]}</div>'

                html_content = f"""
                    <div class="flow-container">{display_string}</div>
                """
                push_col1, push_col2 = st.columns([2, 8])
                with push_col2:
                    st.markdown(html_content, unsafe_allow_html=True)
                with push_col1:
                    push_btn = st.button("Chọn lịch trình này", key=f"line_{line_index}", use_container_width=True)
                if push_btn:
                    select_candidate_points(line_index)
                    for i in st.session_state["candidate_points"]:
                        st.session_state["interests_can"] += i["interests"]
                        st.session_state["moods_can"] += i["moods"]
                    # st.session_state["moods_can"] = st.session_state["origin_object"]["moods"] + st.session_state["destination_object"]["moods"]
                    st.experimental_set_query_params(page="map")
                    st.switch_page("pages/map.py")
                    
            
if go_btn:
    st.session_state["candidate_points"] = [st.session_state["origin_object"], st.session_state["destination_object"]]
    st.session_state["interests_can"] = st.session_state["origin_object"]["interests"] + st.session_state["destination_object"]["interests"]
    st.session_state["moods_can"] = st.session_state["origin_object"]["moods"] + st.session_state["destination_object"]["moods"]
    st.experimental_set_query_params(page="map")
    st.switch_page("pages/map.py")