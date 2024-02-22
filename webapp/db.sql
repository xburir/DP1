ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';

DROP DATABASE if EXISTS dp_webserver;

CREATE DATABASE dp_webserver;
USE dp_webserver;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (username)
);