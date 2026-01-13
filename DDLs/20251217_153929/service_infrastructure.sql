
CREATE TABLE "Service_Infrastructure" (
	service_id INTEGER NOT NULL, 
	infrastructure_id INTEGER NOT NULL, 
	PRIMARY KEY (service_id, infrastructure_id), 
	FOREIGN KEY(service_id) REFERENCES "Service" (id), 
	FOREIGN KEY(infrastructure_id) REFERENCES "Infrastructure" (id)
)

