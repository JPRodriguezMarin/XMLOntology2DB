
CREATE TABLE "_CyberEvent" (
	id INTEGER NOT NULL, 
	_cyberevent_id INTEGER NOT NULL, 
	description VARCHAR NOT NULL, 
	event_time VARCHAR NOT NULL, 
	target_ids VARCHAR NOT NULL, 
	target_modifiers VARCHAR NOT NULL, 
	phase VARCHAR NOT NULL, 
	duration VARCHAR NOT NULL, 
	actor_ids VARCHAR NOT NULL, 
	source_ids VARCHAR NOT NULL, 
	payload VARCHAR NOT NULL, 
	request_acknowledgement VARCHAR NOT NULL, 
	_cybereffect_id INTEGER NOT NULL, 
	_cyberaction_id INTEGER NOT NULL, 
	cyberacknowledge_id INTEGER NOT NULL, 
	cyberorder_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (_cybereffect_id), 
	FOREIGN KEY(_cybereffect_id) REFERENCES "_CyberEffect" (id), 
	UNIQUE (_cyberaction_id), 
	FOREIGN KEY(_cyberaction_id) REFERENCES "_CyberAction" (id), 
	UNIQUE (cyberacknowledge_id), 
	FOREIGN KEY(cyberacknowledge_id) REFERENCES "CyberAcknowledge" (id), 
	UNIQUE (cyberorder_id), 
	FOREIGN KEY(cyberorder_id) REFERENCES "CyberOrder" (id)
)

