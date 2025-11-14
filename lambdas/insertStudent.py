import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('studentData')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        table.put_item(
            Item={
                'studentid': body['studentid'],
                'name': body['name'],
                'class': body['class'],
                'age': body['age']
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps("Student data saved successfully!")
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
