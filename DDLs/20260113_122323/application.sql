
CREATE TABLE "Application" (
	id INTEGER NOT NULL, 
	application_id INTEGER NOT NULL, 
	version VARCHAR NOT NULL, 
	company VARCHAR NOT NULL, 
	operatingsystem_id INTEGER NOT NULL, 
	service_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (operatingsystem_id), 
	FOREIGN KEY(operatingsystem_id) REFERENCES "OperatingSystem" (id), 
	UNIQUE (service_id), 
	FOREIGN KEY(service_id) REFERENCES "Service" (id)
)

