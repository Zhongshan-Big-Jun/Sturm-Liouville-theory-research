"""Read-only AST/call-site inventory; writes only its own author reports."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

Root=Path('/mnt/f/LaTeX/BVE research')
Own=Path(__file__).resolve().parent
Changed={Path(Name).stem for Name in json.loads((Own/'baseline.json').read_text())['files']}
Modules={}
Imports={}
Direct=[]
Symbols={'eigfun','eigenfunction_states','eigen_data','uv_at','prop_matrix','green_kernel','green_regular','green_regularized','_propagate','analytic_jacobian','analytic_jacobian_spectral','term_breakdown'}
for File in sorted((Root/'scripts').glob('*.py')):
	try:
		Tree=ast.parse(File.read_text(encoding='utf-8-sig'))
	except (SyntaxError,UnicodeError):
		continue
	Modules[File.stem]=Tree
	Imported=[]
	for Node in ast.walk(Tree):
		if isinstance(Node,ast.ImportFrom):
			Imported.append(Node.module)
			if Node.module in Changed:
				for Alias in Node.names:
					if Alias.name in Symbols:
						Local=Alias.asname or Alias.name
						Calls=[N.lineno for N in ast.walk(Tree) if isinstance(N,ast.Call) and isinstance(N.func,ast.Name) and N.func.id==Local]
						Direct.append(dict(path=str(File.relative_to(Root)),module=Node.module,symbol=Alias.name,import_line=Node.lineno,call_lines=sorted(Calls)))
		elif isinstance(Node,ast.Import):
			Imported.extend(Alias.name for Alias in Node.names)
	Imports[File.stem]=Imported
Impacted=set(Changed)
while True:
	New={Module for Module,Dependencies in Imports.items() if set(Dependencies)&Impacted}
	if New<=Impacted:
		break
	Impacted|=New
Protected={
	'_gapn2_symmetry_recon.py':['roots_of','D_scalar','Recon'],
	'_gapn2_jacobian_spectral.py':['gtilde_spectral'],
	'_gapn2_half_problem_probe.py':['HalfSpectrum','half_spectrum','_green_table','_green_sum','_spectral_green','_spectral_full_green'],
}
Continuity=[]
for Name,Nodes in Protected.items():
	Old={Node.name:ast.dump(Node,include_attributes=False) for Node in ast.parse((Own/'baseline'/Name).read_text()).body if hasattr(Node,'name')}
	Current={Node.name:ast.dump(Node,include_attributes=False) for Node in ast.parse((Root/'scripts'/Name).read_text()).body if hasattr(Node,'name')}
	for Node in Nodes:
		if Old[Node]!=Current[Node]:
			raise RuntimeError('protected AST changed: '+Name+':'+Node)
		Continuity.append(Name+':'+Node)
Unchanged=['_sl_prufer.py','reflection_seeds.py','_gapn2_jacobian_probe.py','_gapn2_sector_decomposition.py']
Hashes={}
for Name in Unchanged:
	Data=(Root/'scripts'/Name).read_bytes()
	Old=subprocess.check_output(['git','show','HEAD:scripts/'+Name],cwd=Root)
	if Data!=Old:
		raise RuntimeError('protected source changed since HEAD: '+Name)
	Hashes[Name]=hashlib.sha256(Data).hexdigest()
# New changed-source executable indentation should use tabs. Unchanged legacy
# bodies are intentionally left as-is. Parse/compile never writes pyc files.
for Name in json.loads((Own/'baseline.json').read_text())['files']:
	compile((Root/Name).read_text(),str(Root/Name),'exec')
Report=dict(changed=sorted(Changed),direct_imports=Direct,transitive_import_modules=sorted(Impacted),
	protected_ast_unchanged=Continuity,protected_files_equal_HEAD=Hashes,
	boundary='static import/call-site inventory only; not execution coverage for every caller')
(Own/'static_impacts.json').write_text(json.dumps(Report,indent=2)+'\n')
print(json.dumps(dict(direct_import_sites=len(Direct),direct_files=len({Row['path'] for Row in Direct}),
	transitive_modules=len(Impacted),protected_ast=len(Continuity),protected_files=len(Hashes))))
