"""Fresh standalone round8 replay. python3 -B replay.py NEW_OUTPUT_DIRECTORY

All generated files, current-source compilation and receipts go in NEW_OUTPUT_DIRECTORY.
The package itself and installed external Lean/Mathlib artifacts are read-only.
No downloads, Lake build, agents or independent-semantic-review claim.
Exporter algorithms and logging patterns are attributed in attribution.json.
"""
from pathlib import Path
import argparse, concurrent.futures, datetime, hashlib, json, os, re, shutil, sys, time, uuid
from run_lean import BASE, digest, environment, run, win, write_json


def require(condition, message):
	if not condition: raise RuntimeError(message)


def host_path(path):
	if re.match(r'^[A-Za-z]:[\\/]',path):
		return Path('/mnt/'+path[0].lower()+'/'+path[3:].replace('\\','/')).resolve()
	return Path(path).resolve()


def artifact_paths(modules):
	paths={}
	for item in modules:
		base=host_path(item['olean'])
		require(base.is_file(),'Missing imported module '+str(base))
		for suffix in ('','.private','.server'):
			p=Path(str(base)+suffix)
			if p.is_file(): paths[str(p)]=p
		p=base.with_suffix('.ir')
		if p.is_file(): paths[str(p)]=p
	return paths


def hash_files(paths):
	# A bounded pool accelerates mounted-filesystem reads. Hash bytes afresh, never trust .hash files.
	items=list(paths.items())
	def one(item):
		name,p=item
		before=p.stat()
		h=digest(p)
		after=p.stat()
		require((before.st_size,before.st_mtime_ns,before.st_ctime_ns)==(after.st_size,after.st_mtime_ns,after.st_ctime_ns),'File changed while hashing '+str(p))
		return name,{'sha256':h,'bytes':after.st_size,'mtime_ns':after.st_mtime_ns,'ctime_ns':after.st_ctime_ns}
	with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
		return dict(pool.map(one,items))


def byte_map(inventory):
	return {k:v['sha256'] for k,v in inventory.items()}


def stable_digest(data):
	return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('output',type=Path)
	args=parser.parse_args()
	out=args.output.resolve()
	require(out!=BASE and not BASE.is_relative_to(out),'Output must not contain the input package')
	out.mkdir(parents=True,exist_ok=False)
	runid=str(uuid.uuid4())
	start=datetime.datetime.now(datetime.timezone.utc).isoformat()
	write_json(out/'run-start.json',{'run_id':runid,'utc_start':start,'pid':os.getpid(),'role':'replay_execution_only','independent_semantic_review':'not_performed'})
	freeze=json.loads((BASE/'freeze.json').read_text())
	checks={n:digest(BASE/n)==h for n,h in freeze['files'].items()}
	write_json(out/'frozen-input-checks.json',checks)
	require(all(checks.values()),'Frozen package input mismatch')
	config=json.loads((BASE/'runtime-config.json').read_text())
	lean=Path(config['lean'])
	toolchain=lean.parent.parent
	runtime_paths={str(p):p for p in [lean]+sorted(lean.parent.glob('*.dll'))}
	before_runtime=hash_files(runtime_paths)
	write_json(out/'runtime-before.json',before_runtime)
	require(digest(lean)==freeze['lean_exe_sha256'],'Pinned Lean executable mismatch')
	bound=BASE/'external-environment.json'
	if bound.exists():
		binding=json.loads(bound.read_text())
		require(byte_map(before_runtime)==binding['runtime_hashes'],'External runtime differs from frozen author runtime')
	else: binding=None
	src=out/'src';lib=out/'lib'
	src.mkdir();lib.mkdir()
	for n in ['AuditRound8.lean']:
		shutil.copyfile(BASE/n,src/n)
	source=src/'AuditRound8.lean'
	obj=lib/'AuditRound8.olean'
	env=environment(out)
	inputs=[BASE/n for n in freeze['files']]
	version=run(out,'01-version',[str(lean),'--version'],env,src,[source])
	require(version['exit_code']==0,'Version command failed')
	versiontext=(out/'logs/01-version.stdout.txt').read_text().strip()
	require('version 4.31.0, x86_64-w64-windows-gnu' in versiontext,'Wrong Lean platform/version')
	git=shutil.which('git')
	require(git is not None,'git is required only for a read-only Mathlib revision check')
	mathlib=Path(config['original_project'])/'.lake/packages/mathlib'
	gr=run(out,'02-mathlib-revision',[git,'-C',str(mathlib),'rev-parse','HEAD'],env,src,[BASE/'runtime-config.json'])
	require(gr['exit_code']==0 and (out/'logs/02-mathlib-revision.stdout.txt').read_text().strip()==config['mathlib_commit'],'Mathlib revision mismatch')
	# Discover actual imported modules before current-source compilation, including the Lean exporter environment.
	direct=re.findall(r'^import (.+)$',source.read_text(),re.M)
	imports=out/'Imports.lean'
	imports.write_text('\n'.join('import '+m for m in direct)+'\nimport Lean\nopen Lean Elab Command in\nrun_cmd do\n  let env := (← getEnv).setExporting false\n  let mut rows := #[]\n  for name in env.header.moduleNames.qsort Name.lt do\n    let path ← findOLean name\n    rows := rows.push <| Json.mkObj [("module", toJson name.toString),("olean",toJson path.toString)]\n  IO.FS.writeFile '+json.dumps(win(out/'import-discovery.json'))+' ((Json.arr rows).compress ++ "\\n")\n')
	disc=run(out,'03-import-discovery',[str(lean),win(imports)],env,src,[source,imports], [out/'import-discovery.json'])
	require(disc['exit_code']==0,'Actual import discovery failed')
	modules=json.loads((out/'import-discovery.json').read_text())
	external_paths=artifact_paths(modules)
	print('Hashing',len(modules),'loaded external modules,',len(external_paths),'compiled/IR artifacts before proof compilation',flush=True)
	before=hash_files(external_paths)
	write_json(out/'imports-before.json',before)
	if binding:
		require(byte_map(before)==binding['import_hashes'],'External import identity differs from frozen author execution')
	comp=run(out,'04-compile-current-source',[str(lean),'--root='+win(src),'-o',win(obj),win(source)],env,src,[source]+inputs,[obj])
	require(comp['exit_code']==0 and obj.is_file(),'Current source did not compile')
	probeenv=environment(out,[lib])
	contract=json.loads((BASE/'positive-contract.json').read_text())
	positive=out/'PositiveControl.lean'
	positive.write_text('import AuditRound8\nopen AuditRound8\nexample : '+contract['expected_type']+' := AuditRound8.local_root\n')
	pr=run(out,'05-positive-control',[str(lean),win(positive)],probeenv,src,[source,positive,BASE/'positive-contract.json'],[obj])
	require(pr['exit_code']==0,'Positive exact-contract compilation failed')
	inspection=out/'Inspection.lean'
	prefix=(BASE/'ExporterPrefix.lean.txt').read_text()
	suffix=(BASE/'ExporterSuffix.lean.txt').read_text().replace('"OUTPUT_PLACEHOLDER"',json.dumps(win(out/'declarations.json')))
	inspection.write_text(prefix+'\nopen AuditRound8\ntheorem positive_control : '+contract['expected_type']+' := AuditRound8.local_root\n\n'+suffix)
	ir=run(out,'06-declaration-inspection',[str(lean),win(inspection)],probeenv,src,[source,inspection,BASE/'positive-contract.json'],[out/'declarations.json',obj])
	require(ir['exit_code']==0,'Declaration inspection failed')
	decls=json.loads((out/'declarations.json').read_text())
	public=decls['public_declarations']
	expected_names=['AuditRound8.'+n for n in re.findall(r'^(?:def|theorem|lemma) (\w+)',source.read_text(),re.M)]
	require(sorted(p['declaration'] for p in public)==sorted(expected_names),'Complete public declaration inventory mismatch')
	require(decls['expected_type_match'],'Expected type mismatch')
	allowed={'propext','Classical.choice','Quot.sound'}
	require(all(set(p['axioms'])<=allowed and not p['unsafe'] for p in public),'Unaccepted public axioms/unsafe declaration')
	bad=[n for n in decls['dependencies'] if n.get('missing') or n.get('unsafe') or (n.get('kind')=='axiom' and n['name'] not in allowed)]
	require(not bad,'Bad transitive dependency closure: '+str(bad))
	loaded={m['module']:str(host_path(m['olean'])) for m in decls['modules']}
	discovered={m['module']:str(host_path(m['olean'])) for m in modules}
	require(len(loaded)==decls['loaded_module_count'],'Loaded module inventory count mismatch')
	require(loaded.pop('AuditRound8',None)==str(obj),'Inspection imported stale or shadowed root olean')
	require(loaded==discovered,'Inspection environment differs from precompiled import environment')
	resolution=run(out,'07-root-resolution',[str(lean),'--deps',win(positive)],probeenv,src,[source,positive],[obj])
	require(resolution['exit_code']==0,'Root --deps failed')
	resolved=[str(host_path(s)) for s in (out/'logs/07-root-resolution.stdout.txt').read_text().splitlines() if s.strip()]
	require(str(obj) in resolved,'Positive control did not resolve fresh object')
	negative=[]
	for i,(name,needle) in enumerate([('WrongPhase','Type mismatch'),('WrongStationaryFactor','Type mismatch'),('WrongScalar','unsolved goals')],8):
		control=out/(name+'.lean');shutil.copyfile(BASE/'controls'/(name+'.lean'),control)
		label=f'{i:02d}-'+name
		r=run(out,label,[str(lean),win(control)],probeenv,src,[source,control],[obj])
		output=(out/'logs'/(label+'.stdout.txt')).read_text()
		require(r['exit_code']!=0 and needle in output,'Wrong-target control did not fail as expected: '+name)
		require('unknown module' not in output.lower() and 'unknown identifier' not in output.lower(),'Negative failed for an import/name error')
		negative.append({'name':name,'run_id':r['run_id'],'exit_code':r['exit_code'],'stdout_sha256':r['stdout_sha256'],'stderr_sha256':r['stderr_sha256']})
	print('Rehashing runtime and every loaded external artifact after all controls',flush=True)
	after=hash_files(external_paths);after_runtime=hash_files(runtime_paths)
	write_json(out/'imports-after.json',after);write_json(out/'runtime-after.json',after_runtime)
	require(before==after and before_runtime==after_runtime,'External artifacts changed during execution')
	require(digest(source)==freeze['files']['AuditRound8.lean'],'Compiled source differs from package source')
	require(all(digest(BASE/n)==h for n,h in freeze['files'].items()),'Frozen input changed during execution')
	external_binding={'mathlib_commit':config['mathlib_commit'],'lean_version':versiontext,'runtime_hashes':byte_map(before_runtime),'import_hashes':byte_map(before),'external_modules':discovered}
	write_json(out/'external-environment.json',external_binding)
	root=next(p for p in public if p['declaration']=='AuditRound8.local_root')
	summary={'status':'AUTHOR_MACHINE_CHECKS_PASSED','run_id':runid,'utc_start':start,'utc_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),
		'role':'local_lean_author_execution','independent_verification':'not_performed','independent_semantic_review':'pending',
		'source_sha256':digest(source),'source_path':str(source),'olean_path':str(obj),'olean_sha256':digest(obj),
		'lean_version':versiontext,'mathlib_commit':config['mathlib_commit'],'exact_contract_matched':True,'root_axioms':root['axioms'],
		'public_declarations':len(public),'public_theorems':sum(p['kind']=='theorem' for p in public),'public_definitions':sum(p['kind']=='definition' for p in public),
		'closure_declarations':len(decls['dependencies']),'external_loaded_modules':len(modules),'inspected_loaded_modules':decls['loaded_module_count'],
		'external_import_artifacts':len(before),'runtime_binaries':len(before_runtime),'negative_controls':negative,'positive_control_exit_code':pr['exit_code'],
		'current_source_compilation_exit_code':comp['exit_code'],'input_and_import_stability':True,
		'environment_sha256':stable_digest(external_binding),'public_semantic_sha256':stable_digest(public),
		'contract_sha256':digest(BASE/'positive-contract.json'),'declarations_sha256':digest(out/'declarations.json'),
		'commands':len(list((out/'logs').glob('*.json'))),
		'excluded':['full spectral minmax','analytic implicit-function expansions and remainder','spectral identification of a/u/stationarity','T1/deep-sliver/global coverage','global convergence and minimizing-parameter rates','scalar estimates feeding scalarRatio other than the final rational comparison']}
	write_json(out/'evidence.json',summary)
	files={str(p.relative_to(out)):digest(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='receipt-manifest.json'}
	write_json(out/'receipt-manifest.json',{'run_id':runid,'files':files})
	print(json.dumps(summary,indent=2),flush=True)
	return 0

if __name__=='__main__':
	sys.exit(main())
