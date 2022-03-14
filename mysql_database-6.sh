#!/usr/bin/env bash

sudo mysql -u root -p <<EOF
USE db;
CREATE TABLE person(ID int NOT NULL AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL, DOB DATE NOT NULL);
INSERT INTO person(first_name,last_name,DOB) VALUES ("Mihir", "Harshe", '1996-03-25');
INSERT INTO person(first_name,last_name,DOB) VALUES ("Ashish", "Mhatre", '1996-08-15');
INSERT INTO person(first_name, last_name, DOB) VALUES ("Pushkar", "Dandekar", '1996-02-21');
EOF

sudo mysql -H -e "Select * from person" db > ~/Desktop/Shell_Scripting_Assignment/db_Output-6.html
