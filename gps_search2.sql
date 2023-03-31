DROP TABLE IF EXISTS `path`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `path` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` varchar(7) NOT NULL,
  `track` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ihash` (`hash`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- LOAD DATA INFILE 'path.csv' INTO TABLE path;

DROP TABLE IF EXISTS `tracks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tracks` (
  `route` varchar(250) NOT NULL,
  `track` mediumtext NOT NULL,
  PRIMARY KEY (`route`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
