import json
from distance import haversine

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

def zahustenie2(coords,dist):
    new_coords = []
    flag = False
    for i in range(len(coords)):
        if (i != 0):
            if (haversine(coords[i-1][0],coords[i-1][1],coords[i][0],coords[i][1]) > dist):
                flag = True
                new_coord = [(coords[i-1][0]+coords[i][0])/2.0,(coords[i-1][1]+coords[i][1])/2.0]
                new_coords.append(new_coord)
            
        new_coords.append(coords[i])
    return new_coords, flag

def zahustit(filename, count):
    data,coords = open_file(filename+".geojson")
    for _ in range(count):
        coords = zahustenie(coords)

    data['features'][0]['geometry']['coordinates'] = coords
    f = open(filename+f"_dns1_{count}.geojson","w")
    json.dump(data,f)
    f.close()

def zahustit2(filename, dist):
    data,coords = open_file(filename+".geojson")
    while True:
        coords, flag = zahustenie2(coords,dist)
        if flag == False:
            break

    data['features'][0]['geometry']['coordinates'] = coords
    f = open(filename+f"_dns2_{dist}m.geojson","w")
    json.dump(data,f)
    f.close()


def insert_points(original_points, max_distance):
    new_points = [original_points[0]]  # Start with the first point

    for i in range(1, len(original_points)):
        # Check the distance between consecutive points
        distance = haversine(original_points[i - 1][0], original_points[i - 1][1],
                             original_points[i][0], original_points[i][1])

        if distance > max_distance:
            # Calculate the number of new points to insert
            num_new_points = int(distance / max_distance)
            
            # Calculate the step size for inserting new points
            step_lat = (original_points[i][0] - original_points[i - 1][0]) / (num_new_points + 1)
            step_lon = (original_points[i][1] - original_points[i - 1][1]) / (num_new_points + 1)

            # Insert the new points
            for j in range(1, num_new_points + 1):
                new_lat = original_points[i - 1][0] + j * step_lat
                new_lon = original_points[i - 1][1] + j * step_lon
                new_points.append((new_lat, new_lon))

        new_points.append(original_points[i])

    return new_points

def zahustit3(filename, dist):
    data,coords = open_file(filename+".geojson")
    oldpoints = len(coords)
    coords = insert_points(coords,dist)

    if(len(coords) > 16000):
        print("Coords for VALHALLA map matching API must not have more then 16k shape points")
    else:
        print(f"Densified, old points({oldpoints}, new points({len(coords)}))")
        data['features'][0]['geometry']['coordinates'] = coords
        f = open(filename+f"_dns3_{dist}m.geojson","w")
        json.dump(data,f)
        f.close()


# zahustit("220_69",2)
zahustit3("220_69",8)