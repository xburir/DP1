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
RUN pip3 install libgeohash
RUN pip3 install hausdorff
RUN pip3 install pymysql
RUN pip3 install numba
RUN pip3 install mysql-connector-python
COPY db.sql /home/db.sql
COPY gps_search.sql /home/hashmap.sql
# docker build -t search .
# docker run -it -v path.to.show:/var/www/html/ --name search_gps -p 8090:80 search
# after build and run
# docker container attach [name of container]
#  service apache2 start
#  service mysql start
#  mysql -u root < /home/db.sql
#  mysql -u root hashcode < /home/hashmap.sql

# docker start [container name]
# check runnig services .. if apache or mysql not running, start them as below
#  service --status-all  
# RUN service start apache2
# RUN service start mysql
