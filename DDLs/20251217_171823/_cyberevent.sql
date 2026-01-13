
CREATE TABLE "_CyberEvent" (
	id INTEGER NOT NULL, 
	cyberevent_id VARCHAR NOT NULL, 
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
	PRIMARY KEY (id)
)

