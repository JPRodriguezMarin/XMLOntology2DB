
CREATE TABLE "NetworkLink" (
	id INTEGER NOT NULL, 
	networklink_id INTEGER NOT NULL, 
	is_logical VARCHAR NOT NULL, 
	physical_layer VARCHAR NOT NULL, 
	data_link_protocol VARCHAR NOT NULL, 
	bandwidth VARCHAR NOT NULL, 
	latency VARCHAR NOT NULL, 
	jitter VARCHAR NOT NULL, 
	network_interfaces VARCHAR NOT NULL, 
	PRIMARY KEY (id)
)

