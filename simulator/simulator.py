from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json
import time
import random
from datetime import datetime

# AWS IoT settings
ENDPOINT = "adgv3w92nnjik-ats.iot.ap-south-1.amazonaws.com"

CLIENT_ID = "factory-machine-01"

CERTIFICATE = "41466c3872ded69106193bc18f2a0bb7def65083276167b04be74026e7b3ec3c-certificate.pem.crt"

PRIVATE_KEY = "41466c3872ded69106193bc18f2a0bb7def65083276167b04be74026e7b3ec3c-private.pem.key"

ROOT_CA = "AmazonRootCA1 (2).pem"

MQTT_TOPIC = "factory/machine-01/telemetry"


# Create MQTT connection
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(
    event_loop_group,
    host_resolver
)

mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERTIFICATE,
    pri_key_filepath=PRIVATE_KEY,
    ca_filepath=ROOT_CA,
    client_bootstrap=client_bootstrap,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30
)

print("Connecting to AWS IoT Core...")

connect_future = mqtt_connection.connect()
connect_future.result()

print("Connected successfully! ✅")


# Send IoT data continuously
while True:

    temperature = random.randint(60, 110)
    pressure = random.randint(30, 50)

    if temperature > 80:
        status = "WARNING"
    else:
        status = "NORMAL"

    data = {
        "device_id": CLIENT_ID,
        "temperature": temperature,
        "pressure": pressure,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }

    payload = json.dumps(data)

    print("Sending:")
    print(payload)

    mqtt_connection.publish(
        topic=MQTT_TOPIC,
        payload=payload,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    time.sleep(3)