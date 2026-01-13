
CREATE TABLE "Unit_Infrastructure" (
	unit_id INTEGER NOT NULL, 
	infrastructure_id INTEGER NOT NULL, 
	PRIMARY KEY (unit_id, infrastructure_id), 
	FOREIGN KEY(unit_id) REFERENCES "Unit" (id), 
	FOREIGN KEY(infrastructure_id) REFERENCES "Infrastructure" (id)
)

