## Docker

Run the following commands in windows powershell or wsl.

### Create image

```
docker build -t IMAGE_NAME .
ex: docker build -t dp_webapp .
```

### Create bridge

```
docker network create BRIDGE_NAME --driver bridge
ex: docker network create web_server --driver bridge
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

## After container is running

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

## 



## Notes for myself

prepare database with db.sql, maybe need to create root root user or change variables in index.js
you need to register in the app

ERRORS:
(Client does not support authentication protocol requested by server; consider upgrading MySQL client) -> write to mysql -> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

to start server `PORT=8090 npm run start` this will preinstall the dependencies
after depenencies are instlled, you can just `node index.js`

## TODO

- zmenit db aby brala aj email a taketo srandy z registracie
- ked bude csv obsahovat aj cas tak potom array v dict co sa vykresluje na mapu zoradit podla casu.
- na konci csv suboru nemoze byt prazdny riadok
- urobil som to ze prekryvajuce sa trasy zobrazi vsetky v zozname
- urobit ci matchinguju passwords
- mozno este urobit nech sa uklada tema do session
- urobit upload suboru na server v ZIP
- zobrazit moje nahrane zip subory
- po zvoleni zip suboru nascrollovat mapu nejako rozumne
- premenovat unzipped priecinok (alebo vymazat) po tom ako sa urobi map match
- teraz na stranku sa moze nahrat len ZIP s CSV, je tam moznost aj na geojson, treba otestovat
- z nejakeho dovodu sa mi zacyklil asi python script
- ked si to moc oddialim tak mi ukazuje tracks0
- skusit mensie datasety