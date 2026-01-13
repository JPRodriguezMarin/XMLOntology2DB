
CREATE TABLE "MitreEngage" (
	id INTEGER NOT NULL, 
	engage_id VARCHAR NOT NULL, 
	mitreattack_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(mitreattack_id) REFERENCES "MitreAttack" (id)
)

