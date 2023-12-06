
import folium
import pandas as pd
import geopandas as gpd
import json
import requests
from shapely.geometry.linestring import LineString
from pyproj import Geod

# Press the green button in the gutter to run the script.
def map_match(points):
    strr = ""
    for pt in points:
        strr += '{"lat":'+str(pt[1])+',"lon":'+str(pt[0])+'},'
    strr = strr[:-1]

    meili_coordinates = strr
    meili_head = '{"shape":['
    meili_tail = """],"search_radius": 300, "shape_match":"map_snap", "costing":"auto", "format":"osrm"}"""
    meili_request_body = meili_head + meili_coordinates + meili_tail

    url = "http://localhost:8002/trace_route"
    headers = {'Content-type': 'application/json'}
    data = str(meili_request_body)
    # print(data)

    r = requests.post(url, data=data, headers=headers)

    

    if r.status_code == 200:
        response_text = json.loads(r.text)
        return response_text['matchings'][0]['geometry']
    else:
        print(f"bad thing happened {r.content}")


    
   

