import os
import urllib3
import logging
import json

http = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Check if event is a JSON string; if so, parse it
    if isinstance(event, str):
        try:
            event = json.loads(event)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding failed: {e}")
            return {
                "statusCode": 400,
                "body": "Invalid JSON format in event input"
            }
    
    # Log the input received
    logger.info(f"FunctionHandler received: {event}")

    # Construct payload for Slack
    payload = json.dumps({
        "text": f"Issue Created: {event.get('issue', {}).get('html_url', 'No URL provided')}"
    })

    # Send the request to Slack
    slack_url = os.getenv("SLACK_URL")
    r = http.request('POST', slack_url,
                     headers={'Content-Type': 'application/json'},
                     body=payload)
    if r:
        return {
            "statusCode": r.status,
            "body": r.data.decode("utf-8")
        }
    else:
        logger.error("Request to Slack failed.")
        return {
            "statusCode": 500,
            "body": "Failed to send message to Slack"
        }
