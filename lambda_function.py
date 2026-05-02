import json
import base64
import random
import boto3
import uuid
import os
from datetime import datetime
from decimal import Decimal

# AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')

# CORS headers on every response
CORS_HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key",
    "Access-Control-Allow-Methods": "POST,OPTIONS"
}

def put_cloudwatch_metric(predicted_class, confidence):
    try:
        cloudwatch.put_metric_data(
            Namespace='DamageDetection',
            MetricData=[
                {
                    'MetricName': 'PredictionConfidence',
                    'Value': confidence,
                    'Unit': 'None',
                    'Dimensions': [
                        {'Name': 'PredictedClass', 'Value': predicted_class}
                    ]
                },
                {
                    'MetricName': 'TotalPredictions',
                    'Value': 1,
                    'Unit': 'Count'
                }
            ]
        )
    except Exception as e:
        print(f"CloudWatch metric error (non-fatal): {str(e)}")

def lambda_handler(event, context):

    # Handle preflight OPTIONS
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": CORS_HEADERS, "body": ""}

    try:
        body = event.get("body", None)

        if body is None:
            raise Exception("Request body is empty")

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                pass

        if isinstance(body, dict) and "image" in body:
            img_b64 = body["image"]
        else:
            raise Exception("Image key not found in request body")

        # Decode and measure image
        img_data = base64.b64decode(img_b64)
        image_size = len(img_data)

       
        # SIMULATED ML INFERENCE
       
        classes = ["damaged", "no_damage", "unknown"]
        predicted_class = random.choice(classes)
        confidence = round(random.uniform(0.80, 0.97), 4)
        prediction_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

      
        # SAVE IMAGE TO S3
        
        bucket_name = os.environ.get("BUCKET_NAME")
        s3_key = "N/A"
        if bucket_name:
            s3_key = f"images/{prediction_id}.jpg"
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=img_data,
                ContentType="image/jpeg"
            )

   
        # SAVE TO DYNAMODB
       
        table_name = os.environ.get("DYNAMODB_TABLE", "predictions")
        table = dynamodb.Table(table_name)
        table.put_item(Item={
            "prediction_id":    prediction_id,
            "timestamp":        timestamp,
            "predicted_class":  predicted_class,
            "confidence":       Decimal(str(confidence)),
            "s3_key":           s3_key,
            "server":           "EC2",
            "image_size_bytes": image_size
        })

     
        # CLOUDWATCH CUSTOM METRICS
    
        put_cloudwatch_metric(predicted_class, confidence)

     
        # SNS ALERT IF LOW CONFIDENCE
  
        sns_topic_arn = os.environ.get("SNS_TOPIC_ARN")
        if sns_topic_arn and confidence < 0.85:
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Subject="Low Confidence Prediction Alert",
                Message=(
                    f"Prediction ID: {prediction_id}\n"
                    f"Class: {predicted_class}\n"
                    f"Confidence: {confidence}\n"
                    f"Timestamp: {timestamp}\n"
                    f"Server: EC2"
                )
            )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "prediction_id":    prediction_id,
                "predicted_class":  predicted_class,
                "confidence":       confidence,
                "timestamp":        timestamp,
                "server":           "EC2",
                "image_size_bytes": image_size,
                "note":             "Inference complete — result stored in DynamoDB and S3"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "error": str(e),
                "debug_event_body": str(event.get("body", ""))[:200]
            })
        }