
CREATE TABLE "Objective" (
	id INTEGER NOT NULL, 
	objective_id VARCHAR NOT NULL, 
	success_criteria VARCHAR NOT NULL, 
	mission_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(mission_id) REFERENCES "Mission" (id)
)

