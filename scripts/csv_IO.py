import csv
from os.path import exists
from os import path
import pandas as pd

def hodinky_to_input(dir,filename):
    df = pd.read_csv(dir+filename)
    df = df[['LONGITUDE E/W','LATITUDE N/S']]
    df = df.rename(columns={'LONGITUDE E/W': 'lon','LATITUDE N/S':'lat'})
    for i, row in df.iterrows():
        df.loc[i,"lon"] = df.loc[i,"lon"][:-1]
        df.loc[i,"lat"] = df.loc[i,"lat"][:-1]
    df.to_csv(dir+""+filename,index=False)


def load_points(filename):
    with open(filename,'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        coords = []
        for i,row in enumerate(spamreader):
            if  i != 0: 
                coords.append([float(row[0]),float(row[1])])
        return coords


def load_points_hodinky(filename):  ##TODO urobit to tak aby sa vyberali columns a nie podla pozicie
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
            file.write(track+"_0,"+str(data[i][1])+","+str(data[i][0])+"\n")
            file.close()
        else:
            file = open(filename,'a')
            file.write(track+"_0,"+str(data[i][1])+","+str(data[i][0])+"\n")
            file.close()


    

def save_points_to_geojson(filename,data):
    pred = '{"type": "FeatureCollection",  "features": [{"type": "Feature","properties": {},"geometry":'
    nieco = {u"type": u"LineString", u"coordinates": data}
    po =    '}]}'
    save(filename,(str(pred)+str(nieco)+str(po)).replace("'",'"'))