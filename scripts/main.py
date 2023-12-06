from csv_IO import load_points,save_points_to_geojson,save_to_search
from map_matching import map_match
from decode_polyline import decode_polyline
import os
from route_between_points import route,remove_duplicite_points

def folder_to_track(dir):
    for file in os.listdir(dir):
        points = load_points(dir+file)
        geometry = map_match(points)
        pts = decode_polyline(geometry,True)
        name = file[:str(file).find(".")]
        save_to_search("my_tracks.csv",name,pts)


dir = "C:/Users/richard.buri/search_web/python/custom_tracks/"
# folder_to_track(dir)


def route_():
    points = load_points(dir+"19141233.csv")
    geometries = route(points,"trough")
    body = []
    for geometry in geometries:
        body.append(decode_polyline(geometry,True))
    body = [item for sublist in body for item in sublist]
    body = remove_duplicite_points(body)
    save_points_to_geojson("testicek.geojson",body)

def map_match_():
    points = load_points(dir+"19141233.csv")
    geometry = map_match(points)
    pts = decode_polyline(geometry,True)
    save_points_to_geojson("testicek.geojson",pts)

def only_points_():
    points = load_points(dir+"19141233.csv")
    save_points_to_geojson("testicek.geojson",points)

only_points_()