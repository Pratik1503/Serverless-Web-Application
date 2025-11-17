# 🌐 Serverless Web Application on AWS

Deploying a Serverless Web Application using **S3, CloudFront, API Gateway, Lambda, and DynamoDB**

---

## 🚀 Project Overview

This project demonstrates how to deploy a **fully serverless web application** on AWS using managed services.
The application allows users to **insert and retrieve student data** using a clean, scalable, pay-per-use architecture.

### 🧩 **AWS Services Used**

* **Amazon S3** – Static website hosting (Frontend)
* **Amazon CloudFront** – Global CDN for performance + caching
* **Amazon API Gateway** – REST API interface
* **AWS Lambda** – Serverless compute for backend (GET & POST)
* **Amazon DynamoDB** – NoSQL database for student records

---

## 🏗 Architecture

```
User → CloudFront → S3 (Frontend)
                     ↓
                  API Gateway → Lambda (GET / POST) → DynamoDB
```

---

## 🌐 Live Resources

| Component                  | URL                                                                                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **S3 Static Website**      | [http://devops-master-bucket123456.s3-website.ap-south-1.amazonaws.com/](http://devops-master-bucket123456.s3-website.ap-south-1.amazonaws.com/) |
| **API Gateway Invoke URL** | [https://29t07zklok.execute-api.ap-south-1.amazonaws.com/prod](https://29t07zklok.execute-api.ap-south-1.amazonaws.com/prod)                     |
| **CloudFront URL**         | [https://d1y0l2mqbj21dy.cloudfront.net/](https://d1y0l2mqbj21dy.cloudfront.net/)                                                                 |

---

# 🛠 AWS Services Used (Detailed)

---

## 1️⃣ Amazon S3 (Frontend Hosting)

* Hosts the **HTML / CSS / JavaScript** frontend
* Public read access via static website hosting
* Acts as the **origin for CloudFront**
* Easy to update and version

---

## 2️⃣ Amazon CloudFront (CDN)

* Speed up global delivery of frontend
* Caches static files (HTML, JS, CSS)
* Optional custom domain + SSL
* Origin = S3 bucket

---

## 3️⃣ Amazon API Gateway (REST API)

* Handles:

  * **GET** → Retrieve student data
  * **POST** → Insert student data
  * **OPTIONS** → CORS preflight
* Lambda Proxy Integration enabled
* CORS enabled for full browser support

---

## 4️⃣ AWS Lambda Functions

Two Lambda functions handle database operations.

---

### 🟧 **GET Lambda — Fetch Students**

```python
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
```

---

### 🟧 **POST Lambda — Insert Students**

```python
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
```

---

## 5️⃣ DynamoDB — NoSQL Database

**Table Name:** `studentData`

| Attribute | Type                 |
| --------- | -------------------- |
| studentid | String (Primary Key) |
| name      | String               |
| class     | String               |
| age       | Number               |

---

# 📁 Project Structure

```
serverless-student-app/
│
├── frontend/
│   ├── index.html
│   └── app.js
│
├── lambdas/
│   ├── getStudent.py
│   └── insertStudent.py
│
├── architecture-diagram.png
│
└── README.md
```

---

# 📝 Deployment Steps

### **1. Upload frontend to S3**

* Enable static website hosting
* Upload index.html & app.js
* Make files public

---

### **2. Create CloudFront Distribution**

* Origin → S3 bucket website endpoint
* Caching enabled
* HTTPS enabled (optional)

---

### **3. Create DynamoDB Table**

* Table name: `studentData`
* Primary key: `studentid` (String)

---

### **4. Create Lambda Functions**

* Add code for GET & POST
* Set environment variables (optional)

---

### **5. Create API Gateway**

* Method: GET → GET Lambda
* Method: POST → POST Lambda
* Enable CORS
* Deploy to `/prod`

---

### **6. Connect Frontend to API URL**

Update `app.js`:

```js
const apiUrl = "https://29t07zklok.execute-api.ap-south-1.amazonaws.com/prod";
```

---

### **7. Test Application**

* Open CloudFront URL
* Insert student data
* Retrieve student list
* Confirm DynamoDB updates

---

# 🎯 Final Result

✔ Fully serverless
✔ Auto-scaling
✔ No servers to manage
✔ Low-cost
✔ Highly available
✔ Production-ready architecture

---

If you want, I can also generate:

✅ Architecture diagram in PNG
✅ A version of README with images
✅ A Terraform/IaC version
✅ A video explanation script

Just tell me!
