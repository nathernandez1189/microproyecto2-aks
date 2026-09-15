#!/usr/bin/env bash
# Prepare a fresh, suspended load Job without changing application replicas.
source "$(dirname "$0")/common.sh"
export KUBECONFIG="$PROJECT_DIR/.kube/minikube.config"
[[ "$(kubectl config current-context)" == mp2-hpa ]] || { echo 'Se requiere el contexto local mp2-hpa'; exit 1; }
need python3
mkdir -p build
python3 -c 'import re; from pathlib import Path; blocks=re.split(r"^---\s*$", Path("k8s/hpa/demo.yaml").read_text(), flags=re.M); jobs=[b for b in blocks if re.search(r"^kind: Job$", b, re.M)]; assert len(jobs)==1 and "name: load-generator" in jobs[0]; print(jobs[0].strip())' > build/hpa-load-job.yaml
kubectl create --dry-run=client -f build/hpa-load-job.yaml -o name
kubectl -n mp2-hpa delete job load-generator --ignore-not-found --wait=true
kubectl apply -f build/hpa-load-job.yaml
echo 'Generador nuevo y suspendido. Ejecuta bash scripts/09-verify-hpa.sh para comprobar el ciclo.'
