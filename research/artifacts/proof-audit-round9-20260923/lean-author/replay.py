from author_runner import *

def verify(label,contract):
	return run(label,[sys.executable,'-B',PLUGIN/'scripts/verify_lean_project.py',
		'--project',PROJECT,'--contract',BASE/contract,'--lean',LEAN,'--lake',LAKE,
		'--direct','--strict-exit','--build-timeout','1800','--output',BASE/'evidence'/label],
		inputs=[BASE/contract,PROJECT/'AuditRound9.lean',PROJECT/'ConditionalRound9.lean',PROJECT/'lean-toolchain'])

if __name__=='__main__':
	prefix=sys.argv[1]
	steps=[('positive','positive-contract.json'),('wrong-type','controls/wrong-type.json'),
		('missing-target','controls/missing-target.json'),('unproved-premise','controls/unproved-premise.json')]
	results=[]
	for suffix,contract in steps:
		label=prefix+'-'+suffix
		r=verify(label,contract)
		manifest=BASE/'evidence'/label/'run-manifest.json'
		m=json.loads(manifest.read_text()) if manifest.exists() else {}
		if suffix=='positive':
			success=r['exit_code']==0 and m.get('machine_verification_passed') is True and m.get('exact_root_passed') is True
		elif suffix in ('wrong-type','unproved-premise'):
			success=(r['exit_code']!=0 and m.get('machine_verification_passed') is True
				and m.get('exact_root_passed') is False
				and m.get('root_closure',{}).get('status')=='target_mismatch'
				and m.get('target',{}).get('comparison',{}).get('status')=='mismatched')
		else:
			diagnostics='\n'.join(Path(x['stdout_log']).read_text(errors='replace')
				for x in m.get('build',{}).get('commands',[]) if x.get('kind')=='declaration_inspection')
			success=(r['exit_code']!=0 and m.get('exact_root_passed') is False
				and 'Exact root declaration not found: AuditRound9.missing_root' in diagnostics)

		results.append({'case':suffix,'manifest':str(manifest),'exit_code':r['exit_code'],
			'exact_root_passed':m.get('exact_root_passed'),'machine':m.get('machine'),
			'root_closure':m.get('root_closure'),'expected_behavior_observed':success})
		write_json(BASE/(prefix+'-summary.json'),results)
		if not success:sys.exit(2)
