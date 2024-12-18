import simplejson as json
import boto3
import os

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'UrlShortener'
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    response = table.scan()
    items = response.get('Items', [])
    # Format the response
    formatted_items = [
        {
            "id": item["id"],
            "long_url": item["long_url"],
            "short_url": f"https://short.mokh32.com/g/{item['id']}",
            "number_of_clicks": item.get("number_of_clicks", 0)  # Default to 0 if number_of_clicks is missing
        }
        for item in items
    ]

    return {
        'statusCode': 200,
        'body': json.dumps(formatted_items),
        "headers": {
            "Content-Type": "application/json"
        }
    }
