# #!/bin/bash

# SERVICE_NAME="ai-paint" # Define your service name here. Example "test-portal"
# PROJECT_NAME="teachmemedical"

# # Step 1: Build and push the container image
# gcloud builds submit --tag gcr.io/${PROJECT_NAME}/${SERVICE_NAME} .

# # Step 2: Deploy the Cloud Run service 
# gcloud run deploy ${SERVICE_NAME} \
#     --image=gcr.io/${PROJECT_NAME}/${SERVICE_NAME} \
#     --region=us-east1 \
#     --allow-unauthenticated \
#     --platform managed \
#     --project ${PROJECT_NAME}  \
#     --quiet









#!/bin/bash

SERVICE_NAME="ai-paint"
REGION="us-east1"
PROJECT="teachmemedical"
REPO_NAME="noah-artifacts"

# Build and push to Artifact Registry
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT}/${REPO_NAME}/${SERVICE_NAME} .

# Deploy to Cloud Run
gcloud run deploy ${SERVICE_NAME} \
    --image=${REGION}-docker.pkg.dev/${PROJECT}/${REPO_NAME}/${SERVICE_NAME} \
    --region=${REGION} \
    --allow-unauthenticated \
    --platform managed \
    --project ${PROJECT} \
    --quiet