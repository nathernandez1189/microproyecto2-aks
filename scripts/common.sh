#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"
need() { command -v "$1" >/dev/null || { echo "Falta la herramienta: $1" >&2; exit 1; }; }
load_azure() {
  need az
  # Reuse this project's isolated login, when present, without changing other projects.
  if [[ -z "${AZURE_CONFIG_DIR:-}" && -d "$PROJECT_DIR/.azure" ]]; then
    export AZURE_CONFIG_DIR="$PROJECT_DIR/.azure"
  fi
  [[ -f .env ]] || { echo 'Copia .env.example a .env y completa tus datos.' >&2; exit 1; }
  set -a
  source .env
  set +a
  for key in SUBSCRIPTION_ID RESOURCE_GROUP AKS_NAME LOCATION ACR_NAME LOG_WORKSPACE IMAGE_TAG; do
    [[ -n "${!key:-}" && "${!key}" != *REEMPLAZAR* ]] || { echo "Completa $key en .env" >&2; exit 1; }
  done
  [[ "$ACR_NAME" =~ ^[a-zA-Z0-9]{5,50}$ ]] || { echo 'ACR_NAME debe contener 5 a 50 letras o números.' >&2; exit 1; }
  az account set --subscription "$SUBSCRIPTION_ID"
}
connect_aks() {
  need kubectl
  mkdir -p .kube
  export KUBECONFIG="$PROJECT_DIR/.kube/aks.config"
  az aks get-credentials --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME" --file "$KUBECONFIG" --overwrite-existing
  chmod 600 "$KUBECONFIG"
}
