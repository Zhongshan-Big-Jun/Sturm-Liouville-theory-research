from pathlib import Path
import ast, datetime, hashlib, json, os, shutil, subprocess, sys, time

ROOT = Path(__file__).resolve().parent
FROZEN = ROOT / 'frozen'
RUNS = ROOT / 'fresh_runs'
RUNS.mkdir(exist_ok=True)
ERRORS = {
 'wrong-g-right': 'ArithmeticError: G upper endpoint must have strictly negative G',
 'old-upper-endpoint': 'ArithmeticError: Root upper endpoint must have strictly positive F',
 'wrong-u-enclosure': 'ArithmeticError: wrong-u-enclosure: proposed enclosure does not contain certified enclosure',
 'wrong-value-enclosure': 'ArithmeticError: wrong-value-enclosure: proposed enclosure does not contain certified enclosure',
 'unsafe-cot-enclosure': 'ArithmeticError: unsafe-cot-enclosure: proposed enclosure does not contain certified enclosure',
 'binary-pi-enclosure': 'ArithmeticError: binary-pi-enclosure: proposed enclosure does not contain certified enclosure',
 'wrong-sqrt-enclosure': 'ArithmeticError: Invalid sqrt(2) enclosure',
 'omitted-taylor-remainder': 'ArithmeticError: omitted-taylor-remainder: proposed enclosure does not contain certified enclosure',
 'zero-divisor': 'ArithmeticError: Divisor interval contains zero',
 'reversed-interval': 'ArithmeticError: Reversed interval',
 'float-input': 'TypeError: Only exact int or Fraction inputs are accepted',
 'invalid-taylor-degree': 'ArithmeticError: Taylor degree must be a positive integer',
 'invalid-atan-domain': 'ArithmeticError: Arctan series requires 0 < x < 1',
 'wrong-ratio-bound': 'ArithmeticError: Proposed scalar upper bound 0.825 is not certified',
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(label, flags, target, extras, input_files, expected=0, message=None):
    folder = RUNS / label
    folder.mkdir(exist_ok=False)
    sources = {'trace_execution.py': FROZEN / 'trace_execution.py', **input_files}
    for name, origin in sources.items(): shutil.copyfile(origin, folder / name)
    input_hashes = {name: sha(folder / name) for name in sources}
    input_hashes['reviewer_runner.py'] = sha(Path(__file__))
    command = [sys.executable, '-B', *flags, 'trace_execution.py', 'imports.json', target, *extras]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    started, clock = now(), time.monotonic()
    timeout = False
    try:
        p = subprocess.run(command, cwd=folder, env=env, capture_output=True, timeout=55)
        out, err, code = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out, err, code, timeout = e.stdout or b'', e.stderr or b'', None, True
    (folder/'stdout.txt').write_bytes(out); (folder/'stderr.txt').write_bytes(err)
    matches = code == expected and (message is None or message in err.decode(errors='replace'))
    record = {'label': label, 'argv': command, 'cwd': str(folder), 'started_utc': started,
              'finished_utc': now(), 'seconds': time.monotonic()-clock, 'exit_code': code,
              'timed_out': timeout, 'expected_exit_code': expected, 'required_error': message,
              'expectation_matched': matches, 'source_sha256': input_hashes,
              'files_sha256': {f.name: sha(f) for f in folder.iterdir() if f.is_file()},
              'environment_override': {'PYTHONDONTWRITEBYTECODE':'1'},
              'scope': 'Fresh private copies and working directory; real subprocess; -S only where argv says so. No OS sandbox or complete import isolation claimed.'}
    (folder/'receipt.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps({'run':label, 'exit':code,'expected':matches,'seconds':round(record['seconds'],3)}),flush=True)
    return record

def main():
    records=[]
    if sys.argv[1] == 'core':
        for label, flags in [('normal',[]),('optimized',['-O'])]:
            records.append(run('supplied-'+label,flags,'checks.py',['results.json'],{'checks.py':FROZEN/'inputs/submitted/checks.py'}))
        tree = ast.parse((FROZEN/'certificate.py').read_text())
        controls = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NegativeControls' for t in n.targets))
        if set(controls) != set(ERRORS):raise RuntimeError('Negative-control inventory mismatch')
        for label, flags in [('normal',[]),('optimized',['-O']),('no-site',['-S']),('optimized-no-site',['-O','-S'])]:
            records.append(run('certificate-'+label,flags,'certificate.py',['--output','results.json'],{'certificate.py':FROZEN/'certificate.py'}))
            for name in controls:
                records.append(run('negative-'+name+'-'+label, flags, 'certificate.py', ['--negative',name], {'certificate.py':FROZEN/'certificate.py'}, 1, ERRORS[name]))
        records.append(run('legacy-platform',[],'legacy_diagnostics.py',['observations.json'],{'legacy_diagnostics.py':FROZEN/'legacy_diagnostics.py','checks.py':FROZEN/'inputs/submitted/checks.py'}))
    elif sys.argv[1]=='edges':
        for label, flags in [('no-site',['-S']),('optimized-no-site',['-O','-S'])]:
            records.append(run('reviewer-edges-'+label,flags,'reviewer_edges.py',['results.json'],{'reviewer_edges.py':ROOT/'reviewer_edges.py','certificate.py':FROZEN/'certificate.py','author_results.json':FROZEN/'results.json'}))
    elif sys.argv[1]=='symbolic':
        records.append(run('reviewer-symbolic',[],'reviewer_symbolic.py',['results.json'],{'reviewer_symbolic.py':ROOT/'reviewer_symbolic.py'}))
    else: raise ValueError('Unknown review stage')
    (ROOT/('fresh-'+sys.argv[1]+'-summary.json')).write_text(json.dumps(records,indent=2)+'\n')
    if not all(r['expectation_matched'] for r in records):sys.exit(1)

if __name__=='__main__': main()
