SET GLOBAL local_infile=1;
use hashcode;
load data local infile 'data/path.csv' into table path fields terminated by ',' lines terminated by '\n' ignore 1 lines (hash, track);
load data local infile 'data/track.csv' into table tracks fields terminated by ';' lines terminated by '\n' ignore 1 lines (route, track);