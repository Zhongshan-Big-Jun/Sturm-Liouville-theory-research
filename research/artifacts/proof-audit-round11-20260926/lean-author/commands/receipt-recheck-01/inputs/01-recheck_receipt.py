from run import *
Manifest=BASE/'evidence/exact-root-01/run-manifest.json'
R=run('receipt-recheck-01',[sys.executable,'-B',PLUGIN/'scripts/lean_evidence.py','--manifest',Manifest],Inputs=[Path(__file__),Manifest,PROJECT/'AuditRound11.lean',BASE/'contract.json'])
sys.exit(R['exit_code'])
