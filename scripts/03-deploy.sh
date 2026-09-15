#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
connect_aks
need python3
registry="$(az acr show -g "$RESOURCE_GROUP" -n "$ACR_NAME" --query loginServer -o tsv)"
mkdir -p build
kubectl kustomize k8s/overlays/aks > build/aks-template.yaml
python3 scripts/render_images.py "$registry" "$IMAGE_TAG" build/aks-template.yaml build/aks.yaml
kubectl apply -f k8s/base/namespace.yaml
kubectl apply --dry-run=server -f build/aks.yaml
kubectl apply -f build/aks.yaml
kubectl -n microproyecto2 rollout status deployment/classifier --timeout=600s
kubectl -n microproyecto2 rollout status deployment/planner --timeout=300s
kubectl -n microproyecto2 get deployments,pods,services,pvc -o wide
echo 'Aplicaciones desplegadas. Ejecuta scripts/04-open-apps.sh para acceder.'
