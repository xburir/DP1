import sys, os, csv, requests, json, re
from os import path
from os.path import exists

## Path = "C:/Users/richard.buri/search_web/python/test/"

## Save map matched data to a csv file
def create_file_for_db(data,track,user,zip_name,type): 
    base_folder = "routes" # folder in which users routes will be stored

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    if not path.exists(path.join(base_folder,user)):
        os.makedirs(path.join(base_folder,user))

    if not path.exists(path.join(base_folder,user,zip_name)):
        os.makedirs(path.join(base_folder,user,zip_name))

    if not path.exists(path.join(base_folder,user,zip_name,track)):
        os.makedirs(path.join(base_folder,user,zip_name,track))
   
    file = open(path.join(base_folder, user, zip_name, track, type),'w')
    file.write("track,lat,lon")
    for i in range(len(data)):
        file.write("\n"+track+","+str(data[i][1])+","+str(data[i][0]))
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
    try:
        r = requests.post(url, data=data, headers=headers)
        if r.status_code == 200:
            response_text = json.loads(r.text)
            return "SUCESS;",response_text['matchings'][0]['geometry']
        else:
            return f"ERROR;{r.content}",None
    except:
        return "Error;Request did not succeed.",None

## Remove any letters from lat/lon
def clean_value(value):
    return re.sub(r'[^0-9.-]', '', value)

## Get points from csv file, which must be in "lon,lat" structure
def load_points(filename): 
    with open(filename, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        header = next(spamreader)  # Read the header row
        lat_index = None
        lon_index = None
        
        # Find the indices of columns containing "lat" and "lon"
        for i, col in enumerate(header):
            if 'lat' in col.lower():
                lat_index = i
            elif 'lon' in col.lower():
                lon_index = i
                
        # Check if both "lat" and "lon" columns are found
        if lat_index is None or lon_index is None:
            return None
        
        coords = []
        for row in spamreader:
            lat_value = clean_value(row[lat_index])
            lon_value = clean_value(row[lon_index])
            coords.append([float(lon_value), float(lat_value)])
            
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
    successful = []
    failed = {}
    retDict = {}

    ## Check if path contains files as it should
    for subdir in os.listdir(dir):
        if not path.isdir(path.join(dir,subdir)):
            failed['General'] = f"{subdir} is not a directory, check the zip structure."
            retDict["failed"] = 1
            retDict["failed_info"] = failed
            print(json.dumps(retDict))
            return
        if subdir not in ['Walk','Drive']:
            failed['General'] = f"{subdir} does not match the specified directory name \"Walk\" or \"Drive\", check the zip structure."
            retDict["failed"] = 1
            retDict["failed_info"] = failed
            print(json.dumps(retDict))
            return

    for subdir in os.listdir(dir):
        for file in os.listdir(path.join(dir,subdir)):
            ## Get points from file
            format = os.path.splitext(file)[1]
            name = file[:str(file).find(".")]

            if format.lower() == ".csv":
                points = load_points(path.join(dir,subdir,file))
            elif format.lower() == ".geojson":
                points = load_points_from_geojson(path.join(dir,subdir,file))
            else:
                failed[name] = f"Points couldn't be extracted."
            
            if points == None:
                failed[name] = f"Points couldn't be extracted."
            
            ## MAPMATCH
            geometry = None
            status = None
            if subdir == "Walk":
                status, geometry = map_match(points,container_name,costing = "pedestrian")
            if subdir == "Drive":
                status, geometry = map_match(points,container_name, costing = "auto")
            if geometry != None:
                pts = decode_polyline(geometry)
                create_file_for_db(pts,name,user,zip_name,"map-match.csv")
                create_file_for_db(points,name,user,zip_name,"original.csv")
                successful.append(name)
            else:
                failed[name] = status.split(";")[1]
    
    retDict["failed"] = len(failed)
    retDict["successful"] = len(successful)
    retDict["failed_info"] = failed

    print(json.dumps(retDict))

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("ERROR;Specify path, valhalla container name, file format.")
    else:
        dir = sys.argv[1]
        container_name = sys.argv[2]
        user = sys.argv[3]
        zip_name = sys.argv[4]
        folder_process(dir,container_name,user,zip_name)
        