
CREATE TABLE "Task" (
	id INTEGER NOT NULL, 
	task_id VARCHAR NOT NULL, 
	deadline DATETIME, 
	action_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(action_id) REFERENCES "Action" (id)
)

