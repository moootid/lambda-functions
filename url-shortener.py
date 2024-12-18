import json
import uuid
import boto3
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'UrlShortener'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse the input URL from the query string parameters
        query_params = event.get("queryStringParameters", {})
        long_url = query_params.get("url")
        if not long_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' parameter."})
            }

        # Generate a unique ID for the short URL
        short_id = str(uuid.uuid4())[:8]  # Shorten the UUID to 8 characters

        # Store the mapping in DynamoDB
        table.put_item(
            Item={
                "id": short_id,
                "long_url": long_url,
                "number_of_clicks": 0
            }
        )

        # Construct the short URL
        short_url = f"https://short.mokh32.com/g/{short_id}"

        return {
            "statusCode": 200,
            "body": json.dumps({"short_url": short_url}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
