
CREATE TABLE "_CyberDEMBase" (
	id INTEGER NOT NULL, 
	_cyberdembase_id INTEGER NOT NULL, 
	_cyberobject_id INTEGER NOT NULL, 
	_cyberevent_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (_cyberobject_id), 
	FOREIGN KEY(_cyberobject_id) REFERENCES "_CyberObject" (id), 
	UNIQUE (_cyberevent_id), 
	FOREIGN KEY(_cyberevent_id) REFERENCES "_CyberEvent" (id)
)

