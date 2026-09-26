"""Review-owned module-origin recorder; does not change candidate modules."""
import atexit
import hashlib
import json
import os
from pathlib import Path
import sys


def record_origins():
    audit = Path(os.environ['REVIEW_EVIDENCE_ROOT'])
    manifest = json.loads((audit / 'manifest-before.json').read_text())
    expected = {Path(v['copy']).resolve(): v['sha256'] for v in manifest['inputs'].values()}
    known_names = {p.stem for p in expected if p.suffix == '.py'}
    modules = {name: str(Path(module.__file__).resolve())
               for name, module in list(sys.modules.items())
               if getattr(module, '__file__', None)}
    project = {name: path for name, path in modules.items()
               if name.startswith('_gapn') or name in known_names
               or Path(path).stem in known_names}
    checks = {}
    for name, path in project.items():
        actual = Path(path)
        checks[name] = {'path': path, 'listed_copy': actual in expected,
                        'sha256': hashlib.sha256(actual.read_bytes()).hexdigest()}
        checks[name]['unchanged'] = checks[name]['sha256'] == expected.get(actual)
    output = {'argv_at_exit': sys.argv, 'cwd': os.getcwd(),
              'all_loaded_file_modules': modules, 'project_modules': checks,
              'project_isolation_pass': bool(project) and all(v['listed_copy'] and v['unchanged'] for v in checks.values())}
    Path(os.environ['REVIEW_ORIGINS_OUTPUT']).write_text(json.dumps(output, indent=2) + '\n')


atexit.register(record_origins)
