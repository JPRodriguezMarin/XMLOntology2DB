
CREATE TABLE "Device" (
	id INTEGER NOT NULL, 
	device_id VARCHAR NOT NULL, 
	device_types VARCHAR NOT NULL, 
	is_virtual VARCHAR NOT NULL, 
	role VARCHAR NOT NULL, 
	device_identifier VARCHAR NOT NULL, 
	network_interfaces VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)

