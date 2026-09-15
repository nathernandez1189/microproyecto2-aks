#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
connect_aks
[[ "$(kubectl config current-context)" == "$AKS_NAME" ]] || { echo 'Contexto AKS incorrecto'; exit 1; }
need python3
mkdir -p evidencias/azure
exec > >(tee evidencias/azure/04-pruebas-aks.txt) 2>&1
pids=()
cleanup() { for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done; }
trap cleanup EXIT
kubectl -n microproyecto2 port-forward service/classifier 8083:80 > build/classifier-tunnel.log 2>&1 &
pids+=("$!")
open_planner() {
  kubectl -n microproyecto2 port-forward service/planner 8084:80 > build/planner-tunnel.log 2>&1 &
  planner_pid=$!
  pids+=("$planner_pid")
  curl --retry 20 --retry-delay 1 --retry-connrefused --fail --silent http://127.0.0.1:8084/readyz
}
open_planner
curl --retry 20 --retry-delay 1 --retry-connrefused --fail --silent http://127.0.0.1:8083/readyz
echo
date -u '+%Y-%m-%dT%H:%M:%SZ'
CLASSIFIER_URL=http://127.0.0.1:8083 PLANNER_URL=http://127.0.0.1:8084 python3 -m unittest discover -s tests -v
kubectl -n microproyecto2 get pods,pvc -o wide
curl --fail --silent -H 'Content-Type: application/json' -d '{"title":"Persistencia AKS verificada","course":"Computación en la Nube"}' http://127.0.0.1:8084/api/tasks > build/task-persistence.json
before="$(kubectl -n microproyecto2 get pod -l app=planner -o jsonpath='{.items[0].metadata.uid}')"
echo "Pod UID anterior: $before"
volume_before="$(kubectl -n microproyecto2 get pvc planner-data -o jsonpath='{.spec.volumeName}')"
kubectl -n microproyecto2 rollout restart deployment/planner
kubectl -n microproyecto2 rollout status deployment/planner --timeout=180s
kill "$planner_pid" 2>/dev/null || true
wait "$planner_pid" 2>/dev/null || true
open_planner
after="$(kubectl -n microproyecto2 get pod -l app=planner -o jsonpath='{.items[0].metadata.uid}')"
echo "Pod UID nuevo: $after"
[[ "$before" != "$after" ]] || { echo 'El Pod no cambió'; exit 1; }
volume_after="$(kubectl -n microproyecto2 get pvc planner-data -o jsonpath='{.spec.volumeName}')"
[[ "$volume_before" == "$volume_after" ]] || { echo 'El volumen cambió'; exit 1; }
echo "Volumen conservado: $volume_after"
curl --fail --silent -F img=@tests/fixtures/dog.jpg http://127.0.0.1:8083/predict > evidencias/azure/04-inferencia.json
python3 - <<'PY'
import json
from pathlib import Path
from urllib.request import urlopen
original = json.loads(Path('build/task-persistence.json').read_text())
tasks = json.load(urlopen('http://127.0.0.1:8084/api/tasks'))['tasks']
assert original in tasks, 'La tarea desapareció al reemplazar el Pod'
print('PASS: el nuevo Pod conserva la tarea en el mismo PVC:', original)
PY
kubectl -n microproyecto2 get pods,pvc -o wide
kubectl -n microproyecto2 logs -l app=classifier --tail=8 --prefix
echo 'PASS: 12 pruebas HTTP y persistencia completadas en Azure AKS con Azure Disk.'
