FROM ubuntu:20.04
RUN apt-get -y update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Bratislava
RUN apt-get install -y tzdata
RUN apt -y install apache2
RUN apt -y install php libapache2-mod-php php-mysql
RUN apt -y install mysql-server
RUN chmod -R 777 /run/mysqld
RUN apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get -y update
RUN apt -y install python3.8
RUN apt -y install python3-pip
RUN pip3 install geopy
RUN pip3 install numpy
RUN pip3 install six
RUN pip3 install pandas
RUN pip3 install sqlalchemy
RUN pip3 install geojson
RUN pip3 install libgeohash
RUN pip3 install hausdorff
RUN pip3 install pymysql
RUN pip3 install numba
RUN pip3 install mysql-connector-python
COPY db.sql /home/db.sql
COPY gps_search2.sql /home/hashmap.sql

# docker build -t search .
# docker run -dit -v C:\Users\Maksim\Desktop\searchmap_v2\search_web\show:/var/www/html/ -v C:\Users\Maksim\Desktop\searchmap_v2\search_web/:/data --name search_gps2 -p 8090:80 search2 
# after build and run

#  docker container exec -it search_gps /bin/bash
#  service apache2 start
#  service mysql start
#  python3 /data/csv_to_geohash.py
#  mysql -u root < /home/db.sql
#  mysql -u root hashcode < /home/hashmap.sql
#  mysql --local-infile=1 -u root -p1 < /data/configuration.sql

#  mysql
#  SET GLOBAL local_infile=1;
#  quit
#  mysql --local-infile=1 -u root -p1
#  use hashcode;
#  load data local infile 'data/path.csv' into table path fields terminated by ',' lines terminated by '\n' ignore 1 lines (hash, track);
#  load data local infile 'data/track.csv' into table tracks fields terminated by ';' lines terminated by '\n' ignore 1 lines (route, track);

# docker container exec -it search_gps /bin/bash
# check runnig services .. if apache or mysql not running, start them as below
#  service --status-all  
# RUN service start apache2
# RUN service start mysql


#docker run -dit -v C:\Users\Maksim\Desktop\searchmap_v2\search_web\show:/var/www/html/ -v C:\Users\Maksim\Desktop\searchmap_v2\search_web/:/data --name search_gps2 -p 8090:80 search2 