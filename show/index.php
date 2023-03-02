<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta content="Bio inspired tracks comparison" name="description">
    <meta content="mComputing.eu, Maros Cavojsky" name="author">

    <title>Search</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">

    <script src="js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/L.Control.Sidebar.css" />
    <script src="js/L.Control.Sidebar.js"></script>

    <style>
        html, body {
        height: 100%;
        }
        body {
        text-align: center;
        }
        #map {
            height: 100%;
            width: 100%;
        }
       .alg-form input{
            width: 65px !important;
       }
    
    </style>

</head>

<body>

<div id='map'></div>

<div class="container" id="sidebar">
    
    <div class="row">
        <div class="col-lg-12">
                <h3>Parameters</h3>
                <a class="close" onclick="sidebar.hide()">x</a>
                <form class="form-inline alg-form">
                    <p>                   
                        <strong>Box count: <span id="psize">0</span></strong>
                    </p>
                   
                    <br>
                    <div class="form-group">
                        <label class="sr-only" for="gsStart">Start </label>
                        <div class="input-group">
                            <div class="input-group-addon">Start</div>
                            <div class="input-group-addon">&le;</div>
                            <input type="number" class="form-control" id="gsStart" placeholder="1" size="1" value="3" min="1"/>
                        
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="sr-only" for="gsEnd">End</label>
                        <div class="input-group">
                            <div class="input-group-addon">End</div>
                            <div class="input-group-addon">&ge;</div>
                            <input type="number" class="form-control" id="gsEnd" placeholder="1" size="1" value="2"/>
                        </div>
                    </div>
                  
                    <div class="form-group">
                        <label class="sr-only" for="gsMatch">Matches</label>
                        <div class="input-group">
                            <div class="input-group-addon">Matches</div>
                            <div class="input-group-addon">&ge;</div>
                            <input type="number" class="form-control" id="gsMatch" placeholder="" size="1"/>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="sr-only" for="gaps">Gaps</label>
                        <div class="input-group">
                            <div class="input-group-addon">Gaps</div>
                            <div class="input-group-addon">&le;</div>
                            <input type="number" class="form-control" id="gaps" placeholder="" size="1"/>
                        
                        </div>
                    </div>
                    
                </form>
                
        </div> 
    </div>
    <div class="row">
        <div class="col-lg-12">
            <h3>Results</h3>
            <p> Draw at least 2 areas of interest, in right order. </p>
        

            <div id="resultsbox" style="display: none; ">
                <p>Found <span id="totalfound"></span> - <button onclick="showAll()">Show all</button></p>
                <div id="pathbox"></div>
                <div style="height: 400px; overflow-y:auto;">
                    <table class="table" id="datatable">
                    <thead>
                        <tr>
                        <th data-tablesort-type="int">#</th>
                        <th data-tablesort-type="int">Match</th>
                        <th data-tablesort-type="int>">Start</th>
                        <th data-tablesort-type="int">End</th>
                        <th data-tablesort-type="int">Gap</th>
                        </tr>
                    </thead>
                    <tbody id="results">
                    </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <div style="position: absolute; bottom: 0;">
       
        <div class="col-lg-12">
            <a href="https://mcomputing.eu">Algorithm &copy; mcomputing.eu</a> <br>
            <a href="nwa.php">Needleman–Wunsch</a> |
            <a href="swa.php">Smith–Waterman</a>
        </div>
    </div>

</div>


    <link href="https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css">
    <script src="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js"></script>
    <script src="https://npmcdn.com/leaflet-geometryutil"></script>
    <script src="js/geohash.js"></script>

    <script>
    var map = L.map('map').setView([39.93685568995833, 116.37027740478517], 13);
    //var map = L.map('fa-star', {scrollWheelZoom: false}).setView([39.93685568995833, 116.37027740478517], 13);

    var gdata;
    var resultGroup = [];
    var pattern =  L.polyline([], {color: 'red'}).addTo(map);
    var preview = L.polyline([], {color: 'red'}).addTo(map);
    var isDrawingPattern = false;
    var geoPattern = null , geoResult = null, geoAllResult = null;
    var distance = 0;
    var lastLat = 0;
    var lastLon = 0;
    var lastpos = null;
    var interpolated = [];
    var boxes = [];

    var patternStyle = {
        "color": "#e20fcd",
        "weight": 5
    };

    
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFyb3NjIiwiYSI6ImNrb3B4b2QxeTBweG0ycWw0bTBiYWVwcWgifQ.g79td3RKqhZ9DEOLF9nGlA', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>, <a href="https://www.microsoft.com/en-us/download/details.aspx?id=52367">Geolife Data set</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);

    var sidebar = L.control.sidebar('sidebar', {
        position: 'left'
    });

    map.addControl(sidebar);
   
    L.easyButton('fa-repeat', function(btn, map){
        clearSearch();
    }).addTo( map );

    L.easyButton('fa-search', function(btn, map){
        sidebar.toggle();
    }).addTo( map );

    function clearSearch(){
        for (var i in boxes){
                boxes[i].removeFrom(map);
        }
        boxes = [];
        interpolated = [];
        $("#psize").html("0");
        $("#resultsbox").hide();

        if (geoAllResult!=null){
            map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
    }

    function addToPath(latlng){
        var hash = encodeGeoHash(latlng.lat,latlng.lng,7);
        interpolated.push(hash);
        $("#psize").html(interpolated.length);
        var box = decodeGeoHash(hash);
        var rect = L.rectangle([[box['latitude'][0],box['longitude'][0]],[box['latitude'][1],box['longitude'][1]]], {color: "#ff7800", weight: 1});
        rect.bindPopup("Box "+(boxes.length+1)+" <br> <a href='#'>Remove</a>");   
        boxes.push(rect);
        rect.addTo(map);

        
        $("#gsMatch").val(Math.max(1,Math.floor(boxes.length*0.8)));
        $("#gaps").val(Math.round(boxes.length*0.2));
    }

    function onMapClick(e) {
        addToPath(e.latlng);
        findPaths(); 
    }

    function onMapDoubleClick(e) {
       
    }

    function onMapMouseMove(e) {
        
    }

    map.on('click', onMapClick);

    // var paramType = 0;
    // $('input[name="paramtype"]').on('click change', function(e) {
    //     paramType = $(this).filter(":checked").val();
    //     if (paramType == 0){
            
    //     }else{
    //         var match = interpolated.length*(parseInt($("#gsMatchP").val())/100);
    //         var start = interpolated.length*(parseInt($("#gsStartP").val())/100);
    //         var end =  interpolated.length*(parseInt($("#gsEndP").val())/100);
    //         var gaps = interpolated.length*(parseInt($("#gapsP").val())/100);
    //         $("#gsMatch").val(Math.floor(match));
    //         $("#gsStart").val(Math.floor(start));
    //         $("#gsEnd").val(Math.floor(end));
    //         $("#gaps").val(Math.floor(gaps));
    //     }
    // });
   
   
    function showResults(){
        
        $("#resultsbox").show();
        var x = "";
        for (var i in gdata){
            x+= "<tr><td><button onclick=\"showTrack("+i+")\">"+i+"</button></td><td>"+gdata[i][1]+"</td><td>"+gdata[i][2]+"</td><td>"+gdata[i][3]+"</td><td>"+gdata[i][4]+"</td></tr>";
        }
        $("#totalfound").html(gdata.length);
        $("#results").html(x);
        // $("#datatable").tablesorter({
        //     theme : 'blue'
        // });
    }

    function showTrack(id){
        if (geoAllResult!=null){
            map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        geoResult = L.geoJSON(JSON.parse(gdata[id][6]), {
                style: function (feature) {
                    return {fill: false, fillOpacity: 0.6, stroke: true};
                }
        });   
        geoResult.addTo(map);

        $("#pathbox").html(JSON.stringify(gdata[id][5]));

    }

    function showAll(){
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        geoAllResult.addTo(map);
    }

    function findPaths(){
        if (interpolated.length<2){
            return;
        }
        $.ajax({
            method: "POST",
            url: "geohash_py.php",
            dataType: "json",
            data: {"pattern": interpolated, "match": $("#gsMatch").val(), "start": $("#gsStart").val(), "end": Math.max(0,interpolated.length+1-parseInt($("#gsEnd").val())), "gap": $("#gaps").val()}
        })
        .done(function (json) {
            console.log(json);
            gdata = json;
            showResults();
            if (geoAllResult!=null){
                map.removeLayer(geoAllResult);
            }
            geojson = {
                "type": "FeatureCollection",
                "features": json.map(function myFunction(item) { return JSON.parse(item[6]);})
            };
            console.log(geojson);
            geoAllResult = L.geoJSON(geojson, {
                style: function (feature) {
                    return {fill: false, fillOpacity: 0.6, stroke: true};
                }
            });   
            geoAllResult.addTo(map);
            
            for (var i in boxes){
                boxes[i].removeFrom(map);
                boxes[i].addTo(map).bindPopup("Box "+(parseInt(i)+1)+" <br> <a href='#' onclick='removeBox("+i+")'>Remove</a>");
            }
        });

    }

</script>
<script src="js/jquery.tablesorter.min.js"></script>
<link rel="stylesheet" href="css/theme.blue.css"/>

<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="js/ie10-viewport-bug-workaround.js"></script>

</body>
</html>
