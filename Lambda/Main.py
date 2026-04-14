import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = "REPLACE_WITH_YOUR_SNS_TOPIC_ARN"

def lambda_handler(event, context):
    detail = event.get("detail", {})
    event_name = detail.get("eventName", "Unknown")

    # Detection logic
    if event_name in ["ListUsers", "ListRoles"]:
        message = f"⚠️ Recon activity detected → {event_name}"

    elif event_name in ["CreateAccessKey", "AttachUserPolicy"]:
        message = f"🚨 Privilege escalation detected → {event_name}"

    else:
        message = f"ℹ️ Other activity → {event_name}"

    # Send SNS alert
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="AWS Security Alert"
    )

    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }
