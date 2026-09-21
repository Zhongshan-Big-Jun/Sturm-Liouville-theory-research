from pathlib import Path
import concurrent.futures, datetime, difflib, hashlib, json, os, subprocess, sys, time, traceback

OUT = Path('/mnt/f/tools/math-audit-round5-20260921/independent-lean-replay')
PACKET = Path('/mnt/f/LaTeX/BVE research/research/library/reviews/packets/98b6920270e96b30b58dd75e49271e97ed00e0a8ea60e116f88c17dba9dd8140/packet.json')
BASE = 'research/artifacts/proof-audit-round5-20260921/lean/'
SOURCE_HASH = '035043c154c215e995a210b798f80cf131414eee5529ad54396a5af3d669ae45'
ROOT_NAME = 'SL.AuditRound5.local_algebra_root'

def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write_json(path, value):
    path = Path(path)
    assert path.is_relative_to(OUT)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def packet():
    assert sha(PACKET) == PACKET.parent.name
    return json.loads(PACKET.read_bytes())

def frozen(name):
    item = packet()['inputs'][name]
    p = PACKET.parent / item['snapshot']
    assert sha(p) == item['sha256'], str(p)
    return p

def flean(name):
    return frozen(BASE + name)

def copy_snapshot(name, target):
    src = frozen(name)
    target = OUT / target
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as f:
        f.write(src.read_bytes())
    assert sha(src) == sha(target)
    return {'input': name, 'snapshot': str(src), 'copy': str(target), 'sha256': sha(target)}

def win(p):
    s = str(p)
    assert s.startswith('/mnt/') and s[6] == '/'
    return s[5].upper() + ':\\' + s[7:].replace('/', '\\')

def setup():
    copies = []
    copies.append(copy_snapshot('lean-proof/SL/AuditRound5.lean', 'SL/AuditRound5.lean'))
    assert sha(OUT / 'SL/AuditRound5.lean') == SOURCE_HASH
    for n in ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']:
        copies.append(copy_snapshot(BASE + 'pins/' + n, n))
    for n in ['environment.json', 'final/module-artifact-hashes.json', 'final/declarations.json',
              'final/loaded-modules.json', 'final/formal-statements.txt',
              'final/formal-statements-fully-explicit.txt', 'final/local-definition-closure.txt',
              'final/public-theorem-axioms.json', 'positive-contract.json',
              'coordinator-replay/final/declarations.json', 'coordinator-replay/final/loaded-modules.json',
              'InspectAuditRound5.lean']:
        copies.append(copy_snapshot(BASE + n, 'frozen/' + n))
    for n in ['PositiveControls.lean', 'FalseHighSpanEquality.lean']:
        copies.append(copy_snapshot(BASE + 'controls/' + n, n))
    copies.append(copy_snapshot(BASE + 'coordinator-replay/ContractCheck.lean', 'ContractCheck.lean'))
    old = (OUT / 'frozen/InspectAuditRound5.lean').read_bytes()
    literal = b'F:/tools/math-audit-round5-20260921/lean-author/final/'
    replacement = b'F:/tools/math-audit-round5-20260921/independent-lean-replay/final/'
    assert old.count(literal) == 1
    new = old.replace(literal, replacement)
    with (OUT / 'InspectAuditRound5.lean').open('xb') as f:
        f.write(new)
    diff = ''.join(difflib.unified_diff(old.decode().splitlines(True), new.decode().splitlines(True),
                                     fromfile='frozen/InspectAuditRound5.lean',
                                     tofile='InspectAuditRound5.lean'))
    (OUT / 'export-helper.diff').write_text(diff)
    for d in ['build/SL', 'final', 'tmp', 'logs', 'checks']:
        (OUT / d).mkdir(parents=True, exist_ok=True)
    write_json(OUT / 'input-bindings.json', {'copies': copies,
        'exporter_change': {'old_sha256': hashlib.sha256(old).hexdigest(),
                           'new_sha256': hashlib.sha256(new).hexdigest(),
                           'old_literal': literal.decode(), 'new_literal': replacement.decode(),
                           'replacement_count': 1, 'only_output_folder_changed': new.replace(replacement, literal) == old}})
    print('Prepared byte-identical source, pins and controls; changed only exporter output literal.', flush=True)

def hash_one(row):
    p = Path(row['path'])
    st = p.stat()
    actual = sha(p)
    after = p.stat()
    stable = (st.st_size, st.st_mtime_ns, st.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns)
    return {'path': str(p), 'expected_sha256': row['sha256'], 'actual_sha256': actual,
            'expected_bytes': row.get('bytes'), 'actual_bytes': after.st_size,
            'match': actual == row['sha256'] and (row.get('bytes') is None or row['bytes'] == after.st_size),
            'stable_during_read': stable, 'mtime_ns': after.st_mtime_ns, 'ctime_ns': after.st_ctime_ns}

def rehash(stage):
    env = json.loads((OUT / 'frozen/environment.json').read_bytes())
    manifest = json.loads((OUT / 'frozen/final/module-artifact-hashes.json').read_bytes())
    rows = [r for m in manifest['modules'] for r in m['artifacts']]
    assert len(rows) == manifest['artifact_count']
    assert len({r['path'] for r in rows}) == len(rows)
    start = time.monotonic()
    result = {'utc_start': now(), 'native_agent_id': os.environ.get('CODEX_THREAD_ID'),
              'scope': 'Fresh byte hashes of every runtime and module artifact declared in frozen manifests; original local root hashed but excluded from execution lookup.',
              'manifest_sha256': sha(OUT / 'frozen/final/module-artifact-hashes.json')}
    result['runtime'] = [hash_one(r) for r in env['runtime_files']]
    assert all(r['match'] and r['stable_during_read'] for r in result['runtime']), 'Runtime mismatch'
    checked = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for i, v in enumerate(pool.map(hash_one, rows), 1):
            checked.append(v)
            if i % 3000 == 0:
                print(stage, 'hashed', i, '/', len(rows), flush=True)
    result['artifacts'] = checked
    result['module_count'] = len(manifest['modules'])
    result['artifact_count'] = len(checked)
    result['bytes'] = sum(r['actual_bytes'] for r in checked)
    result['all_match'] = all(r['match'] and r['stable_during_read'] for r in checked + result['runtime'])
    result['utc_end'] = now()
    result['duration_seconds'] = time.monotonic() - start
    write_json(OUT / ('artifact-rehash-' + stage + '.json'), result)
    assert result['all_match'], 'Artifact identity mismatch; stopping before execution'
    print(json.dumps({'stage': stage, 'runtime_files': len(result['runtime']), 'modules': result['module_count'],
                      'artifacts': len(checked), 'bytes': result['bytes'], 'all_match': result['all_match'],
                      'seconds': round(result['duration_seconds'], 2)}), flush=True)
    return result

def effective_env():
    original = json.loads((OUT / 'frozen/environment.json').read_bytes())
    parts = original['LEAN_PATH'].split(';')
    assert len(parts) == 10
    assert 'lean-author' in parts[0]
    assert all('\\.lake\\packages\\' in p and p.endswith('\\.lake\\build\\lib\\lean') for p in parts[1:])
    e = os.environ.copy()
    e['LEAN_PATH'] = ';'.join([win(OUT / 'build')] + parts[1:])
    e['WSLENV'] = ':'.join([p for p in e.get('WSLENV', '').split(':')
                            if p and p.split('/')[0] not in ['LEAN_PATH', 'TMP', 'TEMP']] + ['LEAN_PATH', 'TMP', 'TEMP'])
    e['TMP'] = win(OUT / 'tmp')
    e['TEMP'] = win(OUT / 'tmp')
    e['TMPDIR'] = str(OUT / 'tmp')
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    return e

def file_bindings(paths):
    return {str(p): sha(p) for p in dict.fromkeys(paths)}

def run_lean(name, options, source=None, expect=0, output=None):
    log = OUT / 'logs' / name
    assert not log.with_suffix('.json').exists(), 'Refusing receipt overwrite'
    verification = json.loads((OUT / 'artifact-rehash-before.json').read_bytes())
    assert verification['all_match']
    manifest = json.loads((OUT / 'frozen/environment.json').read_bytes())
    lean = Path(manifest['compiler'])
    assert str(lean) == '/mnt/f/DevCache/elan/toolchains/leanprover--lean4---v4.31.0/bin/lean.exe'
    declared = {r['path']: r['sha256'] for r in manifest['runtime_files']}
    assert sha(lean) == declared[str(lean)]
    root = OUT / 'build/SL/AuditRound5.olean'
    paths = [OUT / n for n in ['SL/AuditRound5.lean', 'lean-toolchain', 'lakefile.lean', 'lake-manifest.json']]
    if source:
        paths.append(OUT / source)
    if root.exists():
        paths.append(root)
    args = [str(lean)] + options + ([win(OUT / source)] if source else [])
    env = effective_env()
    receipt = {'argv': args, 'cwd': str(OUT), 'cwd_windows': win(OUT),
               'native_agent_id': os.environ.get('CODEX_THREAD_ID'), 'utc_start': now(),
               'source_sha256_before': file_bindings(paths), 'compiler_sha256': sha(lean),
               'runner_sha256': sha(__file__), 'LEAN_PATH': env['LEAN_PATH'], 'WSLENV': env['WSLENV'],
               'temporary_directories': {k: env[k] for k in ['TMP', 'TEMP', 'TMPDIR']},
               'expected_exit_code': expect, 'root_preexists': root.exists()}
    if output:
        assert not (OUT / output).exists(), 'Output must be fresh'
    write_json(log.with_suffix('.json'), receipt)
    t = time.monotonic()
    with log.with_suffix('.stdout.txt').open('xb') as stdout, log.with_suffix('.stderr.txt').open('xb') as stderr:
        proc = subprocess.Popen(args, cwd=OUT, env=env, stdout=stdout, stderr=stderr)
        receipt['pid'] = proc.pid
        write_json(log.with_suffix('.json'), receipt)
        code = proc.wait()
    receipt.update(exit_code=code, duration_seconds=time.monotonic()-t, utc_end=now(),
                   source_sha256_after=file_bindings(paths))
    receipt['all_inputs_unchanged'] = receipt['source_sha256_before'] == receipt['source_sha256_after']
    for stream in ['stdout', 'stderr']:
        receipt[stream + '_sha256'] = sha(log.with_suffix('.' + stream + '.txt'))
        receipt[stream + '_bytes'] = log.with_suffix('.' + stream + '.txt').stat().st_size
    if root.exists():
        receipt['root_object'] = {'path': str(root), 'sha256': sha(root), 'bytes': root.stat().st_size}
    if output and (OUT / output).exists():
        receipt['output_artifact'] = {'path': str(OUT / output), 'sha256': sha(OUT / output),
                                      'bytes': (OUT / output).stat().st_size}
    receipt['expected_exit_matched'] = code == expect
    write_json(log.with_suffix('.json'), receipt)
    print(name, 'exit', code, 'expected', expect, 'seconds', round(receipt['duration_seconds'], 2), flush=True)
    if name.endswith('version') or code != 0 or name.endswith('compile'):
        print(log.with_suffix('.stdout.txt').read_text(errors='replace'), end='', flush=True)
        print(log.with_suffix('.stderr.txt').read_text(errors='replace'), end='', flush=True)
    assert receipt['all_inputs_unchanged'], name + ': input changed'
    assert code == expect, name + ': unexpected exit'
    return receipt

def execute():
    run_lean('01-version', ['--version'])
    run_lean('02-root-compile', ['--root=' + win(OUT), '-o', win(OUT/'build/SL/AuditRound5.olean')],
             'SL/AuditRound5.lean', output='build/SL/AuditRound5.olean')
    run_lean('03-import-resolution-before', ['--deps'], 'InspectAuditRound5.lean')
    run_lean('04-export', [], 'InspectAuditRound5.lean')
    run_lean('05-positive-controls', ['--root=' + win(OUT), '-o', win(OUT/'build/PositiveControls.olean')],
             'PositiveControls.lean', output='build/PositiveControls.olean')
    run_lean('06-false-high-span-equality', [], 'FalseHighSpanEquality.lean', expect=1)
    run_lean('07-exact-root-contract', ['--root=' + win(OUT), '-o', win(OUT/'build/ContractCheck.olean')],
             'ContractCheck.lean', output='build/ContractCheck.olean')
    run_lean('08-import-resolution-after', ['--deps'], 'InspectAuditRound5.lean')

if __name__ == '__main__':
    try:
        stage = sys.argv[1]
        if stage == 'setup': setup()
        elif stage in ['before', 'after']: rehash(stage)
        elif stage == 'execute': execute()
        else: raise ValueError(stage)
    except BaseException:
        traceback.print_exc()
        raise

