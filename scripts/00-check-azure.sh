#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
load_azure
az account show --query '{name:name,state:state}' -o table
az account list-locations --query '[].{Region:name,Display:displayName}' -o table
for provider in Microsoft.Compute Microsoft.ContainerService Microsoft.Network Microsoft.ContainerRegistry Microsoft.OperationalInsights Microsoft.Insights; do
  az provider show --namespace "$provider" --query '{Provider:namespace,State:registrationState}' -o table
done
az vm list-usage --location "$LOCATION" -o table
need python3
python3 scripts/check-sku.py
echo 'Estas consultas no garantizan capacidad. Valida cuota, restricciones y precio en el portal antes de crear AKS.'
