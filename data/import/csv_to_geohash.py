import pandas as pd
import libgeohash as gh
from sqlalchemy import create_engine
import geojson
import csv

def csvToGeohash():
    df = pd.read_csv("/home/data/import/files/data.csv")
    df = df.fillna('')
    #path.csv
    df['geohash'] = df.apply(
        lambda row: gh.encode(row['lat'], row['lon'], precision=7),
        axis=1
    )

    df_path = df[['geohash', 'track']]
    df_path.to_csv("/home/data/import/files/path.csv", index=False)
    
    #track.csv
    tracks = []
    for id, values in df.groupby('track'):
        tracks.append([id, str(geojson.Feature(geometry=geojson.LineString(values[["lon", "lat"]].values.tolist())))])
        
    df_track = pd.DataFrame(tracks, columns=['route', 'track'])
    df_track.to_csv("/home/data/import/files/track.csv", index=False, sep=';', quoting=csv.QUOTE_NONE)
    
    #latlon_median.csv
    df_lat_mean = df["lat"].median()
    df_lon_mean = df["lon"].median()
    median_export = []
    median_export.append([df_lat_mean, df_lon_mean])
    df_median = pd.DataFrame(median_export, columns=['lat', 'lon'])
    df_median.to_json("/var/www/html/js/latlon_median.json")
    
if __name__ == '__main__':
    csvToGeohash()