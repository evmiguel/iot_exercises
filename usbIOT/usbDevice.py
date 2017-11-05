"""
	Author: Erika Miguel
	Date:	November 05, 2017
	
	The purpose of this script is to trigger a power
	cycle for a USB hub.

"""

import paho.mqtt.client as mqtt
import os
import json
import ssl

#--------------------------------------------------------
# Constants
#--------------------------------------------------------

WORKING_DIR	= os.path.dirname(os.path.realpath(__file__))
__FILEBASENAME__ = os.path.basename(__file__).split('.')[0]
CONFIG_FILENAME = os.path.join("{}".format(WORKING_DIR), "{}.json".format(__FILEBASENAME__))

CONFIG = {}
with open(CONFIG_FILENAME) as f:
	CONFIG = json.load(f)
CERTS_CONFIG 	= CONFIG["certs"]
AWS_CONFIG	= CONFIG["aws"]

# AWS IoT Endpoints
ENDPOINT	= AWS_CONFIG["endpoint"]
PORT		= AWS_CONFIG["port"]

# Certificates
CLIENT_ID	= "USBThing" 
CA_CERT		= "{}/{}".format(WORKING_DIR, CERTS_CONFIG["root"])
CERT_FILE	= "{}/{}".format(WORKING_DIR, CERTS_CONFIG["certFile"])
PRIVATE_KEY	= "{}/{}".format(WORKING_DIR, CERTS_CONFIG["privateKeyFile"])
PUBLIC_KEY	= "{}/{}".format(WORKING_DIR, CERTS_CONFIG["publicKeyFile"])

#--------------------------------------------------------
# Functions
#--------------------------------------------------------
def on_connect(mqtt_client, obj, flags, rc):
	'''
		on_connect callback, as specified in:
			https://www.eclipse.org/paho/clients/python/docs/
	
		where,
			mqtt_client 	= client instance
			obj		= user data set in Client()
			flags		= dictionary containing flags from broker
			rc		= connection result. 0 means successful. 1 means refused
		
	'''
	if rc == 0:
		# This conflicting state will always return a delta message
		payload = {"state": {"reported":{"light":"off"},"desired": {"light":"on"}}}
		mqtt_client.subscribe("$aws/things/USBThing/shadow/update/delta", qos=0)
		mqtt_client.publish("$aws/things/USBThing/shadow/update", json.dumps(payload), 0)

def on_message(mqtt_client, obj, msg):
	print("Message received: {} | QoS {} | Data Received {}".format(msg.topic, msg.qos, msg.payload))

#--------------------------------------------------------
# Main
#--------------------------------------------------------
def main():
	mqtt_client		= mqtt.Client(client_id=CLIENT_ID, clean_session=True)
	
	mqtt_client.on_connect	= on_connect
	mqtt_client.on_message	= on_message
	mqtt_client.tls_set(CA_CERT, certfile=CERT_FILE, keyfile=PRIVATE_KEY,
				cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

	mqtt_client.connect(ENDPOINT, PORT, keepalive=60)

	mqtt_client.loop_forever()

if __name__ == '__main__':
	main()
