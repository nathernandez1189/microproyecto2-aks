#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
az monitor log-analytics workspace create --resource-group "$RESOURCE_GROUP" --workspace-name "$LOG_WORKSPACE" --location "$LOCATION" --retention-time 30
workspace_id="$(az monitor log-analytics workspace show -g "$RESOURCE_GROUP" -n "$LOG_WORKSPACE" --query id -o tsv)"
az aks enable-addons --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME" --addons monitoring --workspace-resource-id "$workspace_id" --data-collection-settings monitoring/data-collection.json
echo 'Container Insights habilitado. Espera la ingestión y sigue docs/03-MONITOREO.md.'
