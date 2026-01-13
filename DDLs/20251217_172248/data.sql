
CREATE TABLE "Data" (
	id INTEGER NOT NULL, 
	data_id INTEGER NOT NULL, 
	sensitivity VARCHAR NOT NULL, 
	data_type VARCHAR NOT NULL, 
	encrypted VARCHAR NOT NULL, 
	status VARCHAR NOT NULL, 
	confidentiality VARCHAR NOT NULL, 
	communicationsdata_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (communicationsdata_id), 
	FOREIGN KEY(communicationsdata_id) REFERENCES "CommunicationsData" (id)
)

