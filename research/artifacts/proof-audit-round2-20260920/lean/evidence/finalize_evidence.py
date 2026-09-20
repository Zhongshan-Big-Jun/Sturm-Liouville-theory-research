from pathlib import Path
import hashlib,json,re,datetime,subprocess,os
OUT=Path('/mnt/f/tools/math-audit-round2-20260920/lean-author')
ROOT=Path('/mnt/f/LaTeX/BVE research')
SOURCE=ROOT/'lean-proof/SL/AuditRound2.lean'

def digest(p):
	return hashlib.sha256(p.read_bytes()).hexdigest()

inventory=json.loads((OUT/'imported-artifact-hashes.json').read_text())
assert inventory['module_count']==3740
assert len(inventory['modules'])==inventory['module_count']
assert inventory['artifact_count']==sum(len(x['artifacts']) for x in inventory['modules'])
assert len({x['module'] for x in inventory['modules']})==inventory['module_count']
evidence=json.loads((OUT/'declaration-evidence.json').read_text())
assert evidence['source_sha256']==digest(SOURCE)
assert evidence['theorem_count']==25
assert evidence['all_target_closures_within_policy']
bridge=json.loads((OUT/'bridge-evidence.json').read_text())
assert len(bridge['declarations'])==5
assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',SOURCE.read_text())
for name in ['13-interface-fix','14-print-types-axioms','16-existing-sl-bridge-merged']:
	r=json.loads((OUT/'logs'/f'{name}.json').read_text())
	assert r['exit_code']==0 and r['source_unchanged_during_run']
	assert r['source_sha256_after'][str(SOURCE)]==digest(SOURCE)
	assert r['stdout_sha256']==digest(OUT/'logs'/f'{name}.stdout.txt')
	assert r['stderr_sha256']==digest(OUT/'logs'/f'{name}.stderr.txt')
	assert not re.search(r'(?:^|\n).*:(?: error| warning)',(OUT/'logs'/f'{name}.stdout.txt').read_text())
run=json.loads((OUT/'logs/13-interface-fix.json').read_text())
assert run['output_artifact']['sha256']==digest(OUT/'build/SL/AuditRound2.olean')
for item in inventory['modules']:
	if item['module']=='SL.AuditRound2':
		assert item['artifacts'][0]['sha256']==run['output_artifact']['sha256']
base=json.loads((OUT/'source-baseline.json').read_text())
checks=[]
for r in base['files']:
	p=Path(r['path']); now=digest(p) if p.exists() else None
	checks.append({'path':str(p),'sha256_before':r['sha256'],'sha256_after':now,'unchanged':now==r['sha256']})
original_lean=[r for r in checks if '/lean-proof/' in r['path']]
assert len(original_lean)==46
assert all(r['unchanged'] for r in original_lean)
comparison={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Only this new Lean file and external lean-author files were written by this author. Root AGENTS and TeX changes observed during concurrent work are preserved and not attributed to this author.','files':checks}
(OUT/'protected-source-comparison.json').write_text(json.dumps(comparison,indent=2))
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
status=subprocess.run(['git','status','--short','--','lean-proof'],cwd=ROOT,env=env,capture_output=True,text=True)
(OUT/'logs/17-final-git-status.stdout.txt').write_text(status.stdout)
(OUT/'logs/17-final-git-status.stderr.txt').write_text(status.stderr)
(OUT/'logs/17-final-git-status.json').write_text(json.dumps({'argv':['git','status','--short','--','lean-proof'],'cwd':str(ROOT),'exit_code':status.returncode,'stdout_sha256':digest(OUT/'logs/17-final-git-status.stdout.txt'),'stderr_sha256':digest(OUT/'logs/17-final-git-status.stderr.txt')},indent=2))
assert status.returncode==0
assert status.stdout.strip()=='?? lean-proof/SL/AuditRound2.lean',status.stdout
report=OUT/'REPORT.md'
s=report.read_text()
text='\n最终依赖清单: '+str(inventory['module_count'])+' 个实际加载模块, '+str(inventory['artifact_count'])+' 个对象文件, '+str(inventory['total_bytes'])+' 字节; 只读哈希耗时 '+str(round(inventory['elapsed_seconds'],2))+' 秒. `FINAL_CHECKS.json` 保存作者收尾核对, `FILE_HASHES.sha256` 固定本次交付文件字节.\n'
if '最终依赖清单:' not in s: report.write_text(s+text)
summary={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'author; not final acceptance','main_theorems':25,'external_definition_bridges':5,'compile_exit_code':0,'inspection_exit_code':0,'external_bridge_exit_code':0,'actual_imported_modules':inventory['module_count'],'hashed_imported_artifacts':inventory['artifact_count'],'source_sha256':digest(SOURCE),'olean_sha256':digest(OUT/'build/SL/AuditRound2.olean'),'main_axioms_within_policy':True,'all_42_original_SL_sources_unchanged':True,'STATUS_lakefile_toolchain_manifest_unchanged':True,'observed_other_changed_sources':[r['path'] for r in checks if not r['unchanged']],'independent_review':'not performed by this author','full_K1_limit':'not formalized','full_MW_spectral_chain':'not formalized','first_pair_global_optimality':'not formalized','commit_or_push_performed':False}
(OUT/'FINAL_CHECKS.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
logs=[]
for p in sorted((OUT/'logs').glob('*.json')):
	logs.append({'run':p.stem,**json.loads(p.read_text())})
(OUT/'command-index.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
files=[SOURCE]+sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='FILE_HASHES.sha256' and '__pycache__' not in p.parts)
(OUT/'FILE_HASHES.sha256').write_text(''.join(digest(p)+'  '+str(p)+'\n' for p in files))
print(json.dumps({'status':'AUTHOR_EVIDENCE_COMPLETE','main_theorems':25,'definition_bridges':5,'imported_modules':inventory['module_count'],'hashed_imported_artifacts':inventory['artifact_count'],'handoff_files_hashed':len(files),'new_lean_sha256':digest(SOURCE),'report':str(report)},ensure_ascii=False))
