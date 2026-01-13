
CREATE TABLE "Unit" (
	id INTEGER NOT NULL, 
	unit_name VARCHAR NOT NULL, 
	callsign VARCHAR, 
	task_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (task_id), 
	FOREIGN KEY(task_id) REFERENCES "Task" (id)
)

