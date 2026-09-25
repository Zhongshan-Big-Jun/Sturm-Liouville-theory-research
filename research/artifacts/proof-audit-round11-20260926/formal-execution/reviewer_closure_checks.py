from run import *
Control=BASE/'closure-control-project'
Results=[]
for Name,Expected in [('positive',True),('hidden-axiom',False),('wrong-type',False),('missing-target',False)]:
	Label='closure-'+Name+'-01'
	Contract=BASE/('control-'+Name+'.json')
	Out=BASE/'evidence'/Label
	R=run(Label,[sys.executable,'-B',PLUGIN/'scripts/verify_lean_project.py','--project',Control,'--contract',Contract,'--lean',LEAN,'--lake',LAKE,'--direct','--strict-exit','--build-timeout','600','--output',Out],Cwd=Control,Inputs=[Path(__file__),Control/'ClosureControl.lean',Control/'lean-toolchain',Contract])
	Manifest=Out/'run-manifest.json'
	Data=json.loads(Manifest.read_text()) if Manifest.exists() else {}
	Results.append({'name':Name,'expected_exact_root_passed':Expected,'actual_exact_root_passed':Data.get('exact_root_passed'),'exit_code':R['exit_code'],'root_closure':Data.get('root_closure'),'manifest':str(Manifest.relative_to(BASE)),'as_expected':Data.get('exact_root_passed')==Expected and R['exit_code']==(0 if Expected else 1)})
	write_json(BASE/'reviewer-closure-checks.json',Results)
print('closure controls:',sum(R['as_expected'] for R in Results),'/',len(Results))
