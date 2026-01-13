
CREATE TABLE "SecurityNetwork" (
	id INTEGER NOT NULL, 
	vlan_id INTEGER NOT NULL, 
	trust_level VARCHAR NOT NULL, 
	service_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(service_id) REFERENCES "Service" (id)
)

