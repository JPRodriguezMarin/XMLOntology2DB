
CREATE TABLE "PhishingAttack" (
	id INTEGER NOT NULL, 
	phishingattack_id INTEGER NOT NULL, 
	message_type VARCHAR NOT NULL, 
	header VARCHAR NOT NULL, 
	body VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)

