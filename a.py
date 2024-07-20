import networkx as nx
import osmnx as ox
from shapely.geometry import LineString, mapping
import geopandas as gpd
import json
from ipyleaflet import *

ox.config(use_cache=True, log_console=True)
# load graph from disk and confirm 'w3' edge attribute is there
graph = ox.load_graphml('graph.graphml')
nodes, edges = ox.graph_to_gdfs(graph)

center = (16.4683,107.5786)
m = Map(center=center, basemap=basemaps.CartoDB.Positron, zoom=15)
to_marker_style = AwesomeIcon(
    name='circle',
    icon_color='white',
    marker_color='red',
    spin=False
)
from_marker = Marker(location=center)
to_marker = Marker(location=(16.4531082, 107.5449069), icon=to_marker_style)

def set_nearest_node(marker):
    marker.nearest_node = ox.nearest_nodes(graph, marker.location[0],marker.location[1])
    return

path_layer_list = []

def handle_change_location(event, marker):
    event_owner = event['owner']
    print(event_owner.location)
    event_owner.nearest_node = ox.nearest_nodes(graph, event_owner.location[0],event_owner.location[1])
    marker.neares_node = ox.nearest_nodes(graph, marker.location[0],marker.location[1])
    
    shortest_path = nx.dijkstra_path(graph, event_owner.nearest_node, marker.neares_node, 
                                     weight='length')
    print(shortest_path)
    if len(path_layer_list) == 1:
        m.remove_layer(path_layer_list[0])
        path_layer_list.pop()
    
    shortest_path_points = nodes.loc[shortest_path]
    path = gpd.GeoDataFrame([LineString(shortest_path_points.geometry.values)], columns=['geometry'])
    path_layer = GeoData(geo_dataframe=path, style={'color':'black', 'weight':2})
    m.add_layer(path_layer)
    path_layer_list.append(path_layer)
    print(shortest_path)
    
    
from_marker.observe(lambda event: handle_change_location(event, to_marker), 'location')
to_marker.observe(lambda event: handle_change_location(event, from_marker), 'location')

m.add_layer(from_marker)
m.add_layer(to_marker)
set_nearest_node(from_marker)
set_nearest_node(to_marker)