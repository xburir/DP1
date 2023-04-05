alter user 'root'@'localhost' identified with mysql_native_password by 'password';
CREATE USER 'search'@'%' IDENTIFIED BY 'password';
GRANT ALL ON *.* TO 'search'@'%';

-- CREATE DATABASE IF NOT EXISTS `hashcode` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- use hashcode;
-- DROP TABLE IF EXISTS `path`;

-- CREATE TABLE `path` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `hash` varchar(7) NOT NULL,
--   `track` varchar(80) NOT NULL,
--   PRIMARY KEY (`id`),
--   KEY `ihash` (`hash`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

-- DROP TABLE IF EXISTS `tracks`;
-- CREATE TABLE `tracks` (
--   `route` varchar(250) NOT NULL,
--   `track` mediumtext NOT NULL,
--   PRIMARY KEY (`route`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- SET GLOBAL local_infile=1;
-- load data local infile '/home/data/import/files/path.csv' into table path fields terminated by ',' lines terminated by '\n' ignore 1 lines (hash, track);
-- load data local infile '/home/data/import/files/track.csv' into table tracks fields terminated by ';' lines terminated by '\n' ignore 1 lines (route, track);