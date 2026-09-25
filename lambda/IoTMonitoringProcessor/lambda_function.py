```python
import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

telemetry_table = dynamodb.Table("FactoryTelemetry")
alerts_table = dynamodb.Table("FactoryAlerts")

SNS_TOPIC_ARN = "my sns arn "


def lambda_handler(event, context):

    print("Received IoT data:")
    print(json.dumps(event))

    device_id = event.get("device_id", "unknown")
    temperature = event.get("temperature", 0)
    pressure = event.get("pressure", 0)
    status = event.get("status", "UNKNOWN")
    timestamp = event.get("timestamp", "")

    # Check temperature
    if temperature > 80:
        alert = "HIGH TEMPERATURE"
    else:
        alert = "NORMAL"

    print("Device:", device_id)
    print("Temperature:", temperature)
    print("Pressure:", pressure)
    print("Status:", alert)

    # -----------------------------
    # SAVE TELEMETRY TO DYNAMODB
    # -----------------------------

    telemetry_item = {
        "device_id": device_id,
        "timestamp": timestamp,
        "temperature": temperature,
        "pressure": pressure,
        "status": status,
        "alert": alert
    }

    telemetry_table.put_item(Item=telemetry_item)

    print("Telemetry saved successfully.")


    # -----------------------------
    # HIGH TEMPERATURE ALERT
    # -----------------------------

    if temperature > 80:

        alert_item = {
            "alert_id": str(uuid.uuid4()),
            "device_id": device_id,
            "timestamp": timestamp,
            "temperature": temperature,
            "pressure": pressure,
            "alert": "HIGH TEMPERATURE",
            "message": "Temperature exceeded 80°C"
        }

        # Save alert to DynamoDB
        alerts_table.put_item(Item=alert_item)

        print("Alert saved to DynamoDB.")


        # -----------------------------
        # SEND SNS EMAIL
        # -----------------------------

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="FactoryIQ - High Temperature Alert",
            Message=f"""
⚠️ HIGH TEMPERATURE ALERT

Device: {device_id}

Temperature: {temperature}°C
Pressure: {pressure} PSI

Temperature exceeded 80°C.

FactoryIQ IoT Monitoring System
"""
        )

        print("SNS notification sent successfully.")


    return {
        "statusCode": 200,
        "body": json.dumps({
            "device_id": device_id,
            "temperature": temperature,
            "pressure": pressure,
            "alert": alert
        })
    }
```
