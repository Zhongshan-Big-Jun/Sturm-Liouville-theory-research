from author_runner import *
prefix=sys.argv[1]
state=Path('/mnt/c/Users/HuangZY/.codex/plugins/cache/math-research/math-research-workflow/2.0.1/scripts/research_state.py')
inputs=[BASE/'author_runner.py',BASE/'replay.py',PROJECT/'AuditRound9.lean',PROJECT/'ConditionalRound9.lean',PROJECT/'lean-toolchain',PROJECT/'lake-manifest.json',PROJECT/'lakefile.toml',BASE/'positive-contract.json',*sorted((BASE/'controls').glob('*.json'))]
args=[sys.executable,'-B',state,'start','--project',BASE,'--job-id',prefix+'-durable','--cwd','.','--timeout','7200']
for p in inputs:args += ['--input',str(p.relative_to(BASE))]
args += ['--',sys.executable,'-B',BASE/'replay.py',prefix]
r=run('launch-'+prefix,args,cwd=BASE,inputs=inputs)
sys.exit(r['exit_code'])
