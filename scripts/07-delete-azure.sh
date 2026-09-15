#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
echo 'Este script elimina TODO el grupo indicado: AKS, ACR, Log Analytics y los datos asociados.'
echo 'Usa exclusivamente un grupo dedicado a este microproyecto. Guarda antes las evidencias y exporta las tareas.'
az resource list -g "$RESOURCE_GROUP" --query '[].{Name:name,Type:type}' -o table
node_group="$(az aks show -g "$RESOURCE_GROUP" -n "$AKS_NAME" --query nodeResourceGroup -o tsv)"
echo "Grupo de nodos administrado por AKS: $node_group"
read -r -p "Escribe ELIMINAR $RESOURCE_GROUP para confirmar: " confirmation
[[ "$confirmation" == "ELIMINAR $RESOURCE_GROUP" ]] || { echo 'Cancelado.'; exit 1; }
az group delete --name "$RESOURCE_GROUP" --yes
echo 'Verificación: ambos grupos deberían devolver false.'
az group exists -n "$RESOURCE_GROUP"
az group exists -n "$node_group"
echo 'Revisa en el portal recursos externos al grupo y Cost Management; la información de consumo puede llegar con retraso.'
