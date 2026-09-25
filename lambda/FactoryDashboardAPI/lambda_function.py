import json
import boto3
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")

telemetry_table = dynamodb.Table("FactoryTelemetry")
alerts_table = dynamodb.Table("FactoryAlerts")


def decimal_to_int(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError


def lambda_handler(event, context):

    # Get latest telemetry
    telemetry_response = telemetry_table.query(
        KeyConditionExpression=Key("device_id").eq(
            "factory-machine-01"
        ),
        ScanIndexForward=False,
        Limit=1
    )

    latest_telemetry = {}

    if telemetry_response["Items"]:
        latest_telemetry = telemetry_response["Items"][0]

    # Get alerts
    alerts_response = alerts_table.scan()
    alerts = alerts_response.get("Items", [])

    alerts.sort(
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )

    alerts = alerts[:10]

    # Determine machine status
    machine_status = "Offline"

    if latest_telemetry:
        try:
            timestamp = latest_telemetry.get("timestamp", "")

            last_time = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )

            # Simulator currently sends a timestamp without timezone
            if last_time.tzinfo is None:
                last_time = last_time.replace(
                    tzinfo=timezone.utc
                )

            now = datetime.now(timezone.utc)

            difference = (
                now - last_time
            ).total_seconds()

            if difference <= 15:
                machine_status = "Online"
            else:
                machine_status = "Offline"

        except Exception as e:
            print("Status calculation error:", str(e))
            machine_status = "Unknown"

    # Final response
    response_data = {
        "machine": {
            "device_id": "factory-machine-01",
            "status": machine_status
        },
        "latest_telemetry": latest_telemetry,
        "alerts": alerts,
        "total_alerts": len(alerts)
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS"
        },
        "body": json.dumps(
            response_data,
            default=decimal_to_int
        )
    }