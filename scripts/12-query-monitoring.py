"""Export real Azure Monitor query results without exposing authentication tokens."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
os.chdir(root)
os.environ.setdefault('AZURE_CONFIG_DIR', str(root / '.azure'))
settings = dict(line.split('=', 1) for line in (root / '.env').read_text().splitlines() if line and not line.startswith('#'))
workspace = subprocess.check_output(['az', 'monitor', 'log-analytics', 'workspace', 'show', '-g', settings['RESOURCE_GROUP'], '-n', settings['LOG_WORKSPACE'], '--query', 'customerId', '-o', 'tsv'], text=True).strip()
queries = (root / 'monitoring/queries.kql').read_text().split('\n\n')
out = root / 'evidencias/azure'
out.mkdir(parents=True, exist_ok=True)
for number, query in enumerate(queries, 1):
    if not query.strip():
        continue
    result = subprocess.run(['az', 'rest', '--method', 'post', '--url', f'https://api.loganalytics.azure.com/v1/workspaces/{workspace}/query', '--resource', 'https://api.loganalytics.io', '--body', json.dumps({'query': query}), '-o', 'json'], capture_output=True, text=True)
    if result.returncode:
        print(result.stderr)
        raise SystemExit(result.returncode)
    data = json.loads(result.stdout)
    (out / f'05-consulta-{number}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f'Consulta {number}: {sum(len(t["rows"]) for t in data["tables"])} filas reales guardadas.')
