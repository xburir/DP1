import requests,json



def route(point1, point2):
    url = "http://localhost:8002/route"
    headers = {'Content-type': 'application/json'}
    data = '{"locations":[{"lat": '+str(point1[1])+',"lon": '+str(point1[0])+'},{"lat": '+str(point2[1])+',"lon": '+str(point2[0])+'}],"format": "osrm","costing": "auto","costing_options":{"auto":{"shortest":true}},"banner_instructions": true,"language": "sk-SK"}'

    r = requests.post(url, data=data, headers=headers)
    # print(data)


    if r.status_code == 200:
        response_text = json.loads(r.text)
        # print(response_text)
        steps = response_text['routes'][0]['legs'][0]['steps']
        points = []
        for step in steps:
            points.append(step['maneuver']['location'])

        
        # return(pred+ str(points)+po)
        return points
    else:
        print(f"bad thing happened {r.content}")

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

def create_points(coords):
    new_coords = []
    for i in range(1,len(coords)):
        new_coords.append(route(coords[i-1],coords[i]))
    return new_coords

# print(route([19.590526,49.098816],[19.590595,49.098896]))

data, coords = open_file('test.geojson')
pts = create_points(coords)
# print(pts)

last_pt = []
points = []
for usek in pts:
    for pt in usek:
        if (pt != last_pt):
            points.append(pt)
            last_pt = pt


pred = '{"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"coordinates":'
po = ',"type": "LineString"}}]}'

print(pred+ str(points),po)