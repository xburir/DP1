const map = L.map('map').setView([48.159411, 17.064991], 13); // set initial position and zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


let shownRoutes = []

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

    shownRoutes = shownRoutes.filter(innerArray => !(
        JSON.stringify(innerArray) === JSON.stringify([fileName, routeType])
    ));

    fitBounds()
}

function toggleFile(fileName, username, routeType, event) {

    fetch("/list-routes/" + fileName).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    }).then(text => {
        let ress = JSON.parse(text)

        for (const track in ress.files) {
            toggleRoute(fileName, ress.files[track].name, event.checked, routeType, username)
        }
    })
}

function toggleRoute(filename, routename, checked, routeType, username) {
    if (checked) {
        fetch('/routes/' + username + '/' + filename + '/' + routename + '/' + routeType + '.csv').then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        }).then(text => {

            points = parseCSV(text)[routename]

            let div = document.getElementById("trackModal")
            var hoveredLayers = []

            const route = L.polyline(points, {
                color: routeType === "original" ? 'red' : 'blue',
                trackId: routename,
                fileName: filename,
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
        })
            .then(_ => {
                shownRoutes.push([filename, routename, routeType])
                fitBounds()
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });

    } else {
        map.eachLayer(function (layer) {
            // Check if the layer is a polyline
            if (layer instanceof L.Polyline) {
                // Remove the polyline from the map
                if (layer.options.fileName === filename && layer.options.routeType === routeType && layer.options.trackId === routename) {
                    map.removeLayer(layer);
                }
            }
        });

        shownRoutes = shownRoutes.filter(innerArray => !(
            JSON.stringify(innerArray) === JSON.stringify([filename, routename, routeType])
        ));

        fitBounds()
    }
}

function openRoutes(filename, username) {
    document.getElementById("list-of-files-header").innerHTML = `Routes of ${filename}`
    document.getElementById("table-of-files").style.display = "flex"
    let table = document.getElementById("table-of-files-tbody")
    table.innerHTML = ""

    document.querySelector(".creation-date-collumn").style.display = "none"

    fetch("/list-routes/" + filename).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();
    }).then(text => {
        let ress = JSON.parse(text)

        for (const track in ress.files) {
            let row = document.createElement("tr")
            let name = document.createElement("td")
            name.innerHTML = ress.files[track].name

            let originalSwitchTD = document.createElement("td")
            let originalSwitchLabel = document.createElement("label")
            originalSwitchTD.appendChild(originalSwitchLabel)
            originalSwitchLabel.classList.add("switch")
            let originalSwitch = document.createElement("input")
            originalSwitch.onchange = function () {
                toggleRoute(filename, ress.files[track].name, originalSwitch.checked, "original", username)
            }
            originalSwitch.type = "checkbox"
            let originalSwitchSpan = document.createElement("span")
            originalSwitchSpan.classList.add("slider")
            originalSwitchLabel.appendChild(originalSwitch)
            originalSwitchLabel.appendChild(originalSwitchSpan)

            if (shownRoutes.some(innerArray => JSON.stringify(innerArray) === JSON.stringify([filename, ress.files[track].name, "original"]))) {
                originalSwitch.checked = true
            }
            else {
                originalSwitch.checked = false
            }

            let matchedSwitchTD = document.createElement("td")
            let matchedSwitchLabel = document.createElement("label")
            matchedSwitchTD.appendChild(matchedSwitchLabel)
            matchedSwitchLabel.classList.add("switch")
            let matchedSwitch = document.createElement("input")
            matchedSwitch.onchange = function () {
                toggleRoute(filename, ress.files[track].name, matchedSwitch.checked, "map-match", username)
            }
            matchedSwitch.type = "checkbox"
            let matchedSwitchSpan = document.createElement("span")
            matchedSwitchSpan.classList.add("slider")
            matchedSwitchLabel.appendChild(matchedSwitch)
            matchedSwitchLabel.appendChild(matchedSwitchSpan)

            if (shownRoutes.some(innerArray => JSON.stringify(innerArray) === JSON.stringify([filename, ress.files[track].name, "map-match"]))) {
                matchedSwitch.checked = true
            }
            else {
                matchedSwitch.checked = false
            }

            let warnTD = document.createElement("td")
            let warnImage = document.createElement("img")
            warnTD.appendChild(warnImage)
            warnImage.src = "/public/icons/error.svg"
            warnImage.style.cursor = "pointer"
            warnImage.addEventListener("click", () => {
                fetch("/warn/" + username + "/" + filename + " " + ress.files[track].name)
            })

            row.appendChild(name)
            row.appendChild(originalSwitchTD)
            row.appendChild(matchedSwitchTD)
            row.appendChild(warnTD)
            table.appendChild(row)
        }
    })


}

function checkIfAllRoutesFromFileAreShown(filename, routesInFile, routeType) {
    found = []
    if (shownRoutes.length == 0) {
        return false
    }
    routesInFile.forEach(route => {
        shownRoutes.forEach(shownRoute => {
            if (shownRoute[0] === filename && shownRoute[1] === route && shownRoute[2] === routeType) {
                found.push(route)
            }
        })
    });
    if (found.length == routesInFile.length) {
        return true
    } else {
        return false
    }
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
    if (any && fitMap) {
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

