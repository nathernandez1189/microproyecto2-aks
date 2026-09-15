#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
need docker
need kubectl
MINIKUBE_BIN="${MINIKUBE_BIN:-minikube}"
[[ -x .tools/minikube ]] && MINIKUBE_BIN="$PROJECT_DIR/.tools/minikube"
command -v "$MINIKUBE_BIN" >/dev/null || { echo 'Instala Minikube o pon el ejecutable en .tools/minikube'; exit 1; }
mkdir -p .kube .tools/minikube-home evidencias/local
export KUBECONFIG="$PROJECT_DIR/.kube/minikube.config"
export MINIKUBE_HOME="$PROJECT_DIR/.tools/minikube-home"
"$MINIKUBE_BIN" start -p mp2-hpa --driver=docker --cpus=2 --memory=3072mb --kubernetes-version=v1.34.0
"$MINIKUBE_BIN" -p mp2-hpa addons enable metrics-server
docker build -t mp2-loadtarget:v1 -f apps/loadtarget/Dockerfile .
"$MINIKUBE_BIN" -p mp2-hpa image load mp2-loadtarget:v1
kubectl apply -f k8s/hpa/demo.yaml
kubectl -n mp2-hpa rollout status deployment/cpu-demo --timeout=240s
echo 'Entorno HPA local preparado. Sigue docs/04-HPA.md para iniciar y detener la carga.'
