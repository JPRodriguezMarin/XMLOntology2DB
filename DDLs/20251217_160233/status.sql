
CREATE TABLE "Status" (
	id INTEGER NOT NULL, 
	value VARCHAR NOT NULL, 
	last_update DATETIME NOT NULL, 
	task_id INTEGER NOT NULL, 
	unit_id INTEGER NOT NULL, 
	mission_id INTEGER NOT NULL, 
	service_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (task_id), 
	FOREIGN KEY(task_id) REFERENCES "Task" (id), 
	UNIQUE (unit_id), 
	FOREIGN KEY(unit_id) REFERENCES "Unit" (id), 
	UNIQUE (mission_id), 
	FOREIGN KEY(mission_id) REFERENCES "Mission" (id), 
	UNIQUE (service_id), 
	FOREIGN KEY(service_id) REFERENCES "Service" (id)
)

