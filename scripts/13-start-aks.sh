#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
# Starting the existing cluster resumes compute charges. No resources are recreated.
az aks start -g "$RESOURCE_GROUP" -n "$AKS_NAME" --output none
connect_aks
kubectl wait --for=condition=Ready nodes --all --timeout=600s
kubectl -n microproyecto2 rollout status deployment/classifier --timeout=600s
kubectl -n microproyecto2 rollout status deployment/planner --timeout=300s
kubectl -n microproyecto2 get pods,pvc -o wide
echo 'Clúster iniciado. Abre las aplicaciones con bash scripts/04-open-apps.sh.'
