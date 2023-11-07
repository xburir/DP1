def strip(file):
    f = open(file, "r")
    text = f.read()
    i = 0
    while text[i] != ';':
        i+=1
    return(text[i+1:])

def save_geojson(file,content):
    i = 0
    while file[i] != '.':
        i+=1
    name = file[:i]
    filee = open(name+'.geojson','w')
    filee.write(content)
    filee.close() 


def create_json(file):
    pred = '{"type":"FeatureCollection","features":['
    str = strip(file)
    po  = ']}'
    save_geojson( file, pred + str + po )



create_json('search_web.txt')