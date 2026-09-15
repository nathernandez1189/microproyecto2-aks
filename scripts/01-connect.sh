#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
connect_aks
origin="${1:-cli-local}"
case "$origin" in cli-local|cloud-shell) ;; *) echo 'Usa cli-local o cloud-shell'; exit 1;; esac
mkdir -p evidencias/azure
{
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  echo "ORIGEN=$origin"
  kubectl version
  kubectl cluster-info
  kubectl get nodes -o wide
} | tee "evidencias/azure/01-nodos-$origin.txt"
ready="$(kubectl get nodes -o go-template='{{range .items}}{{range .status.conditions}}{{if and (eq .type "Ready") (eq .status "True")}}ready{{"\n"}}{{end}}{{end}}{{end}}' | wc -l | tr -d ' ')"
[[ "$ready" -ge 2 ]] || { echo 'No hay al menos dos nodos Ready. El punto 1 aún no cumple.' >&2; exit 1; }
echo 'AKS tiene al menos dos nodos Ready.'
