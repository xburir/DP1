<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="shortcut icon" type="image/x-icon" href="favicon.png" />
    <meta charset="utf-8">
    <meta content="IE=edge" http-equiv="X-UA-Compatible">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta content="Bio inspired tracks comparison" name="description">
    <meta content="mComputing.eu, Maros Cavojsky" name="author">

    <title>Search</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href="css/toastr.css" rel="stylesheet"/>

    <script src="js/ie-emulation-modes-warning.js"></script>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/L.Control.Sidebar.css" />
    <script src="js/L.Control.Sidebar.js"></script>
    <script src="https://canvasjs.com/assets/script/jquery-1.11.1.min.js"></script>
    <script src="https://canvasjs.com/assets/script/jquery.canvasjs.min.js"></script>
    <script src="js/toastr.js"></script>

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

       html * {
            font-size: 14px;
            color: #2020131;
            font-family: 'Roboto', sans-serif;

        }
    </style>

</head>

<body>

<div id='map'></div>

<div class="container" id="sidebar">
    <div class="row">
        <div class="col-lg-12">
                <!-- <h1>Parameters</h1> -->
                <a class="close" onclick="sidebar.hide()">x</a>
                <form class="form-inline alg-form">
                    <h1>                   
                        <strong style="font-size: 24px;">Boxes drawn: <span id="psize" style="font-size: 24px;">0</span></strong>
                    </h1>
                   
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
                <div style="margin-top: 2%; margin-bottom: 5%;"><button class="btn btn-success" onclick="findPaths()">Apply</button></div>
        </div> 
    </div>
    <div class="row">
        <div class="col-lg-12">
            <div id="resultsbox" style="display: none;">
                <p>Found <span id="totalfound"></span> - <button class="btn btn-secondary" onclick="showAll()">Show all</button></p>
                <div style="height: fit-content; overflow-y:auto;">
                    <table class="table" id="datatable">

                    <tbody id="results">
                    </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <div style="position: relative; bottom: 0%; margin-top:10%">
        <div class="col-lg-12">
            <a href="https://mcomputing.eu">Algorithm &copy; mcomputing.eu</a> <br>
            <a href="nwa.php">Needleman–Wunsch</a> |
            <a href="swa.php">Smith–Waterman</a>
        </div>
    </div>

</div>

<div class="container" id="sidebarRight">
    <div class="row">
        <div class="col-lg-12">
                <a class="close" onclick="sidebarRight.hide()">x</a>
        </div> 
    </div>
    <div class="row">
        <div class="col-lg-12" id="chartContainer" style="height: 300px; width: 90%; margin-top: 5%;"></div>
    </div>  
    <div class="row">
        <div class="col-lg-12" id="chart2Container" style="height: 300px; width: 90%; margin-top: 5%;"></div>
    </div>
    <div style="position: relative; bottom: 0%; margin-top:10%">
        <div class="col-lg-12">
            <h1 style="font-size: 18px;">Click on individual columns to show or hide selected values on the map</h1>
        </div>
    </div>
</div>


    <link href="https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css">
    <script src="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js"></script>
    <script src="https://npmcdn.com/leaflet-geometryutil"></script>
    <script src="js/geohash.js"></script>


    <script>
    var chart = new CanvasJS.Chart("chartContainer", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        animationEnabled: true,
        zoomEnabled: true,
        title: {
            text: "Number of trajectories found per selected point",
            fontFamily: "Roboto, sans-serif",
            fontWeight: "lighter"
        },
        axisX:{
            valueFormatString: "#",
            interval: 1
        },
        axisY:{
            valueFormatString: "#",
            interval: 10
        },
        data: [{
            type: "column",
            color: "#1959d1",
            click: function(e){
                showSelectedColumnPerPoint(e.dataPoint.x);
            },
            dataPoints: dps
        }]
    });

    var chart2 = new CanvasJS.Chart("chart2Container", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        animationEnabled: true,
        zoomEnabled: true,
        title: {
            text: "Number of trajectories passing through number of boxes",
            fontFamily: "Roboto, sans-serif",
            fontWeight: "lighter"
        },
        axisX:{
            valueFormatString: "#",
            interval: 1
        },
        axisY:{ 
            valueFormatString: "#",
            interval: 10
        },
        data: [{
            type: "column",
            color: "#1959d1",
            click: function(e){
                showSelectedColumn(e.dataPoint.x);
            },
            dataPoints: dps2
        }]
    });

    var map = L.map('map').setView([39.93685568995833, 116.37027740478517], 13);

    var gdata;
    var resultGroup = [];
    var isDrawingPattern = false;
    var geoPattern = null , geoResult = null, geoAllResult = null;
    var distance = 0;
    var lastLat = 0;
    var lastLon = 0;
    var isFirstToDisplay = 0;
    var lastpos = null;
    var graphButton;
    var interpolated = [];
    var boxes = [];
    var graph_x_axis = [];
    var graph_y_axis = [];
    var graph2_x_axis = [];
    var graph2_y_axis = [];
    var dps = [];
    var dps2 = [];
    var svg = [];
    var testSvg = [];
    var gdataPrintResult = [];
    var gdataPrintResultPerPoint = [];
    var fieldsTicked = [];
    var fieldsTickedPerPoint = [];
    var line_colors = [
            '#056fe8', '#fa05fa', '#f2f202',
            '#02f246', '#9a05eb', '#f7c600',
            '#f08902', '#94793e', '#787369'
        ];

    var patternStyle = {
        "color": "#e20fcd",
        "weight": 5
    };
    
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-top-center",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "5000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFyb3NjIiwiYSI6ImNrb3B4b2QxeTBweG0ycWw0bTBiYWVwcWgifQ.g79td3RKqhZ9DEOLF9nGlA', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>, <a href="https://www.microsoft.com/en-us/download/details.aspx?id=52367">Geolife Data set</a>',
        id: 'mapbox/streets-v12',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);

    var sidebar = L.control.sidebar('sidebar', {
        position: 'left'
    });

    var sidebarRight = L.control.sidebar('sidebarRight', {
        position: 'right'
    });

    map.addControl(sidebar);
    map.addControl(sidebarRight);

    L.easyButton('fa-repeat', function(btn, map){
        clearSearch();
    }).addTo( map );

    L.easyButton('fa-list', function(btn, map){
        sidebar.toggle();
    }).addTo( map );

    graphButton = L.easyButton('fa-bar-chart', function(btn, map){
            sidebarRight.toggle();
    });
    //SVG string to DOM element
    function render_xml(id, xml_string){
        var doc = new DOMParser().parseFromString(xml_string, 'application/xml');
        var el = document.getElementById(id)
        el.appendChild(
            el.ownerDocument.importNode(doc.documentElement, true)
        )
    }

    function showSelectedColumn(point){
        var gdataPrint = [];
        var foundMatch = 0;
        fieldsTickedPerPoint = [];

        for(var i = 0; i < chart2.options.data[0].dataPoints.length; i++){
            if(chart2.options.data[0].dataPoints[i].x == point){
                if(chart2.options.data[0].dataPoints[i].color == "#538efc"){
                    chart2.options.data[0].dataPoints[i].color = "#1959d1";
                }
                else{
                    chart2.options.data[0].dataPoints[i].color = "#538efc";
                }
            }
        }
        chart2.render();

        for(var i = 0; i < chart.options.data[0].dataPoints.length; i++){
            chart.options.data[0].dataPoints[i].color = "#1959d1";
        }
        chart.render();

        for(var i in fieldsTicked){
            if(fieldsTicked[i] == point && foundMatch == 0){
                fieldsTicked.splice(i, 1);
                foundMatch = 1;
            }
        }
        if(foundMatch == 0){
            fieldsTicked.push(point)
        }
        if (gdataPrintResult!=null){
                map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }
        if (geoAllResult!=null){
                map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
                map.removeLayer(geoResult);
        }

        for(var j in fieldsTicked){
            for(var i in gdata){
                if(gdata[i][5].length == fieldsTicked[j]){
                    gdataPrint.push(gdata[i]);
                }
            }
        }


        geojson = {
                "type": "FeatureCollection",
                "features": gdataPrint.map(function myFunction(item) { return JSON.parse(item[6]);})
        };

        gdataPrintResult = L.geoJSON(geojson, {
                style: function (feature, layer) {
                    return {weight: 4, opacity: 0.6, color: line_colors[Math.floor(Math.random() * 4)], fillOpacity: 0.6};
                }
        });
        gdataPrintResult.addTo(map);
    }

    function showSelectedColumnPerPoint(point){
        var gdataPrint = [];
        var foundMatch = 0;
        fieldsTicked = [];

        for(var i = 0; i < chart.options.data[0].dataPoints.length; i++){
            if(chart.options.data[0].dataPoints[i].x == point){
                if(chart.options.data[0].dataPoints[i].color == "#538efc"){
                    chart.options.data[0].dataPoints[i].color = "#1959d1";
                }
                else{
                    chart.options.data[0].dataPoints[i].color = "#538efc";
                }
            }
        }
        chart.render();

        for(var i = 0; i < chart2.options.data[0].dataPoints.length; i++){
            chart2.options.data[0].dataPoints[i].color = "#1959d1";
        }
        chart2.render();

        for(var i in fieldsTickedPerPoint){
            if(fieldsTickedPerPoint[i] == point && foundMatch == 0){
                fieldsTickedPerPoint.splice(i, 1);
                foundMatch = 1;
            }
        }
        if(foundMatch == 0){
            fieldsTickedPerPoint.push(point)
        }
        if (gdataPrintResult!=null){
                map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }
        if (geoAllResult!=null){
                map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
                map.removeLayer(geoResult);
        }

        for(var j in fieldsTickedPerPoint){
            for(var i in gdata){
                for(var k in gdata[i][5]){
                    if(gdata[i][5][k] == fieldsTickedPerPoint[j]){
                        gdataPrint.push(gdata[i]);
                    }
                }
            }
        }

        geojson = {
                "type": "FeatureCollection",
                "features": gdataPrint.map(function myFunction(item) { return JSON.parse(item[6]);})
        };

        gdataPrintResultPerPoint = L.geoJSON(geojson, {
                style: function (feature, layer) {
                    return {weight: 4, opacity: 0.6, color: line_colors[Math.floor(Math.random() * 4)], fillOpacity: 0.6};
                }
        });
        gdataPrintResultPerPoint.addTo(map);
    }

    function clearSearch(){
        sidebarRight.hide();
        graphButton.removeFrom(map);
        for (var i in boxes){
                boxes[i].removeFrom(map);
        }
        boxes = [];
        interpolated = [];
        dps = [];
        dps2 = [];
        $("#psize").html("0");
        $("#resultsbox").hide();
        $("#chartContainer").hide()
        $("#chart2Container").hide()
        if (geoAllResult!=null){
            map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        if (gdataPrintResult!=null){
            map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }
    }

    function addToPath(latlng){
        var hash = encodeGeoHash(latlng.lat,latlng.lng,7);
        interpolated.push(hash);
        $("#psize").html(interpolated.length);
        var box = decodeGeoHash(hash);
        var rect = L.rectangle([[box['latitude'][0],box['longitude'][0]],[box['latitude'][1],box['longitude'][1]]], {color: "#eb3a05", weight: 2, fillOpacity: 0});
        rect.bindPopup("Box "+(boxes.length+1)+" <br> <a href='#' onclick='removeBox("+boxes.length+")'>Remove</a>");
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

    function drawTrackScaledWithoutZoom(coordinates, svgWidth, svgHeight, i){
        // Find the minimum and maximum values for x and y coordinates.
        let minX = coordinates[0][0], maxX = coordinates[0][0];
        let minY = coordinates[0][1], maxY = coordinates[0][1];
        coordinates.forEach(coord => {
            if (coord[0] < minX) minX = coord[0];
            if (coord[0] > maxX) maxX = coord[0];
            if (coord[1] < minY) minY = coord[1];
            if (coord[1] > maxY) maxY = coord[1];
        });
        
        // Calculate the width and height of the viewable area.
        const width = maxX - minX;
        const height = maxY - minY;
        
        // Calculate the scaling factor for the polyline.
        const xScale = svgWidth / width;
        const yScale = svgHeight / height;
        const scale = Math.min(xScale, yScale);
        
        // Calculate the points for the SVG polyline by scaling the polyline coordinates.
        const scaledPoints = coordinates.map(coord => {
            const x = (coord[0] - minX) * scale;
            const y = (coord[1] - minY) * scale;
            return `${x},${y}`;
        }).join(' ');
        
        // Create an SVG element and set its dimensions.
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', svgWidth);
        svg.setAttribute('height', svgHeight);
        
        // Create a polyline element and set its attributes.
        const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
        polyline.setAttribute('points', scaledPoints);
        polyline.setAttribute('stroke', '#1959d1');
        polyline.setAttribute('stroke-width', '2');
        polyline.setAttribute('fill', 'none');
        
        // Append the polyline element to the SVG element and the SVG element to the DOM.
        divname = "mapArea" + i;
        svg.appendChild(polyline);
        document.getElementById(divname).replaceChildren(svg);
    }

    function showResults(){
        
        graphButton.addTo(map);
        $("#resultsbox").show();
        $("#chartContainer").show();
        $("#chart2Container").show();
        fieldsTicked = [];
        fieldsTickedPerPoint = [];

        if (geoAllResult!=null){
            map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        if (gdataPrintResult!=null){
                map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }

        var x = "";
        graph_array = [];
        graph2_array = [[],[]];
        graph_x_axis = [];
        graph_y_axis = [];
        graph2_x_axis = [];
        graph2_y_axis = [];
        point = 1;
        count = 0;
        match_number = 0;
        match_count = 0;

        for (var i in gdata){
            //x+= "<tr><td><div id='mapArea"+i+"' style='width:80px;height:80px;' onclick=\"showTrack("+i+")\"></div></td><td>"+gdata[i][1]+"</td><td>"+gdata[i][2]+"</td><td>"+gdata[i][3]+"</td><td>"+gdata[i][4]+"</td></tr>";
            //x+= "<tr><td><div id='mapArea"+i+"' style='width:80px;height:80px;' onclick=\"showTrack("+i+")\"></div></td><td><div onclick=\"showTrack("+i+")\">Track ID: <b>"+gdata[i][0]+"</b><br>Matched fields: <b>"+gdata[i][1]+"</b> ("+gdata[i][5]+")<br>Starting box: <b>"+gdata[i][2]+"</b><br>Ending box: <b>"+gdata[i][3]+"</b><br>Gaps: <b>"+gdata[i][4]+"</b><br></div></td></tr>"
            x+= "<tr><td><div id='mapArea"+i+"' style='width:80px;height:80px;' onclick=\"showTrack("+i+")\"></div></td><td><div onclick=\"showTrack("+i+")\"><h5><b>"+gdata[i][0]+"</b></h5>Path stars on box <b>"+gdata[i][2]+"</b> and ends on box <b>"+gdata[i][3]+"</b><br>In total, <b>"+gdata[i][1]+"</b> fields matched, with <b>"+gdata[i][4]+"</b> gaps<br>Matched fields: <b>"+gdata[i][5]+"</b></div></td></tr>";
            graph2_array[1].push(i);
            graph2_array[0].push(gdata[i][1]);
            for(var j in gdata[i][5]){
                graph_array.push(gdata[i][5][j]);
            }
        }

        graph_array.sort();

        for(var i in graph_array){
            if(graph_array[i] == point){
                count = count+1;
                //console.log(graph_array[i]);
            }else{
                graph_x_axis.push(point);
                graph_y_axis.push(count);
                count = 0;
                point = point +1;
            }
        }

        for(var i in graph2_array[0]){
            if(i == 0){
                match_number = graph2_array[0][i];
                match_count++;
            }
            else{
                if(match_number == graph2_array[0][i]){
                    match_count++;
                }
                else{
                    graph2_x_axis.push(match_number);
                    graph2_y_axis.push(match_count);
                    match_number = graph2_array[0][i];
                    match_count = 1;
                }
            }
        }

        count = count+1;
        graph_x_axis.push(point);
        graph_y_axis.push(count);

        graph2_x_axis.push(match_number);
        graph2_y_axis.push(match_count);

        for(var i in graph_x_axis){
            dps.push({
                x: graph_x_axis[i],
                y: graph_y_axis[i]
            });
        };

        for(var i in graph2_x_axis){
            dps2.push({
                x: graph2_x_axis[i],
                y: graph2_y_axis[i]
            });
        }
        $("#totalfound").html(gdata.length);
        $("#results").html(x);

        for(i in gdata){
            drawTrackScaledWithoutZoom(JSON.parse(gdata[i][6]).geometry.coordinates, 80, 80, i);
        }
        chart.options.data[0].dataPoints = dps;
        chart2.options.data[0].dataPoints = dps2;
        chart.render();
        chart2.render();
        dps = [];
        dps2 = [];
        isFirstToDisplay = 0;
    }

    function showTrack(id){
        if (geoAllResult!=null){
            map.removeLayer(geoAllResult);
        }
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        if (gdataPrintResult!=null){
                map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }
        geoResult = L.geoJSON(JSON.parse(gdata[id][6]), {
                style: function (feature) {
                    return {fill: false, fillOpacity: 0.6, stroke: true};
                }
        });   
        geoResult.addTo(map);
    }

    function showAll(){
        if (geoResult!=null){
            map.removeLayer(geoResult);
        }
        if (gdataPrintResult!=null){
                map.removeLayer(gdataPrintResult);
        }
        if (gdataPrintResultPerPoint!=null){
                map.removeLayer(gdataPrintResultPerPoint);
        }
        geoAllResult.addTo(map);
    }

    function removeBox(id){
        boxes[id].removeFrom(map);
        boxes.splice(id, 1);
        interpolated.splice(id, 1);
        $("#gsMatch").val(Math.max(1,Math.floor(boxes.length*0.8)));
        $("#gaps").val(Math.round(boxes.length*0.2));
        findPaths();
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
            //console.log(json);
            gdata = json;
            showResults();
            if (geoAllResult!=null){
                map.removeLayer(geoAllResult);
            }
            geojson = {
                "type": "FeatureCollection",
                "features": json.map(function myFunction(item) { return JSON.parse(item[6]);})
            };

            geoAllResult = L.geoJSON(geojson, {
                style: function (feature, layer) {
                    return {weight: 4, opacity: 0.6, color: line_colors[Math.floor(Math.random() * 4)], fillOpacity: 0.6};
                }
            });   

            geoAllResult.addTo(map);

            for (var i in boxes){
                boxes[i].removeFrom(map);
                boxes[i].bindPopup("Box "+(parseInt(i)+1)+" <br> <a href='#' onclick='removeBox("+i+")'>Remove</a>");
                boxes[i].addTo(map);
            }
        });
        svg = [];
        testSvg = [];
    }

    $(document).ready(function onDocumentReady() {  
        toastr["info"]("Draw at least 2 areas of interest in the right order")
    });

</script>
<script src="js/jquery.tablesorter.min.js"></script>
<link rel="stylesheet" href="css/theme.blue.css"/>

<!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
<script src="js/ie10-viewport-bug-workaround.js"></script>

</body>
</html>