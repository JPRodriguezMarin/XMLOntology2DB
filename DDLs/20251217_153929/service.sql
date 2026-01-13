
CREATE TABLE "Service" (
	id INTEGER NOT NULL, 
	service_name VARCHAR NOT NULL, 
	cyberasset_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (cyberasset_id), 
	FOREIGN KEY(cyberasset_id) REFERENCES "CyberAsset" (id)
)

