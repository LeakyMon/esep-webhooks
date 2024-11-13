import os
import json
import requests  # Ensure requests is included in your deployment package

def lambda_handler(event, context):
    slack_url = os.environ.get('SLACK_URL')
    if not slack_url:
        return {
            'statusCode': 500,
            'body': json.dumps('Slack URL not found in environment variables')
        }
    
    # Get ther relevant data from github for issues
    issue = event.get('issue', {})
    payload = {
        "text": "New GitHub Issue Created!",
        "attachments": [
            {
                "title": issue.get("title", "No title"),
                "title_link": issue.get("html_url", "#"),
                "text": issue.get("body", "No description")
            }
        ]
    }

    # Send the PAYLOAD TO SLACK
    response = requests.post(slack_url, json=payload)
    if response.status_code != 200:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to send message to Slack')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message sent to Slack successfully')
    }
