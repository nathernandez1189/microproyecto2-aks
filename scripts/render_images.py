import re
import sys
from pathlib import Path

registry, tag, source, target = sys.argv[1:]
if not re.fullmatch(r'[a-zA-Z0-9.-]+', registry) or not re.fullmatch(r'[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}', tag):
    raise SystemExit('Registro o etiqueta no válidos')
text = Path(source).read_text()
for app in ('classifier', 'planner'):
    old = f'image: mp2-{app}:v1'
    if text.count(old) != 1:
        raise SystemExit(f'Se esperaba exactamente una imagen para {app}')
    text = text.replace(old, f'image: {registry}/mp2-{app}:{tag}')
Path(target).write_text(text)
