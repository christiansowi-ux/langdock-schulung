from pathlib import Path
import json,hashlib,tarfile,subprocess,shutil,time,sys
root=Path('/opt/stacks/langdock-hefte')
release=root/'releases/RELEASE_NAME'
public=root/'public'
m=json.loads((release/'release-manifest.json').read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def run(*args):subprocess.run(args,cwd=root,check=True)
assert digest(release/'RELEASE_NAME-public.tar.gz')==m['archiveSha256']
for name,expected in m['server'].items():
 assert digest(root/name)==expected,('Server configuration changed',name)
for row in m['files']:
 dest=(public/row['path']).resolve()
 assert dest.is_relative_to(public.resolve())
 assert digest(dest) in (row['before'],row['after']),('Live file changed',row['path'])
print('Preflight passed: expected files and server configuration.',flush=True)
if '--check' in sys.argv:sys.exit(0)
backup=release/'public-before.tar.gz'
assert not backup.exists(),'Existing backup: inspect before rerunning.'
with tarfile.open(backup,'w:gz') as t:t.add(public,arcname='public')
run('docker','image','tag','langdock-hefte:latest','langdock-hefte:pre-RELEASE_NAME')
stage=release/'context';stage.mkdir();shutil.copytree(public,stage/'public')
for name in ('Dockerfile','server.mjs','package.json','package-lock.json'):
 if (root/name).exists():shutil.copy2(root/name,stage/name)
with tarfile.open(release/'RELEASE_NAME-public.tar.gz') as t:
 for row in m['files']:
  data=t.extractfile(row['path']).read();assert hashlib.sha256(data).hexdigest()==row['after']
  dest=stage/'public'/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
run('docker','build','-t','langdock-hefte:release-RELEASE_NAME',str(stage))
run('docker','image','tag','langdock-hefte:release-RELEASE_NAME','langdock-hefte:latest')
try:
 run('docker','compose','up','-d','--no-build','--no-deps','langdock-hefte')
 healthy=False
 for _ in range(25):
  r=subprocess.run(['docker','exec','langdock-hefte','node','-e',"fetch('http://127.0.0.1:8080/hefte/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"],capture_output=True)
  if r.returncode==0:healthy=True;break
  time.sleep(2)
 assert healthy,'New release failed healthcheck'
except Exception:
 run('docker','image','tag','langdock-hefte:pre-RELEASE_NAME','langdock-hefte:latest')
 run('docker','compose','up','-d','--no-build','--no-deps','langdock-hefte')
 print('Previous image restored.',flush=True);raise
for row in m['files']:
 dest=public/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(stage/'public'/row['path'],dest)
for name,expected in m['server'].items():assert digest(root/name)==expected
print('DEPLOY_OK:',len(m['files']),'public files. Backup:',backup,flush=True)
