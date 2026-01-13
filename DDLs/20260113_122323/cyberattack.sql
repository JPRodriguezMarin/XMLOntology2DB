
CREATE TABLE "CyberAttack" (
	id INTEGER NOT NULL, 
	cyberattack_id INTEGER NOT NULL, 
	mitre_attack_subtechnique_ids VARCHAR NOT NULL, 
	dataexfiltration_id INTEGER NOT NULL, 
	manipulationattack_id INTEGER NOT NULL, 
	phishingattack_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (dataexfiltration_id), 
	FOREIGN KEY(dataexfiltration_id) REFERENCES "DataExfiltration" (id), 
	UNIQUE (manipulationattack_id), 
	FOREIGN KEY(manipulationattack_id) REFERENCES "ManipulationAttack" (id), 
	UNIQUE (phishingattack_id), 
	FOREIGN KEY(phishingattack_id) REFERENCES "PhishingAttack" (id)
)

