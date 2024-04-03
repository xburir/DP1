FROM ubuntu:22.04
RUN apt-get -y update
RUN apt -y install npm
RUN apt -y install mysql-server
RUN apt -y install python3
RUN apt -y install python3-pip
# RUN pip3 install python-csv
RUN pip3 install requests
RUN pip3 install gpxpy

ENV TZ=Europe/Bratislava
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /DP1/webapp

# RUN service mysql start  ### DOESNT WORK
# RUN mysql < db.sql   
# PORT=8090 npm run start

# docker build -t dp_webapp .
# docker network create web_server --driver bridge
# docker run -dit --name dp_webapp --network web_server -p 8090:8090 -v C:\Users\richard.buri\Desktop\docker\DP1:/DP1 dp_webapp
# docker container exec -it dp_webapp /bin/bash

# docker build -t IMAGE_NAME .
# docker network create BRIDGE_NAME --driver bridge
# docker run -dit --name CONTAINER NAME --network BRIDGE_NAME -p 8090:80 -v C:\PATH\DP1:./ IMAGE_NAME
# docker container exec -it IMAGE_NAME /bin/bash