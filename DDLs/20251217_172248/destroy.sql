
CREATE TABLE "Destroy" (
	id INTEGER NOT NULL, 
	destroy_id INTEGER NOT NULL, 
	hardwaredamageeffect_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (hardwaredamageeffect_id), 
	FOREIGN KEY(hardwaredamageeffect_id) REFERENCES "HardwareDamageEffect" (id)
)

