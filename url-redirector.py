import json
import boto3
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'UrlShortener'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parse the 'id' from the query string parameters
        query_params = event.get("queryStringParameters", {})
        short_id = query_params.get("id")
        if not short_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'id' parameter."})
            }

        # Retrieve the corresponding long URL from DynamoDB
        response = table.get_item(Key={"id": short_id})
        item = response.get("Item")
        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Short URL not found."})
            }

        long_url = item["long_url"]

        number_of_clicks = item["number_of_clicks"]
        number_of_clicks = number_of_clicks + 1

        table.put_item(
            Item={
                "id": short_id,
                "long_url": long_url,
                "number_of_clicks": number_of_clicks
            }
        )

        # Redirect to the long URL
        return {
            "statusCode": 200,
            "body": json.dumps({"long_url": long_url}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
