"""Observed file-backed modules, explicit allowlist, and instrumented real CLI.

This is a replay provenance check, not an OS sandbox or an anti-evasion monitor.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import sysconfig
import types

GATE_EXIT = 86
NUMERICAL_MODULES = (
    'op03_gap_fh', 'gap_n1_grad', '_tmp_fh_paradox', 'tmp_fh_test',
    'tmp_verify_endpoints', 'gap_lib', '_gapn2_symmetry_recon',
    '_gapn2_jacobian_probe', '_gapn2_jacobian_analytic', '_gapn2_hess_verify',
    '_gapn2_hess_sign_and_bigR', '_gapn2_hp_scan', '_gapn2_jacobian_spectral',
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen_sources(base):
    path = base / 'manifest.json'
    if digest(path) != (base / 'manifest.sha256').read_text().split()[0]:
        raise RuntimeError('manifest digest mismatch')
    return json.loads(path.read_text())['package_files']


def runtime_policy(base):
    stdlib = sorted({str(Path(sysconfig.get_path(k)).resolve())
                     for k in ('stdlib', 'platstdlib')})
    packages = {}
    for name in ('numpy', 'scipy'):
        spec = importlib.util.find_spec(name)
        if spec is None or not spec.origin:
            raise RuntimeError('installed package unavailable: ' + name)
        root = Path(spec.origin).resolve().parent
        if root.is_relative_to(base.resolve()) or not any(
                p in root.parts for p in ('site-packages', 'dist-packages')):
            raise RuntimeError('package is not from installed package directory: ' + str(root))
        packages[name] = str(root)
    return dict(stdlib_roots=stdlib, installed_package_roots=packages,
                stdlib_excluded_components=['site-packages', 'dist-packages'],
                fresh_input_root=str(base.resolve()))


def collect_modules():
    # Deliberately no Base/path allowlist filter at observation time.
    return {name: str(Path(module.__file__).resolve())
            for name, module in list(sys.modules.items())
            if getattr(module, '__file__', None)}


def expected_bindings(tree, kind):
    prefix = tree + '/scripts/'
    if kind == 'cli':
        return {'__main__': prefix + 'op03_gap_fh.py',
                'op03_gap_fixed': prefix + 'op03_gap_fixed.py',
                'provenance': 'regression/provenance.py'}
    names = (*NUMERICAL_MODULES,
             'op03_gap_precise' if tree == 'originals' else 'op03_gap_fixed')
    return {**{name: prefix + name + '.py' for name in names},
            '__main__': 'regression/regression.py',
            'backend_probe': 'regression/backend_probe.py',
            'provenance': 'regression/provenance.py'}


def classify(path, base, tree, sources, policy):
    if path.is_relative_to(base):
        rel = path.relative_to(base).as_posix()
        if rel in sources and (rel.startswith(tree + '/scripts/') or
                               rel.startswith('regression/')):
            return 'fresh-input'
        return 'unexpected'
    for root in policy['installed_package_roots'].values():
        if path.is_relative_to(Path(root)):
            return 'installed-package'
    for root in policy['stdlib_roots']:
        if path.is_relative_to(Path(root)) and not any(
                part in path.relative_to(root).parts
                for part in policy['stdlib_excluded_components']):
            return 'standard-library'
    return 'unexpected'


def validate(module_files, base, tree, expected, sources, policy):
    base = base.resolve()
    problems, details = [], {}
    for name, value in sorted(module_files.items()):
        path = Path(value).resolve()
        category = classify(path, base, tree, sources, policy)
        item = dict(path=str(path), category=category)
        if category == 'unexpected':
            problems.append(dict(code='unexpected-module', module=name, path=str(path)))
            # Do not read an arbitrary rejected external file; its real path is evidence.
        else:
            try:
                item['sha256'] = digest(path)
            except OSError as error:
                problems.append(dict(code='unreadable-module', module=name, error=str(error)))
            if category == 'fresh-input':
                rel = path.relative_to(base).as_posix()
                if item.get('sha256') != sources[rel]['sha256']:
                    problems.append(dict(code='source-digest-mismatch', module=name, path=str(path)))
        details[name] = item
    required = {}
    for name, rel in sorted(expected.items()):
        path = str((base / rel).resolve())
        required[name] = dict(path=path, sha256=sources[rel]['sha256'])
        if name not in module_files:
            problems.append(dict(code='missing-required-module', module=name, expected_path=path))
        elif module_files[name] != path:
            problems.append(dict(code='wrong-required-path', module=name,
                                 expected_path=path, actual_path=module_files[name]))
        elif details[name].get('sha256') != sources[rel]['sha256']:
            problems.append(dict(code='required-digest-mismatch', module=name, expected_path=path))
    return dict(accepted=not problems, problems=problems, modules=details, required=required)


def control_arguments(parser):
    parser.add_argument('--control-outside', type=Path)
    parser.add_argument('--control-missing', action='store_true')


def import_control(args, base):
    if args.control_outside is None:
        return None
    path = args.control_outside.resolve()
    # Only the supplied benign fixture in the enclosing author/reviewer package.
    owner = base.parents[1] if base.parent.name == 'work' else base
    if path != (owner / 'control-fixtures' / 'outside_probe.py').resolve() or path.is_relative_to(base):
        raise RuntimeError('outside control must use the enclosing package fixture')
    spec = importlib.util.spec_from_file_location('r7_outside_probe', path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return dict(module=spec.name, path=str(path), sha256=digest(path), token=module.TOKEN)


def report(base, tree, kind, args, imported):
    sources = frozen_sources(base)
    policy = runtime_policy(base)
    removed = None
    if args.control_missing:
        name = 'gap_lib' if kind == 'numerical' else 'op03_gap_fixed'
        module = sys.modules.pop(name)  # Real missing binding, after actual execution.
        removed = dict(module=name, path=str(Path(module.__file__).resolve()),
                       sha256=digest(module.__file__))
    module_files = collect_modules()
    gate = validate(module_files, base, tree, expected_bindings(tree, kind), sources, policy)
    gate.update(module_files=module_files, policy=policy, tree=tree, kind=kind,
                optimize=sys.flags.optimize, pid=os.getpid(),
                controls=dict(imported=imported, removed=removed))
    print('PROVENANCE ' + ('PASS' if gate['accepted'] else 'REFUSED') +
          ' ' + json.dumps(gate['problems']), flush=True)
    return gate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    control_arguments(parser)
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[1]
    output = (base / args.output).resolve()
    if not output.is_relative_to(base):
        raise RuntimeError('output outside fresh run')
    imported = import_control(args, base)
    # Execute every unmodified CLI statement, including its four-point loop,
    # with real __main__, __file__, argv, script path and working directory.
    target = base / 'candidates/scripts/op03_gap_fh.py'
    sys.modules['provenance'] = sys.modules[__name__]
    module = types.ModuleType('__main__')
    module.__file__ = str(target)
    module.__package__ = None
    sys.modules['__main__'] = module
    sys.argv = [str(target)]
    sys.path.insert(0, str(target.parent))
    os.chdir(target.parent.parent)
    exec(compile(target.read_bytes(), str(target), 'exec'), module.__dict__)
    gate = report(base, 'candidates', 'cli', args, imported)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(gate, indent=2) + '\n')
    return 0 if gate['accepted'] else GATE_EXIT


if __name__ == '__main__':
    sys.exit(main())
