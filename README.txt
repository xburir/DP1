# build image with already downloaded maps(pbf) in custom_files directory, not tested
docker.exe run -dt --name valhalla-test-slovakia -p 8002:8002 -v /custom_files:/custom_files ghcr.io/gis-ops/docker-valhalla/valhalla:latest


# build image with download-slovakia-map in command
docker.exe run -dt --name valhalla-test-slovakia -p 8002:8002 -v /custom_files:/custom_files -e tile_urls=https://download.geofabrik.de/europe/slovakia-latest.osm.pbf ghcr.io/gis-ops/docker-valhalla/valhalla:latest

# get route of coords
curl http://localhost:8002/route --data '{"locations":[{"lat":41.318818,"lon":19.461336},{"lat":41.321001,"lon":19.459598}],"costing":"auto","directions_options":{"units":"miles"}}' | jq '.'
curl http://localhost:8002/route --data '{"locations":[{"lat":19.461336,"lon":41.318818},{"lat":19.459598,"lon":41.321001}],"costing":"auto","directions_options":{"units":"miles"}}' | jq '.'

# get route on slovakia
curl http://localhost:8002/route --data '{"locations":[{"lat":48.16098927363811,"lon":17.50091786329},{"lat":48.15250791638809,"lon":17.528853774658444}],"costing":"auto","directions_options":{"units":"miles"}}' | jq '.'