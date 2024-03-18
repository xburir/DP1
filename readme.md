# Web application for showing GPS routes and map-matching

## Bridge

### Create bridge

```
docker network create BRIDGE_NAME --driver bridge
ex: docker network create web_server --driver bridge
```

### To check bridge

```
docker inspect BRIDGE_NAME
ex: docker inspect web_server
```

## Web application container

### Create web application image

```
docker build -t IMAGE_NAME .
ex: docker build -t dp_webapp .
```

### Run container

```
docker run -dit --name CONTAINER NAME --network BRIDGE_NAME -p PORT:PORT -v PATH:/PATH IMAGE_NAME
ex: docker run -dit --name dp_webapp --network web_server -p 8090:8090 -v C:\Users\richard.buri\Desktop\docker\DP1:/DP1 dp_webapp
```

### Exec container

You can either exec the container from Docker Desktop or run it from CLI:

```
docker container exec -it CONTAINER_NAME /bin/bash
ex: docker container exec -it dp_webapp /bin/bash
```

### After container is running

Some commands to execute in bash

```
service mysql start
mysql < db.sql   
```

### To start the webapp

Note: the port must be the same as entered when running the container.

```
PORT=8090 npm run start
```

## Valhalla container

You can run the container either with a linked directory, in which you have downloaded your maps or you can run the container with a one line command which downloads the latest map specified by url (slower). The first startup of the container can take a while (several minutes), see the logs until the output says `INFO: Found config file. Starting valhalla service!`.

### Linked directory

```
docker run -dit --name CONTAINER_NAME --network BRIDGE_NAME -p PORT:PORT -v PATH\custom_files:/custom_files ghcr.io/gis-ops/docker-valhalla/valhalla:latest
ex: docker run -dit --name valhalla --network web_server -p 8002:8002 -v C:\Users\richard.buri\search_web\doker\custom_files:/custom_files ghcr.io/gis-ops/docker-valhalla/valhalla:latest
```

### One line

```
docker run -dit --name CONTAINER_NAME --network BRIDGE_NAME -p PORT:PORT -e tile_urls=MAP_URL ghcr.io/gis-ops/docker-valhalla/valhalla:latest
ex: docker run -dit --name valhalla --network web_server -p 8002:8002 -e tile_urls=https://download.geofabrik.de/europe/slovakia-latest.osm.pbf ghcr.io/gis-ops/docker-valhalla/valhalla:latest
```

Note: If you choose CONTAINER_NAME or PORT different than the one in example, you will have to change the `port` variable in `map_match.py` in `map_match` function, and `valhalla_container_name` variable in `upload.js` in `handleUploadAndUnzip` function.

## Uploaded files structure

### ZIP file

The zip file should contain 2 directories 'Drive' and 'Walk'. The structure should look like this:

        |-- Drive
        |   |-- 33718.csv
        |   |-- 31783.geojson
        |-- Walk
        |   |-- 93293.csv
        |   |-- 44352.csv
        |   |-- 764555.geojson
        |   |-- 354852.csv

### GEOjson file

The structure should look like this:

```
{
    "type": "FeatureCollection",
    "features": [
      {
        "geometry": {
          "coordinates": [
            [
              17.073124,
              48.152729
            ],
            [
              17.073124,
              48.152729
            ]
          ],
          "type": "LineString"
        },
        "properties": {},
        "type": "Feature"
      }
    ]
  }
```

### CSV file

The csv file should consist of two columns longitude and latitude.

    lon,lat
    17.07299,48.151611
    17.073095,48.151878
    17.073084,48.15184
    17.073084,48.151733
    17.073048,48.151672
    17.073011,48.151714



## Notes for myself

prepare database with db.sql, maybe need to create root root user or change variables in index.js
you need to register in the app

ERRORS:
(Client does not support authentication protocol requested by server; consider upgrading MySQL client) -> write to mysql -> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

to start server `PORT=8090 npm run start` this will preinstall the dependencies
after depenencies are instlled, you can just `node index.js`

## TODO

- ~~na konci csv suboru nemoze byt prazdny riadok~~
- ~~urobil som to ze prekryvajuce sa trasy zobrazi vsetky v zozname~~
- ~~urobit upload suboru na server v ZIP~~
- ~~zobrazit moje nahrane zip subory~~
- ~~premenovat unzipped priecinok (alebo vymazat) po tom ako sa urobi map match~~
- ~~teraz na stranku sa moze nahrat len ZIP s CSV, je tam moznost aj na geojson, treba otestovat~~
- ~~z nejakeho dovodu sa mi zacyklil asi python script~~
- ~~unzipping empty folder does not create folder~~
- ~~asynchronne urobit upload~~
- ~~cas pri list of files je zly~~
- ~~skusit urobit aby sa pri uploade nerefreshla stranka~~
- ~~nastavit pri uploade nech sa to automaticky posle bez stlacenia tlacidla a potom ked vyjde alert napisat ze musis dat refresh aby sa pridala ta vec do zoznamu~~
- ~~neuspesne rozzipovanie/mapmatchnutie ->nevymazat zip ale zobrazit upozornenie na neskorsie stiahnutie a upravenie zip + tlacidlo znova spustit map match  + downlaod original zip + delete~~
- ~~show -> prepinac~~
- ~~ked pridam zip s jednou fotkou vnutri tak sa tvari ze presiel map match v poriadku~~
- ~~parse zip tak aby nemusli byt oba priecinky, ale sa bral prefix~~
- ~~ked mam nastakovane nejake files zip ktore sa nepodarili a potom sa mi jedno podari tak ostatne sa vymazu~~
- ~~aby sa nemuselo refreshovat po uploade.~~
- ~~prejdem vsetky priecinky (rozzipovane zip), vylistujem na ne dam rerun, potom prejdem vsetky zip a ked sa nenachadzaju v priecinkoch tak pridam, ked ano tak nepridam~~
- ~~pridat .csv aj .CSV~~
- ~~s CSV v zipiande je nejaky problem ktory si myslim ze pred tym nebol.~~
- ~~ked dam rerun a zlyha tak musim refresh stranky?~~
- ~~python script nech neberie stlpce podla [] ale podla toho ci obsahuju LAT / LON~~
- ~~dizajn~~
- ~~ked sa otvori jedno okno nech sa zatvori druhe.~~
- ~~tlacidlo na bad map match~~
- ~~global try catch~~
- ~~nech sa nevypne pri vypnuti DB~~
- ~~chyby z login a register dat na popup ako je pri map match~~
- ~~zmenit db aby brala aj email a taketo srandy z registracie -> nechat len username a heslo, ostatne netreba~~
- ~~po zvoleni zip suboru nascrollovat mapu nejako rozumne~~
- ~~urobit ci matchinguju passwords~~
- ked si to moc oddialim tak mi ukazuje tracks0
- automaticky vymazat rerun dir a zip
- troska upratat ten index.js ten auth
- ked bude csv obsahovat aj cas tak potom array v dict co sa vykresluje na mapu zoradit podla casu.
- ~~po vypnuti okna ktore zobrazuje routes a zapnuti ukazuje, že nie je zobrazena trasa ale je~~
