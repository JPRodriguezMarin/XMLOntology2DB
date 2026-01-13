
CREATE TABLE "Task_Infrastructure" (
	task_id INTEGER NOT NULL, 
	infrastructure_id INTEGER NOT NULL, 
	PRIMARY KEY (task_id, infrastructure_id), 
	FOREIGN KEY(task_id) REFERENCES "Task" (id), 
	FOREIGN KEY(infrastructure_id) REFERENCES "Infrastructure" (id)
)

