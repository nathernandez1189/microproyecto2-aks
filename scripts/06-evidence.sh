#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
connect_aks
destination="evidencias/azure/$(date -u '+%Y%m%dT%H%M%SZ')"
mkdir -p "$destination"
kubectl get nodes -o wide > "$destination/nodos.txt"
kubectl -n microproyecto2 get deployments,pods,services,pvc -o wide > "$destination/recursos.txt"
kubectl -n microproyecto2 get events --sort-by=.metadata.creationTimestamp > "$destination/eventos.txt"
kubectl top nodes > "$destination/cpu-nodos.txt" 2>&1 || echo 'Métricas de nodos pendientes.'
kubectl -n microproyecto2 top pods > "$destination/cpu-pods.txt" 2>&1 || echo 'Métricas de Pods pendientes.'
kubectl -n microproyecto2 logs -l app=classifier --all-containers --tail=100 --prefix > "$destination/classifier-logs.txt"
kubectl -n microproyecto2 logs -l app=planner --all-containers --tail=100 --prefix > "$destination/planner-logs.txt"
az aks show -g "$RESOURCE_GROUP" -n "$AKS_NAME" --query '{name:name,location:location,kubernetesVersion:kubernetesVersion,pools:agentPoolProfiles[].{name:name,count:count,vmSize:vmSize},monitoring:addonProfiles.omsagent.enabled}' > "$destination/aks-resumen.json"
echo "Evidencias guardadas en $destination. Añade las capturas del portal según docs/05-EVIDENCIAS.md."
