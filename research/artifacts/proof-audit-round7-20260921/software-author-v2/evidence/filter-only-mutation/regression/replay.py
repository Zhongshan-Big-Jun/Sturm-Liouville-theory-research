"""Portable, bounded replay with observed provenance and real negative controls."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

import provenance
import verify_package

Base = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='')
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    if verify_package.main():
        return 1
    sources = provenance.frozen_sources(Base)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run = Base / 'work' / ('replay-' + stamp + '-' + uuid.uuid4().hex[:6])
    run.mkdir(parents=True)
    source_hashes = {}
    for rel in (*sources, 'manifest.json', 'manifest.sha256'):
        path = Path(rel)
        if path.is_absolute() or '..' in path.parts or not (Base / rel).resolve().is_relative_to(Base):
            raise RuntimeError('unsafe manifest path: ' + rel)
        target = run / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Base / rel, target)
        source_hashes[rel] = digest(target)
    for folder in ('results', 'receipts', 'work'):
        (run / folder).mkdir(exist_ok=True)
    (run / 'copy-manifest.json').write_text(json.dumps(source_hashes, indent=2) + '\n')
    compiled = sorted((run / 'originals').rglob('*.py')) + sorted((run / 'candidates').rglob('*.py'))
    for path in compiled:
        compile(path.read_bytes(), str(path), 'exec')
    environment = os.environ.copy()
    environment.update(PYTHONDONTWRITEBYTECODE='1', OMP_NUM_THREADS='1',
                       OPENBLAS_NUM_THREADS='1', TMPDIR=str(run / 'work'), PYTHONUTF8='1')
    # Installed NumPy/SciPy remain discoverable through normal site configuration.
    # Any inherited Python path is recorded below, not treated as an allowed root.
    policy = provenance.runtime_policy(run)
    fixture = Base / 'control-fixtures/outside_probe.py'
    results = []
    print('Replay directory: ' + str(run), flush=True)
    for mode in ('normal', 'optimized'):
        flags = ['-B'] + (['-O'] if mode == 'optimized' else [])
        cases = [] if args.controls_only else [
            ('originals', 'numerical', None), ('candidates', 'numerical', None),
            ('candidates', 'cli', None)]
        cases += [('candidates', kind, control) for control in ('outside', 'missing')
                  for kind in ('numerical', 'cli')]
        for tree, kind, control in cases:
            name = ('op03-cli' if kind == 'cli' else tree) + '-' + mode
            if control:
                name += '-' + control
            output = 'results/' + name + '.json'
            entry = 'provenance.py' if kind == 'cli' else 'regression.py'
            child = [sys.executable, *flags, str(run / 'regression' / entry), '--output', output]
            if kind == 'numerical':
                child += ['--tree', tree]
            if control == 'outside':
                child += ['--control-outside', str(fixture)]
            elif control == 'missing':
                child += ['--control-missing']
            argv = [sys.executable, '-B', str(run / 'regression/capture_run.py'),
                    '--name', name, '--timeout', '180', '--', *child]
            start = time.monotonic()
            proc = subprocess.run(argv, cwd=run, env=environment, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, timeout=200)
            (run / 'receipts' / (name + '-launcher.stdout')).write_bytes(proc.stdout)
            (run / 'receipts' / (name + '-launcher.stderr')).write_bytes(proc.stderr)
            expected_exit = provenance.GATE_EXIT if control else (1 if tree == 'originals' else 0)
            row = dict(name=name, argv=argv, exit_code=proc.returncode,
                       expected_exit=expected_exit, seconds=time.monotonic() - start, accepted=False)
            try:
                data = json.loads((run / output).read_text())
                gate = data['provenance'] if kind == 'numerical' else data
                # Re-evaluate all reported bindings; do not trust the child's PASS flag.
                checked = provenance.validate(gate['module_files'], run, tree,
                    provenance.expected_bindings(tree, kind), sources, policy)
                passed = (proc.returncode == expected_exit and
                          gate['optimize'] == int(mode == 'optimized') and
                          gate['policy'] == policy and
                          gate['problems'] == checked['problems'] and
                          gate['accepted'] == checked['accepted'])
                if kind == 'numerical':
                    passed = (passed and data['tests'] == 117 and
                              data['failed'] == (79 if tree == 'originals' else 0) and
                              not any(r['name'].endswith('/exception') for r in data['checks']))
                    row.update(tests=data['tests'], passed_checks=data['passed'], failed_checks=data['failed'])
                else:
                    stdout = (run / 'receipts' / name / 'stdout.txt').read_text()
                    pairs = [(float(a), float(b)) for a, b in re.findall(
                        r'dD/du_num=([+\-0-9.e]+)\s+2\(1-R\)f=([+\-0-9.e]+)', stdout)]
                    passed = passed and len(pairs) == 4 and all(
                        abs(a - b) <= max(.002, abs(a) * 2e-4) for a, b in pairs)
                    row['pairs'] = pairs
                if control == 'outside':
                    imported = gate['controls']['imported']
                    passed = (passed and not checked['accepted'] and
                              gate['module_files'].get('r7_outside_probe') == str(fixture) and
                              imported['sha256'] == digest(fixture) and
                              imported['token'] == 'R7-SW-001 real outside import executed' and
                              checked['problems'] == [dict(code='unexpected-module',
                                  module='r7_outside_probe', path=str(fixture))])
                elif control == 'missing':
                    missing = 'gap_lib' if kind == 'numerical' else 'op03_gap_fixed'
                    rel = 'candidates/scripts/' + missing + '.py'
                    passed = (passed and not checked['accepted'] and
                              missing not in gate['module_files'] and
                              gate['controls']['removed'] == dict(module=missing,
                                  path=str(run / rel), sha256=sources[rel]['sha256']) and
                              checked['problems'] == [dict(code='missing-required-module',
                                  module=missing, expected_path=str(run / rel))])
                else:
                    passed = passed and checked['accepted']
                row.update(accepted=bool(passed), provenance_accepted=checked['accepted'],
                           provenance_problems=checked['problems'], pid=gate['pid'])
            except Exception as error:
                row['evidence_error'] = repr(error)
            results.append(row)
            print(json.dumps(row), flush=True)
    final_hashes = {rel: digest(run / rel) for rel in source_hashes}
    names_agree = None
    if not args.controls_only:
        normal = json.loads((run / 'results/candidates-normal.json').read_text())
        optimized = json.loads((run / 'results/candidates-optimized.json').read_text())
        names_agree = [r['name'] for r in normal['checks']] == [r['name'] for r in optimized['checks']]
    summary = dict(role='software repair author; independent review pending', label=args.label,
                   root=str(run), python=sys.executable, optimize=sys.flags.optimize,
                   controls_only=args.controls_only, runs=results,
                   compiled_python_files=len(compiled), runtime_policy=policy,
                   inherited_pythonpath=environment.get('PYTHONPATH'),
                   input_sha256_before=source_hashes, input_sha256_after=final_hashes,
                   inputs_unchanged=final_hashes == source_hashes,
                   outside_fixture=dict(path=str(fixture), sha256=digest(fixture)),
                   normal_optimized_names_agree=names_agree,
                   accepted=all(r['accepted'] for r in results) and
                            final_hashes == source_hashes and names_agree is not False)
    summary['output_sha256'] = {p.relative_to(run).as_posix(): digest(p)
        for folder in ('results', 'receipts') for p in sorted((run / folder).rglob('*')) if p.is_file()}
    (run / 'replay-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('AUTHOR REPLAY ' + ('PASS' if summary['accepted'] else 'FAIL') +
          ' ' + str(run / 'replay-summary.json'), flush=True)
    return int(not summary['accepted'])


if __name__ == '__main__':
    sys.exit(main())
