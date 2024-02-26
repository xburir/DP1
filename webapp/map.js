const map = L.map('map').setView([48.159411, 17.064991], 13); // set initial position and zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


let inputBox = document.getElementById("input")

// Function to check if the cursor position intersects with a polyline's path
function isCursorOnPolyline(cursorPos, polyline) {
    var path = polyline.getLatLngs();
    for (var i = 0; i < path.length - 1; i++) {
        var p1 = path[i];
        var p2 = path[i + 1];
        if (L.GeometryUtil.belongsSegment(cursorPos, p1, p2)) {
            return true;
        }
    }
    return false;
}


function showFileDetails(fileName,username,route) {
    map.eachLayer(function (layer) {
        // Check if the layer is a polyline
        if (layer instanceof L.Polyline) {
            // Remove the polyline from the map
            map.removeLayer(layer);
        }
    });

    let div = document.getElementById("trackModal")
    var hoveredLayers = []

    let path = '/routes/'+username+'/'+fileName+'/'
    if (route === 'original'){
        path = path+'database_original.csv'
    }
    if (route === 'map-match'){
        path = path+'database.csv'
    }

    fetch(path)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(csvData => {
            const tracks = parseCSV(csvData);
            for (const track in tracks){
                const route = L.polyline(tracks[track], {
                    color: 'red',
                    customData: track}).addTo(map);
                
                route.on('mouseover', function(event) {
                    // Display a popup on hover
                    div.style.opacity = "1"
                    div.style.pointerEvents = "auto"
                    
                    var cursorPos = event.latlng; // Get the cursor position
                    map.eachLayer(function (polyline) {
                        // Check if the layer is a polyline
                        if (polyline instanceof L.Polyline) {
                            if (isCursorOnPolyline(cursorPos, polyline)) {
                                // Handle the hovered polyline accordingly
                                // You can add it to a list of hovered layers or perform other actions
                                hoveredLayers.push(polyline)
                            }
                        }
                    });
                    let str = ""
                    for (var event of hoveredLayers){
                        console.log();
                        let key = event.options.customData
                        str += '<br>'+key;
                    }
                    document.getElementById("trackModalText").innerHTML = "Tracks ("+hoveredLayers.length+") "+str
                    
                })
                .on('mouseout', function(event) {
                    // Close the popup when mouse leaves the marker
                    div.style.opacity = "0"
                    div.style.pointerEvents = "none"

                    hoveredLayers = []

                });
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}



function parseCSV(csvData) {
    const tracks = {};
    const lines = csvData.split('\n');
    for (let i = 1; i < lines.length; i++) { // Start from index 1 to skip the header row
        const [track, lat, lon] = lines[i].trim().split(',');
        if (!tracks.hasOwnProperty(track)) {
            tracks[track] = [];
        }
        tracks[track].push([parseFloat(lat), parseFloat(lon)]);
        
        
    }
    return tracks;
}

