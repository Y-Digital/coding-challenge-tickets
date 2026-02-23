#!/usr/bin/env bash
# ------------------------------------------------------------------
# Deploy to Azure Container Apps — template script
#
# Prerequisites:
#   - az cli installed & logged in (az login)
#   - Docker image built locally
#
# TODO (candidate):
#   Fill in the <PLACEHOLDERS> below with the values you receive.
# ------------------------------------------------------------------

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────
RESOURCE_GROUP="<RESOURCE_GROUP>"
LOCATION="eastus"
ACR_NAME="<ACR_NAME>"
IMAGE_NAME="triage-api"
IMAGE_TAG="latest"
CONTAINER_APP_NAME="triage-api"
CONTAINER_APP_ENV="<CONTAINER_APP_ENV>"

# ── Build & push image ──────────────────────────────────────────
echo "==> Building Docker image..."
docker build -t "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" .

echo "==> Logging into ACR..."
az acr login --name "$ACR_NAME"

echo "==> Pushing image..."
docker push "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"

# ── Deploy to Container Apps ────────────────────────────────────
echo "==> Deploying to Container Apps..."
az containerapp up \
  --name "$CONTAINER_APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --environment "$CONTAINER_APP_ENV" \
  --image "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_OPENAI_ENDPOINT=secretref:azure-openai-endpoint \
    AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key \
    AZURE_OPENAI_DEPLOYMENT=secretref:azure-openai-deployment \
    AZURE_OPENAI_API_VERSION=secretref:azure-openai-api-version

echo "==> Done. Check the FQDN in the output above."
