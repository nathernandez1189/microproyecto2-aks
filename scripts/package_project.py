"""Export only reviewed, Git-tracked project files plus an integrity manifest.

Run after committing the delivery. Untracked files and private runtime data are
never discovered recursively. A dirty tracked file aborts export so the archive
corresponds to the recorded source rather than silently mixing versions.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BLOCKED = {'.git', '.azure', '.kube', '.tools', '.venv', '__pycache__',
           'build', 'output', 'tmp', 'privadas'}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def main():
    revision = git('rev-parse', 'HEAD').decode().strip()
    if git('status', '--porcelain', '--untracked-files=no').strip():
        raise SystemExit('Hay cambios sin commit. Revisa y registra los archivos antes de exportar.')
    names = [n.decode() for n in git('ls-files', '-z').split(b'\0') if n]
    if not names:
        raise SystemExit('No hay archivos registrados para exportar.')
    files = []
    for name in names:
        relative = Path(name)
        path = ROOT / relative
        blocked = (any(part in BLOCKED for part in relative.parts)
                   or (path.name.startswith('.env') and path.name != '.env.example')
                   or path.suffix.lower() in {'.pem', '.key', '.pyc'}
                   or any(x in path.name.lower() for x in ('.db', '.sqlite'))
                   or path.name == 'tareas-respaldo.json')
        if relative.parts[0] == 'evidencias':
            blocked |= name != 'evidencias/README.md' and relative.parts[:2] != ('evidencias', 'publicables')
        if blocked or path.is_symlink() or not path.is_file():
            raise SystemExit(f'Archivo no apto para exportación: {name}')
        files.append((name, path.read_bytes()))
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    target = output / 'Microproyecto2-AKS-Equipo.zip'
    manifest = {'git_commit': revision, 'files': {
        name: hashlib.sha256(data).hexdigest() for name, data in files}}
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files:
            archive.writestr(f'{ROOT.name}/{name}', data)
        archive.writestr(f'{ROOT.name}/MANIFIESTO-SHA256.json',
                         json.dumps(manifest, indent=2, ensure_ascii=False))
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise SystemExit('Falló la comprobación de integridad del ZIP.')
    print(f'{target}\n{len(files)} archivos; commit {revision}; ZIP verificado.')


if __name__ == '__main__':
    main()
