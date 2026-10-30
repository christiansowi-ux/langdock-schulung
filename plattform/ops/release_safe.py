"""Sichere Teil-Veröffentlichung der Lernplattform (Ablauf wie in UEBERGABE.md seit 26.10.2026).

python -X utf8 ops/release_safe.py <release-name> [--only REGEX] [--dry]

1. Liest Hashes aller Live-Dateien (nur Stack /opt/stacks/langdock-hefte) und vergleicht mit plattform/public.
2. Nimmt neue + geänderte Dateien; alte Modul-1-Tagesseiten, die sich nur im Aufgaben-Cachetoken
   unterscheiden, bleiben unverändert live (keine Scheinänderung).
3. Packt Archiv + Manifest, prüft auf dem Server (--check), sichert public/ und das Image,
   baut das neue Image, Healthcheck, kopiert Dateien, prüft danach per HTTPS bytegenau.
Dateien, die nur live existieren, werden nie gelöscht.
"""
import concurrent.futures
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
from pathlib import Path

HOST = 'root@212.227.85.113'
STACK = '/opt/stacks/langdock-hefte'
PUB = Path(__file__).resolve().parents[1] / 'public'
WORK = Path(__file__).resolve().parents[2] / '_quellen/build/releases'
SSH = ['ssh', '-o', 'BatchMode=yes', HOST]
DEPLOY = Path(__file__).resolve().parent / 'deploy_remote_template.py'

LIVE = """from pathlib import Path
import json,hashlib,subprocess
r=Path('/opt/stacks/langdock-hefte');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads(subprocess.check_output(['docker','inspect','--format','{{json .State}}','langdock-hefte'],text=True))
print(json.dumps(dict(files={p.relative_to(r/'public').as_posix():h(p) for p in (r/'public').rglob('*') if p.is_file()},server={n:h(r/n) for n in ['server.mjs','Dockerfile','docker-compose.yml','package.json','package-lock.json']},status=s['Status'],health=s['Health']['Status'])))
"""


def digest(b):
    return hashlib.sha256(b).hexdigest()


def norm(x):
    return re.sub(r'\s+', ' ', re.sub(r'(/hefte/assets/aufgaben\.json)\?v=[^"\s]+', r'\1', x)).strip()


def main():
    name = sys.argv[1]
    only = re.compile(sys.argv[sys.argv.index('--only') + 1]) if '--only' in sys.argv else None
    dry = '--dry' in sys.argv
    work = WORK / name
    work.mkdir(parents=True, exist_ok=True)
    live = json.loads(subprocess.run(SSH + ['python3 -'], input=LIVE, text=True, capture_output=True, check=True).stdout)
    assert live['status'] == 'running' and live['health'] == 'healthy', live
    (work / 'live-before.json').write_text(json.dumps(live), encoding='utf8')
    local = {p.relative_to(PUB).as_posix(): p for p in PUB.rglob('*') if p.is_file()}
    cand = [k for k, p in sorted(local.items()) if live['files'].get(k) != digest(p.read_bytes()) and (not only or only.search(k))]
    olds = [k for k in cand if re.fullmatch(r'(ingo|carmen|tabea)/tag-(\d+)/index\.html', k) and k in live['files']]
    token_only = []
    if olds:
        tgz = subprocess.run(SSH + [f'cd {STACK}/public && tar czf - ' + ' '.join(olds)], capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tgz)) as t:
            for k in olds:
                if norm(t.extractfile(k).read().decode('utf8')) == norm(local[k].read_text(encoding='utf8')):
                    token_only.append(k)
    rows = [dict(path=k, before=live['files'].get(k), after=digest(local[k].read_bytes()), bytes=local[k].stat().st_size)
            for k in cand if k not in token_only]
    print(f'{len(rows)} Dateien ({sum(1 for r in rows if not r["before"])} neu), {len(token_only)} nur Cachetoken – bleiben live unverändert')
    if dry:
        for r in rows[:400]:
            print('  ', 'NEU ' if not r['before'] else 'ÄND ', r['path'])
        return
    arc = work / f'{name}-public.tar.gz'
    with tarfile.open(arc, 'w:gz') as z:
        for r in rows:
            z.add(local[r['path']], arcname=r['path'])
    m = dict(release=name, status='prepared', files=rows, server=live['server'], archiveSha256=digest(arc.read_bytes()), unchangedTokenPages=len(token_only))
    (work / 'release-manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf8')
    (work / 'deploy_remote.py').write_text(DEPLOY.read_text(encoding='utf8').replace('RELEASE_NAME', name), encoding='utf8')
    remote = f'{STACK}/releases/{name}'
    subprocess.run(SSH + [f'test ! -e {remote} && mkdir -p {remote}'], check=True)
    subprocess.run(['scp', '-q', '-o', 'BatchMode=yes', str(arc), str(work / 'release-manifest.json'), str(work / 'deploy_remote.py'), f'{HOST}:{remote}/'], check=True)
    subprocess.run(SSH + [f'python3 {remote}/deploy_remote.py --check'], check=True)
    with (work / 'deploy.log').open('w', encoding='utf8') as f:
        subprocess.run(SSH + [f'python3 {remote}/deploy_remote.py'], stdout=f, stderr=subprocess.STDOUT, check=True)

    verify(name, rows, live, work, remote, m)


def verify(name, rows, live, work, remote, m):
    import time

    def check(r):
        if r['path'] == 'manifest.json':
            return dict(path=r['path'], internal=True)
        url = 'https://quint-games.de/hefte/' + urllib.parse.quote(r['path']) + '?verify=' + name
        for attempt in range(6):  # direkt nach dem Container-Neustart kann kurz der alte Stand antworten
            with urllib.request.urlopen(urllib.request.Request(url, headers={'Cache-Control': 'no-cache'}), timeout=60) as resp:
                ok = digest(resp.read()) == r['after']
                if ok or attempt == 5:
                    return dict(path=r['path'], status=resp.status, match=ok)
            time.sleep(3)
    time.sleep(4)
    with concurrent.futures.ThreadPoolExecutor(8) as ex:
        res = list(ex.map(check, rows))
    (work / 'live-verification.json').write_text(json.dumps(res, indent=1), encoding='utf8')
    bad = [r for r in res if not r.get('match', r.get('internal'))]
    assert not bad, bad[:5]
    after = dict(live['files']); after.update({r['path']: r['after'] for r in rows})
    host = json.loads(subprocess.run(SSH + ['python3 -'], input=LIVE, text=True, capture_output=True, check=True).stdout)
    assert host['files'] == after and host['server'] == live['server'] and host['health'] == 'healthy', 'Unerwartete Abweichung auf dem Server'
    m['status'] = 'deployed-verified'
    (work / 'release-manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding='utf8')
    subprocess.run(['scp', '-q', '-o', 'BatchMode=yes', str(work / 'release-manifest.json'), str(work / 'live-verification.json'), str(work / 'deploy.log'), f'{HOST}:{remote}/'], check=True)
    print(f'LIVE OK: {len(rows)} Dateien per HTTPS bytegenau, alle {len(after)} Host-Dateien wie erwartet, Container gesund, Server unverändert.')


def verify_only(name):
    work = WORK / name
    m = json.loads((work / 'release-manifest.json').read_text(encoding='utf8'))
    live = json.loads((work / 'live-before.json').read_text(encoding='utf8'))
    verify(name, m['files'], live, work, f'{STACK}/releases/{name}', m)


if __name__ == '__main__':
    verify_only(sys.argv[1]) if '--verify-only' in sys.argv else main()
