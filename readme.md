
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