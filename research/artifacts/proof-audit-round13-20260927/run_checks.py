"""Portable replay of preserved R13 property tests, without editing evidence.

Examples: python3 research/artifacts/proof-audit-round13-20260927/run_checks.py
          python3 .../run_checks.py --optimized --suite certificate
Requires numpy/mpmath for spectral tests. Recompute the accepted certificate
first with misc/e1_certgen.py if its bound sources have changed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time

Artifact = Path(__file__).resolve().parent
Parser = argparse.ArgumentParser(description=__doc__)
Parser.add_argument('--root', type=Path, default=Artifact.parents[2])
Parser.add_argument('--suite', choices=['all','certificate','interval','spectral','round12'], default='all')
Parser.add_argument('--optimized', action='store_true')
Parser.add_argument('--output', type=Path)
Args = Parser.parse_args()
Root = Args.root.resolve()
Output = (Args.output or Path(tempfile.mkdtemp(prefix='sl-round13-results-'))).resolve()
Output.mkdir(parents=True, exist_ok=True)
Prefix = [sys.executable] + (['-O'] if Args.optimized else []) + ['-B']
Suites = ['interval','certificate','spectral','round12'] if Args.suite=='all' else [Args.suite]
Results = []
with tempfile.TemporaryDirectory(prefix='sl-round13-replay-') as Temporary:
	Working = Path(Temporary)
	for Name in Suites:
		Bindings = {}
		if Name=='certificate':
			Command = Prefix + [str(Root/'scripts/test_round13_certificates.py')]
		else:
			Names = {'interval':['interval-author/test_rigid1d.py'], 'spectral':['spectral-author/test_round13.py','spectral-author/reference.py'], 'round12':['spectral-author/r12_regression.py']}[Name]
			for Relative in Names:
				Source = Artifact/Relative
				Raw = Source.read_bytes()
				# Only the old author-specific repository path is relocated. The
				# preserved original is never overwritten; both hashes are logged.
				Text = Raw.decode('utf-8').replace("Path('/mnt/f/LaTeX/BVE research')",'Path('+repr(str(Root))+')')
				Target = Working/Source.name
				Target.write_text(Text,encoding='utf-8')
				Bindings[Relative] = dict(original_sha256=hashlib.sha256(Raw).hexdigest(), executed_sha256=hashlib.sha256(Target.read_bytes()).hexdigest())
			Command = Prefix + [str(Working/Path(Names[0]).name)] + ([str(Root)] if Name=='round12' else [])
		Start = time.monotonic()
		with (Output/(Name+'.stdout')).open('w') as Stdout, (Output/(Name+'.stderr')).open('w') as Stderr:
			Run = subprocess.run(Command,cwd=Root,stdout=Stdout,stderr=Stderr)
		Results.append(dict(suite=Name,argv=Command,exit_code=Run.returncode,seconds=time.monotonic()-Start,bindings=Bindings))
		(Output/'results.json').write_text(json.dumps(Results,indent=2)+'\n')
		print(Name,'exit',Run.returncode,flush=True)
print('Results:',Output)
raise SystemExit(0 if all(Row['exit_code']==0 for Row in Results) else 1)
