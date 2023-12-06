import requests,json
from decode_polyline import decode_polyline
from math import ceil
from remove_points import remove_duplicite_points



def route(points,type):
    url = "http://localhost:8002/route"
    headers = {'Content-type': 'application/json'}
    geometries = []
    strr = ""
    i = 0
    for pt in points: 
        strr += '{"lat":'+str(pt[1])+',"lon":'+str(pt[0])+',"type":"'+type+'"},'
        if (i == 19):
            strr = strr[:-1]
            data = '{"locations":['+str(strr)+'],"format": "osrm","costing": "auto","costing_options":{"auto":{"shortest":true}},"banner_instructions": true,"language": "sk-SK"}'
            r = requests.post(url, data=data, headers=headers)
            i = 0
            strr = ""
            if r.status_code == 200:
                response_text = json.loads(r.text)
                geometry = response_text['routes'][0]['geometry']
                geometries.append(geometry)
            else:
                print(f"bad thing happened {r.content} and input {data} and url {url}")
        i += 1
    if strr != "":
        strr = strr[:-1]
        data = '{"locations":['+str(strr)+'],"format": "osrm","costing": "auto","costing_options":{"auto":{"shortest":true}},"banner_instructions": true,"language": "sk-SK"}'
        r = requests.post(url, data=data, headers=headers)
        i = 0
        strr = ""
        if r.status_code == 200:
            response_text = json.loads(r.text)
            geometry = response_text['routes'][0]['geometry']
            geometries.append(geometry)
        else:
            print(f"bad thing happened {r.content} and input {data} and url {url}")
    return geometries

def open_file(file):
    f = open(file, "r")
    text = f.read()
    data = json.loads(text)
    features = data['features']
    feature = features[0]
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    f.close()
    return data, coordinates

# data, coords = open_file('C:/Users/richard.buri/search_web/python/test.geojson')

def route_get_points(coords):
    geometries = route(coords,"trough")
    body = []
    for geometry in geometries:
        body.append(decode_polyline(geometry,True))
    body = [item for sublist in body for item in sublist]
    body = remove_duplicite_points(body)
    nieco = {u"type": u"LineString", u"coordinates": body}
    return(str(nieco).replace("'",'"'))


# print(route_get_points(coords))
