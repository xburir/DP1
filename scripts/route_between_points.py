import requests,json
from decode_polyline import decode_polyline
from math import ceil



def route(points,type):
    url = "http://localhost:8002/route"
    headers = {'Content-type': 'application/json'}
    geometries = []
    size = ceil(len(points)/19.0)
    for i in range(size): 
        strr = ""
        for pt in points[20*i:(i+1)*20-1]:
            strr += '{"lat":'+str(pt[1])+',"lon":'+str(pt[0])+',"type":"'+type+'"},'  
        strr = strr[:-1]
        data = '{"locations":['+str(strr)+'],"format": "osrm","costing": "auto","costing_options":{"auto":{"shortest":true}},"banner_instructions": true,"language": "sk-SK"}'

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == 200:
            response_text = json.loads(r.text)
            geometry = response_text['routes'][0]['geometry']
            geometries.append(geometry)
        else:
            print(f"bad thing happened {r.content}")
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

data, coords = open_file('test.geojson')
geometries = route(coords,"trough")
body = []
for geometry in geometries:
    body.append(decode_polyline(geometry))
body = [item for sublist in body for item in sublist]
nieco = {u"type": u"LineString", u"coordinates": body}
print(str(nieco).replace("'",'"'))


