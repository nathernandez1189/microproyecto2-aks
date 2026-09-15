#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
export KUBECONFIG="$PROJECT_DIR/.kube/minikube.config"
[[ "$(kubectl config current-context)" == 'mp2-hpa' ]] || { echo 'Se requiere el contexto local mp2-hpa'; exit 1; }
mkdir -p evidencias/local
exec > >(tee evidencias/local/03-hpa-ciclo.txt) 2>&1
snapshot() { date -u '+%Y-%m-%dT%H:%M:%SZ'; kubectl -n mp2-hpa get hpa cpu-demo; kubectl -n mp2-hpa get deployment cpu-demo; }
stop_load() { kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":true}}' >/dev/null; }
trap stop_load EXIT
echo 'FASE 1: Antes de la carga'
snapshot
kubectl -n mp2-hpa patch job load-generator --type merge -p '{"spec":{"suspend":false}}'
echo 'FASE 2: Esperar aumento automático a cuatro réplicas disponibles'
grew=false
for i in {1..24}; do
  snapshot
  count="$(kubectl -n mp2-hpa get deployment cpu-demo -o jsonpath='{.status.availableReplicas}')"
  if [[ "${count:-0}" -ge 4 ]]; then grew=true; break; fi
  sleep 10
done
[[ "$grew" == true ]] || { echo 'FALLO: no se observaron cuatro réplicas disponibles'; exit 1; }
stop_load
echo 'FASE 3: Esperar reducción automática a una réplica'
shrunk=false
for i in {1..30}; do
  snapshot
  desired="$(kubectl -n mp2-hpa get deployment cpu-demo -o jsonpath='{.spec.replicas}')"
  ready="$(kubectl -n mp2-hpa get deployment cpu-demo -o jsonpath='{.status.availableReplicas}')"
  if [[ "$desired" == 1 && "${ready:-0}" == 1 ]]; then shrunk=true; break; fi
  sleep 10
done
kubectl -n mp2-hpa describe hpa cpu-demo
[[ "$shrunk" == true ]] || { echo 'FALLO: no se observó regreso a una réplica'; exit 1; }
echo 'PASS: HPA local creció hasta cuatro y regresó a una réplica sin usar kubectl scale.'
