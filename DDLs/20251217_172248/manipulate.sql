
CREATE TABLE "Manipulate" (
	id INTEGER NOT NULL, 
	manipulate_id INTEGER NOT NULL, 
	manipulationeffect_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (manipulationeffect_id), 
	FOREIGN KEY(manipulationeffect_id) REFERENCES "ManipulationEffect" (id)
)

