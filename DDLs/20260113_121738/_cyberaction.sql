
CREATE TABLE "_CyberAction" (
	id INTEGER NOT NULL, 
	_cyberaction_id INTEGER NOT NULL, 
	cyberadmin_id INTEGER NOT NULL, 
	cyberattack_id INTEGER NOT NULL, 
	cyberdefend_id INTEGER NOT NULL, 
	cyberrecon_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (cyberadmin_id), 
	FOREIGN KEY(cyberadmin_id) REFERENCES "CyberAdmin" (id), 
	UNIQUE (cyberattack_id), 
	FOREIGN KEY(cyberattack_id) REFERENCES "CyberAttack" (id), 
	UNIQUE (cyberdefend_id), 
	FOREIGN KEY(cyberdefend_id) REFERENCES "CyberDefend" (id), 
	UNIQUE (cyberrecon_id), 
	FOREIGN KEY(cyberrecon_id) REFERENCES "CyberRecon" (id)
)

