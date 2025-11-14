# Serverless-Web-Application
Deploying Serverless Web Application on AWS: S3, API Gateway, Lambda, DynamoDB and CloudFront

Deploying a Serverless Web Application on AWS
Using S3, CloudFront, API Gateway, Lambda, and DynamoDB
🚀 Project Overview

This project demonstrates how to deploy a fully serverless web application using AWS managed services:

Amazon S3 – Static website hosting

Amazon CloudFront – Global CDN for caching and performance

Amazon API Gateway – REST API interface

AWS Lambda – Serverless backend compute

Amazon DynamoDB – NoSQL database

The application allows users to insert and retrieve student data using a clean serverless architecture.

🏗 Architecture
User → CloudFront → S3 (Frontend) → API Gateway → Lambda (GET/POST) → DynamoDB

🌐 Live Resources
Component	URL
S3 Static Website :	http://devops-master-bucket123456.s3-website.ap-south-1.amazonaws.com/

API Gateway Invoke URL : https://29t07zklok.execute-api.ap-south-1.amazonaws.com/prod

CloudFront URL	: https://d1y0l2mqbj21dy.cloudfront.net/

🛠 AWS Services Used

1️⃣ Amazon S3

Hosts frontend HTML/CSS/JS
Acts as the origin for CloudFront
Public read access (via static hosting)

2️⃣ Amazon CloudFront

Improves performance globally
Custom domain + SSL (optional)
Caches static website assets

3️⃣ Amazon API Gateway

Handles GET, POST, and OPTIONS
Lambda Proxy Integration enabled
CORS fully configured

4️⃣ AWS Lambda

Two functions:
🟧 GET Lambda — Fetch Students

import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('studentData')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps(data, cls=DecimalEncoder)
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}



🟧 POST Lambda — Insert Students

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


🗂 Database – DynamoDB

Table: studentData
Primary Key: studentid (String)

Additional Attributes:
name
class
age


📁 Project Structure

serverless-student-app/
│
├── frontend/
│   ├── index.html
│   ├── app.js
│
│
├── lambdas/
│   ├── getStudent.py
│   └── insertStudent.py
│
├── architecture-diagram.png
│
└── README.md


📝 Deployment Steps
1. Upload website to S3
2. Create CloudFront distribution
3. Create DynamoDB table
4. Create Lambda functions
5. Create API Gateway (GET, POST, OPTIONS)
6. Test APIs and enable CORS
7. Connect frontend to API URL
