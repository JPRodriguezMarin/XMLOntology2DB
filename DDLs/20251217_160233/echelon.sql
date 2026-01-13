
CREATE TABLE "Echelon" (
	id INTEGER NOT NULL, 
	level VARCHAR NOT NULL, 
	unit_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (unit_id), 
	FOREIGN KEY(unit_id) REFERENCES "Unit" (id)
)

