
CREATE TABLE "Incident" (
	id INTEGER NOT NULL, 
	incident_id VARCHAR NOT NULL, 
	severity VARCHAR NOT NULL, 
	event_id INTEGER NOT NULL, 
	mitreattack_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (event_id), 
	FOREIGN KEY(event_id) REFERENCES "Event" (id), 
	FOREIGN KEY(mitreattack_id) REFERENCES "MitreAttack" (id)
)

