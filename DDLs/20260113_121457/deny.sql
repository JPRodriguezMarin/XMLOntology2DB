
CREATE TABLE "Deny" (
	id INTEGER NOT NULL, 
	deny_id INTEGER NOT NULL, 
	destroy_id INTEGER NOT NULL, 
	degrade_id INTEGER NOT NULL, 
	disrupt_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (destroy_id), 
	FOREIGN KEY(destroy_id) REFERENCES "Destroy" (id), 
	UNIQUE (degrade_id), 
	FOREIGN KEY(degrade_id) REFERENCES "Degrade" (id), 
	UNIQUE (disrupt_id), 
	FOREIGN KEY(disrupt_id) REFERENCES "Disrupt" (id)
)

