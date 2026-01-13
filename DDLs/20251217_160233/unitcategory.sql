
CREATE TABLE "UnitCategory" (
	id INTEGER NOT NULL, 
	cat_name VARCHAR NOT NULL, 
	unit_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (unit_id), 
	FOREIGN KEY(unit_id) REFERENCES "Unit" (id)
)

