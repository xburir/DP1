# %% IMPORT LIBRARIES
import folium
import pandas as pd
import geopandas as gpd
import json
import requests
from shapely.geometry.linestring import LineString
from pyproj import Geod


# decode an encoded string
def decode(encoded):
    inv = 1.0 / 1e6
    decoded = []
    previous = [0, 0]
    i = 0
    # for each byte
    while i < len(encoded):
        # for each coord (lat, lon)
        ll = [0, 0]
        for j in [0, 1]:
            shift = 0
            byte = 0x20
            # keep decoding bytes until you have this coord
            while byte >= 0x20:
                byte = ord(encoded[i]) - 63
                i += 1
                ll[j] |= (byte & 0x1f) << shift
                shift += 5
            # get the final value adding the previous offset and remember it for the next
            ll[j] = previous[j] + (~(ll[j] >> 1) if ll[j] & 1 else (ll[j] >> 1))
            previous[j] = ll[j]
        # scale by the precision and chop off long coords also flip the positions so
        # it's the far more standard lon,lat instead of lat,lon
        decoded.append([float('%.6f' % (ll[1] * inv)), float('%.6f' % (ll[0] * inv))])
    # hand back the list of coordinates
    return decoded


def tutorial_jedna(response_text):
    search_1 = response_text.get('matchings')
    search_2 = dict(search_1[0])
    polyline6 = search_2.get('geometry')
    search_3 = response_text.get('tracepoints')

    lst_MapMatchingRoute = LineString(decode(polyline6))
    gdf_MapMatchingRoute_linestring = gpd.GeoDataFrame(geometry=[lst_MapMatchingRoute], crs=4326)
    gdf_MapMatchingRoute_points_temp = gdf_MapMatchingRoute_linestring.apply(
        lambda x: [y for y in x['geometry'].coords], axis=1)
    gdf_MapMatchingRoute_points = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy([a_tuple[0] for a_tuple in gdf_MapMatchingRoute_points_temp[0]],
                                    [a_tuple[1] for a_tuple in gdf_MapMatchingRoute_points_temp[0]]), crs=4326)
    gdf_MapMatchingRoute = gpd.GeoDataFrame(
        pd.concat([gdf_MapMatchingRoute_linestring, gdf_MapMatchingRoute_points], ignore_index=True))

    # TODO-riso tu som sa zasekl
    df_mapmatchedGPS_points = pd.DataFrame(list([d['location'] for d in search_3 if 'location' in d]),
                                           columns=['lon', 'lat'])
    gdf_mapmatchedGPS_points = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(df_mapmatchedGPS_points['lon'], df_mapmatchedGPS_points['lat']), crs=4326)

    # %% RAW & MAP-MATCHING ROUTES - DRAW MAP
    m = folium.Map([22.2783, -97.8643], tiles='cartodbdark_matter', zoom_start=14)
    folium.GeoJson(gdf_rawGPS, style_function=lambda x: {'color': 'red'},
                   marker=folium.CircleMarker(radius=4, weight=0, fill_color='red', fill_opacity=1),
                   name='rawGPS_points').add_to(m)
    folium.GeoJson(gdf_mapmatchedGPS_points,
                   marker=folium.CircleMarker(radius=4, weight=0, fill_color='white', fill_opacity=1),
                   name='MapMatching_rawGPS_points').add_to(m)
    folium.GeoJson(gdf_MapMatchingRoute, style_function=lambda x: {'color': 'green'},
                   marker=folium.CircleMarker(radius=4, weight=0, fill_color='green', fill_opacity=1),
                   name='MapMatching_Route').add_to(m)
    folium.LayerControl(position='topright', collapsed=False).add_to(m)
    m.save('mapmatching.html')

    # %% RAW & MAP-MATCHING ROUTES - CALCULATE DISTANCE
    geod = Geod(ellps="WGS84")
    rawGPS_linestring_distance = geod.geometry_length(gdf_rawGPS_linestring['geometry'][0])
    MapMatchingRoute_linestring_distance = geod.geometry_length(gdf_MapMatchingRoute_linestring['geometry'][0])
    print('rawGPS_linestring_distance = ', f"{rawGPS_linestring_distance:,.0f}")
    print('MapMatchingRoute_linestring_distance = ', f"{MapMatchingRoute_linestring_distance:,.0f}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # %% READ & FORMAT GPS INFO

    geojson_file = 'second.geojson'
    gdf_rawGPS_linestring = gpd.read_file(geojson_file)
    gdf_rawGPS_points_temp = gdf_rawGPS_linestring.apply(lambda x: [y for y in x['geometry'].coords], axis=1)
    gdf_rawGPS_points = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy([a_tuple[0] for a_tuple in gdf_rawGPS_points_temp[0]],
                                    [a_tuple[1] for a_tuple in gdf_rawGPS_points_temp[0]]), crs=4326)
    df_rawGPS_points = pd.DataFrame(list(zip([a_tuple[0] for a_tuple in gdf_rawGPS_points_temp[0]],
                                             [a_tuple[1] for a_tuple in gdf_rawGPS_points_temp[0]])),
                                    columns=['lon', 'lat'])
    gdf_rawGPS = gpd.GeoDataFrame(pd.concat([gdf_rawGPS_linestring, gdf_rawGPS_points], ignore_index=True))

    # %% VALHALLA REQUEST
    meili_coordinates = df_rawGPS_points.to_json(orient='records')
    meili_head = '{"shape":'
    meili_tail = ""","search_radius": 150, "shape_match":"map_snap", "costing":"auto", "format":"osrm"}"""
    meili_request_body = meili_head + meili_coordinates + meili_tail

    url = "http://localhost:8002/trace_route"
    headers = {'Content-type': 'application/json'}
    data = str(meili_request_body)
    r = requests.post(url, data=data, headers=headers)

    # %% READ & FORMAT VALHALLA RESPONSE

    if r.status_code == 200:
        response_text = json.loads(r.text)
    else:
        print(f"bad thing happened {r.content}")

    # tutorial_jedna(response_text)

    # There are a lot more information that we got from Meili
    # but I'm interested in just 'tracepoints'
    resp = str(response_text['tracepoints'])

    # This is a replacement to distinguish single None's in a row
    # from "waypoint_index" being None
    resp = resp.replace("'waypoint_index': None", "'waypoint_index': '#'")
    resp = resp.replace("None",
                        "{'matchings_index': '#', 'name': '', 'waypoint_index': '#', 'alternatives_count': 0, 'distance': 0, 'location': [0.0, 0.0]}")

    # This is to make it a valid JSON
    resp = resp.replace("'", '"')
    resp = json.dumps(resp)
    resp = json.loads(resp)

    # Reading our JSON to a Pandas DataFrame
    df_response = pd.read_json(resp)

    # Saving the columns that I actually need
    df_response = df_response[['name', 'distance', 'location']]

    # FORMAT for geojson.io
    for index, row in df_response.iterrows():
        if row['location'] != [0.0, 0.0]:
            print(f"{row['location']},")

