-- Define a table called users in a database. 

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL,
	name VARCHAR(255),
	PRIMARY KEY(id), 
	UNIQUE(email)
);
