from csv_IO import load_points_hodinky,save_points_to_geojson,save_to_search,load_points_mobil,create_file_for_db,hodinky_to_input,load_points
from map_matching import map_match
from decode_polyline import decode_polyline
import os
from os import path
from route_between_points import route,remove_duplicite_points

def folder_process(dir):
    for file in os.listdir(dir):
        if not path.isdir(dir+file):
            ## Convert CSV from GPS watch to desirable format
            # hodinky_to_input(dir,file)

            ## Load points and prepare output folder
            points = load_points(dir+file)
            name = file[:str(file).find(".")]
            output_folder_path = os.path.join(dir, name + "_output")
            os.makedirs(output_folder_path, exist_ok=True)

            ## MAPMATCH
            geometry = map_match(points)
            if geometry != None:
                pts = decode_polyline(geometry,True)
                save_points_to_geojson(output_folder_path+"/"+name+"_map_match.geojson",pts)

                ## track for SEARCH WEB
                # save_to_search(dir+"track.csv",name,pts)
                create_file_for_db(dir+"database.csv",pts,name)

            ## ROUTE
            # geometries = route(points,"trough")
            # body = []
            # for geometry in geometries:
                # body.append(decode_polyline(geometry,True))
            # body = [item for sublist in body for item in sublist]
            # save_points_to_geojson(output_folder_path+"/"+name+"_route.geojson",body)
            # body = remove_duplicite_points(body)
            # save_points_to_geojson(output_folder_path+"/"+name+"_route_WO_dup_points.geojson",body)

            ## ORIGINAL POINTS
            save_points_to_geojson(output_folder_path+"/"+name+"_original.geojson",points)

        


dir = "C:/Users/richard.buri/search_web/python/hodinky/"


def route_():
    points = load_points_hodinky(dir+"19141233.csv")
    geometries = route(points,"trough")
    body = []
    for geometry in geometries:
        body.append(decode_polyline(geometry,True))
    body = [item for sublist in body for item in sublist]
    body = remove_duplicite_points(body)
    save_points_to_geojson("testicek.geojson",body)

def map_match_():
    points = load_points_hodinky(dir+"19141233.csv")
    geometry = map_match(points)
    pts = decode_polyline(geometry,True)
    save_points_to_geojson("testicek.geojson",pts)

def only_points_():
    points = load_points_hodinky(dir+"19141233.csv")
    save_points_to_geojson("testicek.geojson",points)


folder_process(dir)