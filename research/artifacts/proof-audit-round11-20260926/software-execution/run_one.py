import datetime,hashlib,json,os,pathlib,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parent
label=sys.argv[1]; args=sys.argv[2:]
out=root/'results'; manifest=json.loads((root/'manifest.json').read_text())
def hashes():
    return {k:hashlib.sha256((root/k).read_bytes()).hexdigest() for k in manifest['sources']}
argv=[sys.executable,'-B',*args]
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root/'instrumentation'),AUDIT_PRIVATE_ROOT=str(root),AUDIT_ORIGINS_OUTPUT=str(out/(label+'.modules.json')),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
record={'label':label,'argv':argv,'cwd':str(root),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_hashes_before':hashes()}
start=time.monotonic()
with (out/(label+'.stdout.txt')).open('w') as stdout, (out/(label+'.stderr.txt')).open('w') as stderr:
    result=subprocess.run(argv,cwd=root,env=env,stdout=stdout,stderr=stderr)
record.update(returncode=result.returncode,elapsed_seconds=time.monotonic()-start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_hashes_after=hashes())
record['sources_unchanged']=record['source_hashes_before']==record['source_hashes_after']=={k:v['sha256'] for k,v in manifest['sources'].items()}
origins=out/(label+'.modules.json')
record['all_module_origins_match']=json.loads(origins.read_text())['all_match'] if origins.exists() else False
(out/(label+'.execution.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ('label','returncode','elapsed_seconds','sources_unchanged','all_module_origins_match')}),flush=True)
print((out/(label+'.stdout.txt')).read_text()[-6000:],flush=True)
print((out/(label+'.stderr.txt')).read_text()[-3000:],flush=True)
raise SystemExit(result.returncode)
