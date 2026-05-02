═══════════════════════════════════════════════════════════
VEHICLE DAMAGE DETECTION SYSTEM
CS5024 — Theory and Practice of Advanced AI Ecosystems
═══════════════════════════════════════════════════════════

STUDENT: Limbachiya Manthan
MODULE:  CS5024 AY2526

───────────────────────────────────────────────────────────
PROJECT OVERVIEW
───────────────────────────────────────────────────────────
A cloud-native vehicle damage detection system built on AWS.
Users upload a vehicle image via a web frontend. The image
is sent to an AWS Lambda function via API Gateway, which
calls an EC2-hosted Flask inference server, stores results
in DynamoDB and S3, and returns a prediction to the user.

───────────────────────────────────────────────────────────
FILE STRUCTURE
───────────────────────────────────────────────────────────
lambda_function.py   — AWS Lambda handler (Python)
model_server.py      — EC2 Flask inference server (Python)
Dockerfile           — Docker image for EC2 model server
index.html           — Frontend web application
requirements.txt     — Python dependencies for EC2 server
env_variables.txt    — Lambda environment variable reference
vehicle_damage.ipynb — Model notebook file
README.txt           — This file

───────────────────────────────────────────────────────────
AWS SERVICES USED
───────────────────────────────────────────────────────────
1.  Amazon S3          — Frontend hosting + image storage
2.  Amazon CloudFront  — CDN and HTTPS delivery
3.  Amazon API Gateway — REST API endpoint
4.  AWS Lambda         — Serverless orchestration
5.  Amazon EC2         — Flask model inference server
6.  Amazon ECR         — Docker image registry
7.  Amazon DynamoDB    — Prediction results storage
8.  Amazon SNS         — Low confidence alerts
9.  Amazon CloudWatch  — Monitoring and custom metrics
10. AWS IAM            — Roles and permissions
11. Amazon SageMaker   — ML notebook (development only)

───────────────────────────────────────────────────────────
DEPLOYMENT REGION
───────────────────────────────────────────────────────────
All services deployed in: eu-north-1 (Stockholm, Sweden)

───────────────────────────────────────────────────────────
LIVE URLS
───────────────────────────────────────────────────────────
Frontend (S3):
  http://damage-predictions-25022776.s3-website.eu-north-1.amazonaws.com

API Gateway endpoint:
  https://nwp613e5lb.execute-api.eu-north-1.amazonaws.com/dev/predict

───────────────────────────────────────────────────────────
HOW TO RUN LOCALLY (EC2 Flask server)
───────────────────────────────────────────────────────────
1. Install dependencies:
   pip install -r requirements.txt

2. Run the Flask server:
   python model_server.py

3. Test health endpoint:
   curl http://localhost:5000/health

4. Test predict endpoint:
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"image": "BASE64_STRING_HERE"}'

───────────────────────────────────────────────────────────
HOW TO DEPLOY LAMBDA
───────────────────────────────────────────────────────────
1. Open AWS Lambda Console
2. Create function → Python 3.x runtime
3. Paste contents of lambda_function.py
4. Set environment variables from env_variables.txt
5. Attach IAM role with required policies
6. Deploy

───────────────────────────────────────────────────────────
HOW TO BUILD AND PUSH DOCKER IMAGE TO ECR
───────────────────────────────────────────────────────────
1. Build:
   docker build -t damage-detection-model .

2. Tag:
   docker tag damage-detection-model:latest \
   YOUR_ACCOUNT_ID.dkr.ecr.eu-north-1.amazonaws.com/damage-detection-model:latest

3. Push:
   docker push \
   YOUR_ACCOUNT_ID.dkr.ecr.eu-north-1.amazonaws.com/damage-detection-model:latest

───────────────────────────────────────────────────────────
GOOGLE COLAB TRAINING NOTEBOOK
───────────────────────────────────────────────────────────
File: vehicle_damage_detection_training.ipynb

This notebook contains the full model training pipeline:
- Dataset loading and preprocessing
- Model architecture definition
- Training loop with validation
- Accuracy and loss evaluation
- Model export and save to file

To run:
1. Open in Google Colab at https://colab.research.google.com
2. Runtime -> Run all
3. GPU runtime recommended:
   Runtime -> Change runtime type → T4 GPU

───────────────────────────────────────────────────────────
TRAINED MODEL
───────────────────────────────────────────────────────────
The trained model file is stored in:
  AWS S3 bucket: vehicle-damage-bucket-25022776
  Region: eu-north-1