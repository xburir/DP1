from zahustenie import open_file
import json

data,coords = open_file("11k.geojson")

def skratit():
    
        
    data['features'][0]['geometry']['coordinates'] = coords[:11000]
    f = open("9k.geojson","w")
    json.dump(data,f)
    f.close()

# skratit()
print(len(coords))
