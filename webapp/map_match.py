import sys, os, csv, requests, json
from os import path
from os.path import exists

## Path = "C:/Users/richard.buri/search_web/python/test/"

## Save map matched data to a csv file
def create_file_for_db(filename,data,track,user,zip_name): 
    base_folder = "routes" # folder in which users routes will be stored

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    if not path.exists(path.join(base_folder,user)):
        os.makedirs(path.join(base_folder,user))

    if not path.exists(path.join(base_folder,user,zip_name)):
        os.makedirs(path.join(base_folder,user,zip_name))

    write_header = not exists(path.join(base_folder,user,zip_name,filename))    
    file = open(path.join(base_folder,user,zip_name,filename),'a')
    if write_header:
        file.write("track,lat,lon")
    for i in range(len(data)):
        file.write("\n"+track+"_0,"+str(data[i][1])+","+str(data[i][0]))
    file.close()
 
## Save points for easy displaying
def save_points_to_geojson(filename,data):
    head = '{"type": "FeatureCollection",  "features": [{"type": "Feature","properties": {},"geometry":'
    body = {u"type": u"LineString", u"coordinates": data}
    tail =    '}]}'
    data = (str(head)+str(body)+str(tail)).replace("'",'"')
    with open(filename,'w') as file:
        file.write(str(data))
        file.close()

## Decode polyline
def decode_polyline(polyline):
    points = []
    index = lat = lng = 0

    while index < len(polyline):
        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lat += (~result >> 1) if (result & 1) != 0 else (result >> 1)

        result = 1
        shift = 0
        while True:
            b = ord(polyline[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1F:
                break
        lng += ~(result >> 1) if (result & 1) != 0 else (result >> 1)
        # Valhala uses 6 point precision instead of 5
        points.append([round(lng * 1e-6, 6), round(lat * 1e-6, 6)])
    return points 

## Map match the points
def map_match(points,container_name,costing):
    strr = ""
    for pt in points:
        strr += '{"lat":'+str(pt[1])+',"lon":'+str(pt[0])+'},'
    strr = strr[:-1]

    meili_coordinates = strr
    meili_head = '{"shape":['
    meili_tail = """],"search_radius": 300, "shape_match":"map_snap", "costing": \""""+costing+"""\",  "format":"osrm"}"""
    meili_request_body = meili_head + meili_coordinates + meili_tail
    port = 8002
    url = f"http://{container_name}:{port}/trace_route"
    headers = {'Content-type': 'application/json'}
    data = str(meili_request_body)

    r = requests.post(url, data=data, headers=headers)

    if r.status_code == 200:
        response_text = json.loads(r.text)
        return response_text['matchings'][0]['geometry']
    else:
        print(f"Request did not succeed {r.content}")
        return None

## Get points from csv file, which must be in "lon,lat" structure
def load_points(filename): 
    with open(filename,'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        coords = []
        for i,row in enumerate(spamreader):
            if  i != 0: 
                coords.append([float(row[0]),float(row[1])])
        return coords

## Get points from geojson file
def load_points_from_geojson(file):
    f = open(file, "r")
    text = f.read()
    data = json.loads(text)
    features = data['features']
    feature = features[0]
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    f.close()
    return  coordinates


def folder_process(dir, container_name, user, zip_name):
    ## Check if path contains files as it should
    if len(os.listdir(dir)) != 2:
        print("The directory should have 2 subdirectiries \"Walk\" and \"Drive\"")
        return
    for subdir in os.listdir(dir):
        if not path.isdir(path.join(dir,subdir)):
            print(f"{dir}/{subdir} is not a directory.")
            return
        if subdir not in ['Walk','Drive']:
            print(f"{subdir} does not match the specified subdirectory name \"Walk\" or \"Drive\"")
            return
        

    for subdir in os.listdir(dir):
        for file in os.listdir(path.join(dir,subdir)):
            ## Get points from file
            format = os.path.splitext(file)[1]
            if format == ".csv":
                points = load_points(path.join(dir,subdir,file))
            if format == ".geojson":
                points = load_points_from_geojson(path.join(dir,subdir,file))

            ## MAPMATCH
            geometry = None
            if subdir == "Walk":
                geometry = map_match(points,container_name,costing = "pedestrian")
            if subdir == "Drive":
                geometry = map_match(points,container_name, costing = "auto")
            if geometry != None:
                name = file[:str(file).find(".")]
                pts = decode_polyline(geometry)
                create_file_for_db("database.csv",pts,name,user,zip_name)
                create_file_for_db("database_original.csv",points,name,user,zip_name)
            else:
                print(f"{file} could not been map matched.")

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("Specify path, valhalla container name, file format")
    else:
        dir = sys.argv[1]
        container_name = sys.argv[2]
        user = sys.argv[3]
        zip_name = sys.argv[4]
        folder_process(dir,container_name,user,zip_name)
        