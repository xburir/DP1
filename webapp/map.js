const map = L.map('map').setView([48.159411, 17.064991], 13); // set initial position and zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


let shownFiles = []

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

function removeLayers(fileName, routeType) {
    var layersToRemove = []
    map.eachLayer(function (layer) {
        // Check if the layer is a polyline
        if (layer instanceof L.Polyline) {
            // Remove the polyline from the map
            if (layer.options.fileName === fileName && layer.options.routeType === routeType) {
                layersToRemove.push(layer); // Add the layer to the removal array
            }
        }
    });
    // Remove layers outside the loop to avoid modifying the iteration array
    layersToRemove.forEach(function (layer) {
        map.removeLayer(layer);
    });

    shownFiles = shownFiles.filter(innerArray => !(
        JSON.stringify(innerArray) === JSON.stringify([fileName,routeType])
      ));

    fitBounds()
}

function toggleRoute(fileName, username, routeType, event) {
    if (event.checked) {
        showFileDetails(fileName, username, routeType)
    } else {
        removeLayers(fileName, routeType)
    }
}


function showFileDetails(fileName, username, routeType) {


    let div = document.getElementById("trackModal")
    var hoveredLayers = []

    let path = '/routes/' + username + '/' + fileName + '/'
    if (routeType === 'original') {
        path = path + 'database_original.csv'
    }
    if (routeType === 'map-match') {
        path = path + 'database.csv'
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
            for (const track in tracks) {
                const route = L.polyline(tracks[track], {
                    color: routeType === "original" ? 'red' : 'blue',
                    trackId: track,
                    fileName: fileName,
                    routeType: routeType
                }).addTo(map);


                route.on('mouseover', function (event) {
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
                    for (var event of hoveredLayers) {
                        console.log();
                        let key = event.options.trackId
                        let file = event.options.fileName
                        str += '<br>' + key + '[' + file + ']';
                    }
                    document.getElementById("trackModalText").innerHTML = "Tracks (" + hoveredLayers.length + ") " + str

                })
                    .on('mouseout', function (event) {
                        // Close the popup when mouse leaves the marker
                        div.style.opacity = "0"
                        div.style.pointerEvents = "none"

                        hoveredLayers = []

                    });
            }
        })
        .then(_ => {
            shownFiles.push([fileName,routeType])
            fitBounds()
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function fitBounds() {
    let bounds = new L.LatLngBounds();
    let any = false
    map.eachLayer(function (polyline) {
        // Check if the layer is a polyline
        if (polyline instanceof L.Polyline) {
            bounds.extend(polyline.getBounds())
            any = true
        }
    });
    if (any) {
        map.fitBounds(bounds)
    }

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

