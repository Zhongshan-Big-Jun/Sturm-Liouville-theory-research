from run import *
Checks=[('export-01','ExportDeclarations.lean',0),('print-01','PrintDeclarations.lean',0),('positive-01','PositiveControls.lean',0),('negative-sign-01','NegativeDeterminantSign.lean',1),('negative-blocks-01','NegativeDiagonalBlocks.lean',1),('negative-boundary-01','NegativeBoundaryFormula.lean',1),('negative-physical-01','NegativePhysicalSign.lean',1)]
Results=[]
for Label,File,Expected in Checks:
	Source=PROJECT/File
	Object=BASE/'objects'/Label/Path(File).with_suffix('.olean').name
	Object.parent.mkdir(parents=True,exist_ok=False)
	R=run(Label,[LEAN,'-R',win(PROJECT),'-o',win(Object),win(Source)],Inputs=[Path(__file__),Source,PROJECT/'AuditRound11.lean',BASE/'objects/main-final/AuditRound11.olean'],Extra=[BASE/'objects/main-final'])
	Results.append({'label':Label,'file':File,'expected_exit':Expected,'actual_exit':R['exit_code'],'as_expected':R['exit_code']==Expected,'command_record':f'commands/{Label}/command.json'})
	write_json(BASE/'author-checks.json',Results)
print('expected outcomes:',sum(R['as_expected'] for R in Results),'/',len(Results))
