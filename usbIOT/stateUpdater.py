import boto3, json

client = boto3.client('iot-data')

def main():
	response = client.get_thing_shadow(
	    thingName='USBThing'
	)

	payload = response['payload']
	state = json.loads(payload.read())["state"]["reported"]["light"]

	payload = {"state": {"reported":{"light":state},"desired": {"light": "off" if state == "on" else "on"}}}
	jsonData = json.dumps(payload)

	response = client.update_thing_shadow(
		thingName='USBThing',
		payload=jsonData.encode()
	)

	print(response['payload'].read())

	

if __name__ == '__main__':
	main()
