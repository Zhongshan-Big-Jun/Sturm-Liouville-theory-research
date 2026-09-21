#!/usr/bin/env python3
"""Independent receipt and byte-identity collector; no supplied helper imported."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, os, shutil, subprocess, sys, time
BASE = Path('/mnt/f/tools/math-audit-round7-20260921/independent-execution')
RUN = Path(__file__).resolve().parent

def digest(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(path, obj):
    path = Path(path)
    if not path.resolve().is_relative_to(BASE):
        raise RuntimeError('write outside execution directory')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def pointer(path):
    p = Path(path).resolve()
    return {'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size}

def host(path):
    if len(path) > 2 and path[1] == ':':
        return Path('/mnt') / path[0].lower() / path[3:].replace('\\', '/')
    return Path(path)

def preflight():
    packet = json.loads((BASE/'PACKET.json').read_text())
    freeze_file = BASE/'lean-package/freeze.json'
    freeze = json.loads(freeze_file.read_text())
    expected = {str(freeze_file): packet['lean_freeze_sha256']}
    expected.update({str(BASE/'lean-package'/p): h for p,h in freeze['files'].items()})
    expected.update({str(BASE/'numerical'/p): h for p,h in packet['numeric_sources'].items()})
    if freeze['external_inputs'] != packet['allowed_external_inputs']:
        raise RuntimeError('packet/freeze external lists disagree')
    expected.update(freeze['external_inputs'])
    rows = []
    for name, sha in expected.items():
        p = Path(name)
        row = {'path': name, 'expected_sha256': sha}
        try:
            row.update(actual_sha256=digest(p), bytes=p.stat().st_size)
            row['match'] = row['actual_sha256'] == sha
        except OSError as e:
            row.update(match=False, error=repr(e))
        rows.append(row)
    config = json.loads((BASE/'lean-package/runtime-config.json').read_text())
    manifest = json.loads((BASE/'lean-package/snapshot/lake-manifest.json').read_text())
    resolved = Path(sys.executable).resolve()
    existing_leanpath = []
    for p in manifest['packages']:
        location = Path(config['original_project'])/'.lake/packages'/p['name']/'.lake/build/lib/lean'
        if location.is_dir():
            existing_leanpath.append(subprocess.check_output(['wslpath','-w',str(location)], cwd=BASE, text=True).strip())
    supplied_path_matches = ';'.join(existing_leanpath) == config['LEAN_PATH']
    mathlib = Path(config['original_project'])/'.lake/packages/mathlib'
    git = subprocess.run(['git','-C',str(mathlib),'rev-parse','HEAD'], cwd=BASE, capture_output=True, text=True, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    for stream in ('stdout','stderr'):
        (RUN/('mathlib-head.'+stream+'.txt')).write_text(getattr(git,stream))
    missing = BASE/'numerical/inputs/manifest.json'
    report = {
        'utc': stamp(), 'packet': pointer(BASE/'PACKET.json'), 'checks':rows,
        'all_declared_hashes_match':all(r['match'] for r in rows),
        'python':{'version':sys.version,'executable':str(resolved),'sha256':digest(resolved), 'matches_frozen_python':str(resolved) in expected and digest(resolved)==expected[str(resolved)]},
        'runtime_leanpath_matches_config': supplied_path_matches,
        'mathlib_head':{'argv':['git','-C',str(mathlib),'rev-parse','HEAD'], 'returncode':git.returncode,'actual':git.stdout.strip(),'expected':config['mathlib_commit'],'match':git.returncode==0 and git.stdout.strip()==config['mathlib_commit'], 'stdout':pointer(RUN/'mathlib-head.stdout.txt'),'stderr':pointer(RUN/'mathlib-head.stderr.txt')},
        'numeric_undeclared_manifest':{'path':str(missing),'exists':missing.exists(),'contents_read':False},
        'replay_destination_existed': (RUN/'replay').exists(),
        'scope':'No author output, README, AGENTS, memory, histories, or manuscript content read. Listed external audit report was hashed only.'
    }
    save(RUN/'preflight.json',report)
    print(json.dumps({k:report[k] for k in ('all_declared_hashes_match','runtime_leanpath_matches_config','numeric_undeclared_manifest','replay_destination_existed')},ensure_ascii=False),flush=True)
    print('hash_checks',len(rows),'python_match',report['python']['matches_frozen_python'],'mathlib_head_match',report['mathlib_head']['match'],flush=True)
    if not report['all_declared_hashes_match'] or not supplied_path_matches or not report['python']['matches_frozen_python'] or not report['mathlib_head']['match']:
        return 1
    roots = [host(p) for p in config['LEAN_PATH'].split(';')]
    roots.append(Path(config['lean']).parent.parent/'lib/lean')
    paths=[]
    for root in roots:
        for directory, subdirs, names in os.walk(root):
            subdirs.sort()
            for name in sorted(names):
                if name.endswith(('.olean','.olean.server','.olean.private')):
                    paths.append(Path(directory)/name)
    def record(path):
        before=path.stat()
        h=digest(path)
        after=path.stat()
        return {'path':str(path),'sha256':h,'bytes':after.st_size,'mtime_ns':after.st_mtime_ns,'stable_during_hash':(before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns)}
    start=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        inventory=list(pool.map(record,paths))
    save(RUN/'runtime-before.json',{'utc':stamp(),'roots':list(map(str,roots)),'artifacts':inventory,'hashes_count':len(inventory),'seconds':time.monotonic()-start})
    print('runtime artifacts prehashed',len(inventory),'seconds',round(time.monotonic()-start,2),flush=True)
    return 0 if all(x['stable_during_hash'] for x in inventory) else 1

def run(label, argv):
    logs=RUN/'executor-logs';logs.mkdir(exist_ok=True)
    receipt=logs/(label+'.json')
    if receipt.exists():
        raise RuntimeError('receipt exists; do not overwrite a prior attempt')
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    temp=RUN/'tmp';temp.mkdir(exist_ok=True)
    env['TMPDIR']=str(temp)
    record={'label':label,'argv':argv,'cwd':str(BASE),'started_at_utc':stamp(),'collector':pointer(__file__),'executable':pointer(shutil.which(argv[0]) or argv[0]),'selected_environment':{k:env.get(k) for k in ('PYTHONDONTWRITEBYTECODE','TMPDIR')}}
    save(receipt,record)
    start=time.monotonic()
    with (logs/(label+'.stdout.log')).open('xb') as out, (logs/(label+'.stderr.log')).open('xb') as err:
        process=subprocess.Popen(argv,cwd=BASE,stdout=out,stderr=err,env=env)
        record['pid']=process.pid;save(receipt,record)
        print('started',label,'pid',process.pid,flush=True)
        code=process.wait()
    record.update(returncode=code,ended_at_utc=stamp(),elapsed_seconds=time.monotonic()-start)
    for stream in ('stdout','stderr'):
        record[stream]=pointer(logs/(label+'.'+stream+'.log'))
    save(receipt,record)
    print('finished',label,'exit',code,'seconds',round(record['elapsed_seconds'],2),flush=True)
    return code

if __name__=='__main__':
    if sys.argv[1]=='preflight':
        sys.exit(preflight())
    if sys.argv[1]=='run':
        sys.exit(run(sys.argv[2],sys.argv[3:]))
    raise SystemExit('unknown operation')
