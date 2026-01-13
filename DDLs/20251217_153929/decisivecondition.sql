
CREATE TABLE "DecisiveCondition" (
	id INTEGER NOT NULL, 
	condition_id VARCHAR NOT NULL, 
	state_description VARCHAR NOT NULL, 
	objective_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(objective_id) REFERENCES "Objective" (id)
)

