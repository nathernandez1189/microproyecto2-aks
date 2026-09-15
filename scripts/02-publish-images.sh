#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
az aks show -g "$RESOURCE_GROUP" -n "$AKS_NAME" --query provisioningState -o tsv
# Creates a registry inside the project group. This consumes Azure credit.
if ! az acr show -g "$RESOURCE_GROUP" -n "$ACR_NAME" >/dev/null 2>&1; then
  az acr create -g "$RESOURCE_GROUP" -n "$ACR_NAME" --sku Basic --admin-enabled false --role-assignment-mode rbac
fi
mode="$(az acr show -g "$RESOURCE_GROUP" -n "$ACR_NAME" --query roleAssignmentMode -o tsv)"
[[ "$mode" != 'AbacRepositoryPermissions' ]] || { echo 'Este ACR usa ABAC: consulta docs/02-AZURE.md antes de continuar.' >&2; exit 1; }
registry="$(az acr show -g "$RESOURCE_GROUP" -n "$ACR_NAME" --query loginServer -o tsv)"
az aks update -g "$RESOURCE_GROUP" -n "$AKS_NAME" --attach-acr "$ACR_NAME" --output none
build_mode="${BUILD_MODE:-acr}"
# ACR Tasks is not available in Chile Central; the registry itself is supported.
if [[ "$LOCATION" == 'chilecentral' ]]; then build_mode=local; fi
if [[ "$build_mode" == local ]]; then
  need docker
  az acr login --name "$ACR_NAME"
fi
for app in classifier planner; do
  # Builds amd64 even when the student's laptop uses Apple Silicon.
  if [[ "$build_mode" == local ]]; then
    docker buildx build --platform linux/amd64 --tag "$registry/mp2-$app:$IMAGE_TAG" --file "apps/$app/Dockerfile" --push .
  else
    az acr build --registry "$ACR_NAME" --platform linux/amd64 --image "mp2-$app:$IMAGE_TAG" --file "apps/$app/Dockerfile" .
  fi
done
echo "Imágenes disponibles en $registry. Continúa con 03-deploy.sh."
