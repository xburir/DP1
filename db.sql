
CREATE DATABASE IF NOT EXISTS `hashcode` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER 'search'@'%' IDENTIFIED BY 'password';
GRANT ALL ON hashcode.* TO 'search'@'%';