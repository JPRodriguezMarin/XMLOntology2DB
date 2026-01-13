
CREATE TABLE "_CyberEffect" (
	id INTEGER NOT NULL, 
	_cybereffect_id INTEGER NOT NULL, 
	deny_id INTEGER NOT NULL, 
	detect_id INTEGER NOT NULL, 
	manipulate_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (deny_id), 
	FOREIGN KEY(deny_id) REFERENCES "Deny" (id), 
	UNIQUE (detect_id), 
	FOREIGN KEY(detect_id) REFERENCES "Detect" (id), 
	UNIQUE (manipulate_id), 
	FOREIGN KEY(manipulate_id) REFERENCES "Manipulate" (id)
)

