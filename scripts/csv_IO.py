import csv
from os.path import exists
from os import path


def load_points_hodinky(filename):
    with open(filename,'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        coords = []
        for i,row in enumerate(spamreader):
            if  i != 0:  # if speed wasnt 0  -> row[7] != "0.0" and
                coords.append([float(row[5][:-1]),float(row[4][:-1])]) ## -1 lebo treba odstranit E alebo N
        return coords
    
def load_points_mobil(filename):
    with open(filename,'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        coords = []
        for i,row in enumerate(spamreader):
            if  i != 0:  # if speed wasnt 0  -> row[7] != "0.0" and
                coords.append([float(row[2]),float(row[1])])
        return coords
    
def save(filename,data):
    with open(filename,'w') as file:
        file.write(str(data))
        file.close()

def save_to_search(filename,track_id,data):
    data = '{"geometry": {"coordinates": '+str(data)+',"type": "LineString"},"properties": {},"type": "Feature"}'
    
    if not exists(filename):
        file = open(filename,'a')
        file.write("route;track\n")
        file.write(track_id+";"+data+"\n")
        file.close()
    else:
        file = open(filename,'a')
        file.write(track_id+";"+data+"\n")
        file.close()

def create_file_for_db(filename,data,track): # na konci to hodi error lebo sa bude snazit nacitt prazdny riadok
    for i in range(len(data)):
        if not exists(filename):
            file = open(filename,'a')
            file.write("track,lat,lon\n")
            file.write(track+","+str(data[i][1])+","+str(data[i][0])+"\n")
            file.close()
        else:
            file = open(filename,'a')
            file.write(track+","+str(data[i][1])+","+str(data[i][0])+"\n")
            file.close()


    

def save_points_to_geojson(filename,data):
    pred = '{"type": "FeatureCollection",  "features": [{"type": "Feature","properties": {},"geometry":'
    nieco = {u"type": u"LineString", u"coordinates": data}
    po =    '}]}'
    save(filename,(str(pred)+str(nieco)+str(po)).replace("'",'"'))