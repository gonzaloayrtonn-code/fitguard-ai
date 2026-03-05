#!/bin/bash
# FitGuard AI — Automated Deployment Script
# Google Cloud Run · Gemini Live Agent Challenge

set -e

PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="fitguard-ai"
IMAGE="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "================================================"
echo "  FITGUARD AI — AUTOMATED DEPLOYMENT"
echo "  Project: $PROJECT_ID"
echo "  Region:  $REGION"
echo "================================================"

# 1. Build container
echo ""
echo "[1/3] Building Docker image..."
gcloud builds submit --tag $IMAGE .

# 2. Deploy to Cloud Run
echo ""
echo "[2/3] Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10

# 3. Get URL
echo ""
echo "[3/3] Deployment complete!"
URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')
echo ""
echo "================================================"
echo "  APP LIVE AT: $URL"
echo "================================================"
