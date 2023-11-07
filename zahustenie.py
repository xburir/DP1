import json

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

def zahustenie(coords):
    new_coords = []
    for i in range(len(coords)):
        if (i != 0):
            new_coord = [(coords[i-1][0]+coords[i][0])/2.0,(coords[i-1][1]+coords[i][1])/2.0]
            new_coords.append(new_coord)
        new_coords.append(coords[i])
    return new_coords

def zahustit(filename, count):
    
    data,coords = open_file(filename+".geojson")
    
    for _ in range(count):
        coords = zahustenie(coords)

    data['features'][0]['geometry']['coordinates'] = coords
    f = open(filename+"_zahustene.geojson","w")
    json.dump(data,f)
    f.close()


zahustit("search_web",3)