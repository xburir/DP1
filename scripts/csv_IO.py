import csv
from os.path import exists
from os import path


def load_points(filename):
    with open(filename,'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        coords = []
        for i,row in enumerate(spamreader):
            if  i != 0:  # if speed wasnt 0  -> row[7] != "0.0" and
                coords.append([float(row[5][:-1]),float(row[4][:-1])])
        return coords
    
def save(filename,data):
    with open("C:/Users/richard.buri/search_web/python/"+filename,'w') as file:
        file.write(str(data))
        file.close()

def save_to_search(filename,track_id,data):
    data = '{"geometry": {"coordinates": '+str(data)+',"type": "LineString"},"properties": {},"type": "Feature"}'
    
    if not exists("C:/Users/richard.buri/search_web/python/"+filename):
        file = open("C:/Users/richard.buri/search_web/python/"+filename,'a')
        file.write("route;track\n")
        file.write(track_id+";"+data+"\n")
        file.close()
    else:
        file = open("C:/Users/richard.buri/search_web/python/"+filename,'a')
        file.write(track_id+";"+data+"\n")
        file.close()

    

def save_points_to_geojson(filename,data):
    nieco = {u"type": u"LineString", u"coordinates": data}
    save(filename,str(nieco).replace("'",'"'))