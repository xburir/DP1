import pandas as pd
import libgeohash as gh
from sqlalchemy import create_engine
import geojson
import csv
import mysql.connector
import sys
import json

def csvToGeohash(csvPath, dbName, title):
    df = pd.read_csv(csvPath)
    df = df.fillna('')
    #path.csv
    df['geohash'] = df.apply(
        lambda row: gh.encode(row['lat'], row['lon'], precision=7),
        axis=1
    )

    df_path = df[['geohash', 'track']]
    df_path.to_csv("/home/data/import/files/"+dbName+"_path.csv", index=False)
    
    #track.csv
    tracks = []
    for id, values in df.groupby('track'):
        tracks.append([id, str(geojson.Feature(geometry=geojson.LineString(values[["lon", "lat"]].values.tolist())))])
        
    df_track = pd.DataFrame(tracks, columns=['route', 'track'])
    df_track.to_csv("/home/data/import/files/"+dbName+"_track.csv", index=False, sep=';', quoting=csv.QUOTE_NONE)
    
    #latlon_median.csv
    mapconfig = {"center":{"lat": df["lat"].median(), "lon": df["lon"].median()}, "title": title, "dbname": dbName, "attribution": ""}
    with open("/var/www/html/center/"+dbName+".json", 'w') as outfile:
        outfile.write(json.dumps(mapconfig))
    # df_lat_mean = df["lat"].median()
    # df_lon_mean = df["lon"].median()
    # median_export = []
    # median_export.append([df_lat_mean, df_lon_mean])
    # df_median = pd.DataFrame(median_export, columns=['lat', 'lon'])
    # df_median.to_json("/var/www/html/center/"+dbName+".json")

def importData(dbName):
    mydb = mysql.connector.connect(
        host="localhost",
        user="search",
        password="password"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS `"+dbName+"` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    mycursor.close()
    mydb.disconnect()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database=dbName,
        allow_local_infile=True
    )
    mycursor = mydb.cursor()
    mycursor.execute("DROP TABLE IF EXISTS `path`;")
    mycursor.execute("CREATE TABLE `path` (`id` int(11) NOT NULL AUTO_INCREMENT,`hash` varchar(7) NOT NULL,`track` varchar(80) NOT NULL, PRIMARY KEY (`id`), KEY `ihash` (`hash`)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;")
    mycursor.execute("DROP TABLE IF EXISTS `tracks`;")
    mycursor.execute("CREATE TABLE `tracks` ( `route` varchar(250) NOT NULL, `track` mediumtext NOT NULL, PRIMARY KEY (`route`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    
    mycursor.execute("SET GLOBAL local_infile=1;")
    mycursor.execute("load data local infile '/home/data/import/files/"+dbName+"_path.csv' into table `path` fields terminated by ',' lines terminated by '\n' ignore 1 lines (`hash`, `track`);")
    mycursor.execute("load data local infile '/home/data/import/files/"+dbName+"_track.csv' into table `tracks` fields terminated by ';' lines terminated by '\n' ignore 1 lines (`route`, `track`);")
    mydb.commit()
    mycursor.close()
    mydb.disconnect()
    
    
if __name__ == '__main__':
    if len(sys.argv)<3:
        print("Specify path to CSV and dbName")
    else:
        title = sys.argv[2] if len(sys.argv)==3 else sys.argv[3]
        csvToGeohash(sys.argv[1], sys.argv[2], title)
        importData(sys.argv[2])
        print("Finished")