#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
connect_aks
pids=()
cleanup() { for pid in "${pids[@]}"; do kill "$pid" 2>/dev/null || true; done; }
trap cleanup EXIT INT TERM
kubectl -n microproyecto2 port-forward --address 127.0.0.1 service/classifier 8081:80 &
pids+=("$!")
kubectl -n microproyecto2 port-forward --address 127.0.0.1 service/planner 8082:80 &
pids+=("$!")
echo 'Visión AI: http://localhost:8081 | Campus Planner: http://localhost:8082'
echo 'Mantén esta terminal abierta. Ctrl+C cierra ambos túneles. Si falla un Pod, vuelve a ejecutar el script.'
wait
