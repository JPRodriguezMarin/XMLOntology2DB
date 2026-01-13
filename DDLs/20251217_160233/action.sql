
CREATE TABLE "Action" (
	id INTEGER NOT NULL, 
	action_type VARCHAR NOT NULL, 
	timestamp DATETIME NOT NULL, 
	decisivecondition_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(decisivecondition_id) REFERENCES "DecisiveCondition" (id)
)

