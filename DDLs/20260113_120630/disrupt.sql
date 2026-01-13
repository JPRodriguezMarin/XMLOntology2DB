
CREATE TABLE "Disrupt" (
	id INTEGER NOT NULL, 
	disrupt_id INTEGER NOT NULL, 
	blocktrafficeffect_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (blocktrafficeffect_id), 
	FOREIGN KEY(blocktrafficeffect_id) REFERENCES "BlockTrafficEffect" (id)
)

