# dinstar-importer

Dinstar-importer is a Python's program that imports logs from Dinstar Voip Gateway to MySQL database



1) Clone this project with git

git clone git@github.com:vmsouza/dinstar-importer.git



2) Install and configure mysql server



3) Install Python module for MySQL (MySQLdb module)

In Ubuntu: apt-get install python-mysqldb



4) Create a database 'dinstar' and an user

mysql> create database dinstar;

mysql> grant all privileges on dinstar.* to `dinstarsqluser`@`localhost` identified by `dinstarsqlpw`;

mysql> flush privileges;



5. Configure dinstar-importer.conf



6. Run ./dinstar-importer.py


