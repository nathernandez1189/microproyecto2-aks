#!/usr/bin/env python3
"""Query the regional Compute catalog with server-side filtering and pagination."""
import json
import os
import subprocess
import urllib.parse

query = urllib.parse.urlencode({
    'api-version': '2021-07-01',
    '$filter': f"location eq '{os.environ['LOCATION']}'",
})
subscription = os.environ['SUBSCRIPTION_ID']
url = f'https://management.azure.com/subscriptions/{subscription}/providers/Microsoft.Compute/skus?{query}'
target = os.environ.get('NODE_VM_SIZE', 'Standard_DS2_v2')
matches = []
while url:
    result = subprocess.run(
        ['az', 'rest', '--method', 'get', '--url', url, '-o', 'json'],
        check=True, text=True, capture_output=True, timeout=120,
    )
    page = json.loads(result.stdout)
    matches.extend(sku for sku in page.get('value', [])
                   if sku.get('resourceType') == 'virtualMachines' and sku.get('name') == target)
    url = page.get('nextLink')
print(json.dumps(matches, indent=2, ensure_ascii=False))
if not matches:
    raise SystemExit(f'No se encontró {target} en {os.environ["LOCATION"]}.')
