const map = L.map('map').setView([48.159411, 17.064991], 13); // set initial position and zoom level

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


let inputBox = document.getElementById("input")

document.getElementById('downloadButton').addEventListener('click', function() {

    map.eachLayer(function (layer) {
        // Check if the layer is a polyline
        if (layer instanceof L.Polyline) {
            // Remove the polyline from the map
            map.removeLayer(layer);
        }
    });

    let div = document.getElementById("trackModal")

    fetch(inputBox.value)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(csvData => {
            const tracks = parseCSV(csvData);
            console.log('Tracks:', tracks);
            for (const track in tracks){
                const route = L.polyline(tracks[track], {color: 'red'}).addTo(map);
                route.on('mouseover', function(event) {
                    // Display a popup on hover
                    div.style.opacity = "1"
                    div.style.pointerEvents = "auto"
                    document.getElementById("trackModalText").innerHTML = "Track: "+track
                })
                .on('mouseout', function(event) {
                    // Close the popup when mouse leaves the marker
                    div.style.opacity = "0"
                    div.style.pointerEvents = "none"
                });
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});

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


