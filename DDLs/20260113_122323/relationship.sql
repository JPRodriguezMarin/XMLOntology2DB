
CREATE TABLE "Relationship" (
	id INTEGER NOT NULL, 
	relationship_id INTEGER NOT NULL, 
	related_object_1 VARCHAR NOT NULL, 
	related_object_2 VARCHAR NOT NULL, 
	relationship_type VARCHAR NOT NULL, 
	privileges VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)

