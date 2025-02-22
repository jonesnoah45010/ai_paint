#!/bin/bash

SERVICE_NAME="ai-paint" # Define your service name here. Example "test-portal"
PROJECT_NAME="YOUR_GOOGLE_CLOUD_CONSOLE_PROJECT_NAME_HERE"

# Step 1: Build and push the container image
gcloud builds submit --tag gcr.io/${PROJECT_NAME}/${SERVICE_NAME} .

# Step 2: Deploy the Cloud Run service 
gcloud run deploy ${SERVICE_NAME} \
    --image=gcr.io/${PROJECT_NAME}/${SERVICE_NAME} \
    --region=us-east1 \
    --allow-unauthenticated \
    --platform managed \
    --project ${PROJECT_NAME}  \
    --quiet