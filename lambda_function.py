import os
import urllib3

http = urllib3.PoolManager()

import logging
import json
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the input received
    logger.info(f"FunctionHandler received: {event}")

    payload = json.dumps({
        "text": f"Issue Created: {event['issue']['html_url']}"
    })

    slack_url = os.getenv("SLACK_URL")
    r = http.request('POST', slack_url,
                 headers={'Content-Type': 'application/json'},
                 body=payload)
    if r:
        return r.read()
    else:
        logger.error(f"Request to Slack failed: {response.status_code} - {response.text}")
        return f"Error: {response.status_code}"