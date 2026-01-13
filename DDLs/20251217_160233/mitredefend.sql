
CREATE TABLE "MitreDefend" (
	id INTEGER NOT NULL, 
	defend_id VARCHAR NOT NULL, 
	mitreattack_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(mitreattack_id) REFERENCES "MitreAttack" (id)
)

