#!/bin/bash
set -euo pipefail

PROJECT_ID=adktest-460913
REGION=us-central1
SERVICE_NAME=weather-backend
REPO=adk-repo
IMAGE_NAME=weather-backend
TAG=v4
IMAGE_URI=us-central1-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE_NAME:$TAG
SA_NAME=cloud-run-vertex
SA_EMAIL=$SA_NAME@$PROJECT_ID.iam.gserviceaccount.com

gcloud config set project "$PROJECT_ID"

docker buildx build \
  --platform linux/amd64 \
  -t "$IMAGE_URI" \
  -f Dockerfile \
  --push .

if ! gcloud iam service-accounts list --format="value(email)" | grep -q "$SA_EMAIL"; then
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="Cloud Run → Vertex AI service account"
fi

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user" || true

gcloud run deploy "$SERVICE_NAME" \
  --image "$IMAGE_URI" \
  --region "$REGION" \
  --allow-unauthenticated \
  --service-account "$SA_EMAIL"
