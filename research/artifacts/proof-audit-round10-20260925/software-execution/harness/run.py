from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time
root=Path(__file__).resolve().parent.parent
name=sys.argv[1]; argv=[sys.executable,'-B']+sys.argv[2:]
env=os.environ.copy(); env.update(REVIEW_ROOT=str(root),REVIEW_RUN=name,PYTHONPATH=str(root/'harness')+os.pathsep+str(root/'scripts'),PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',TMPDIR=(root/'temporary-runtime-directory.txt').read_text())
env['REVIEW_CAPTURE_WORKERS']='1' if name.startswith('recon-observed') else '0'
(root/'tmp').mkdir(exist_ok=True)
meta={'argv':argv,'cwd':str(root),'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'environment':{k:env.get(k) for k in ('PYTHONPATH','PYTHONDONTWRITEBYTECODE','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','TMPDIR','REVIEW_ROOT','REVIEW_RUN','REVIEW_CAPTURE_WORKERS','PATH')},'stdout':str(root/'logs'/(name+'.stdout')),'stderr':str(root/'logs'/(name+'.stderr'))}
start=time.monotonic()
with open(meta['stdout'],'w') as out,open(meta['stderr'],'w') as err:
    try: result=subprocess.run(argv,cwd=root,env=env,stdout=out,stderr=err,timeout=1800); meta['returncode']=result.returncode
    except subprocess.TimeoutExpired: meta['returncode']='timeout'
meta['seconds']=time.monotonic()-start;meta['end_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
meta['sources_unchanged']=all(hashlib.sha256(Path(row['copy']).read_bytes()).hexdigest()==row['sha256'] for row in json.loads((root/'manifest-before.json').read_text())['files'])
(root/'logs'/(name+'.run.json')).write_text(json.dumps(meta,indent=2))
print(json.dumps({k:meta[k] for k in ('argv','returncode','seconds','sources_unchanged')}))
print('STDOUT TAIL:',Path(meta['stdout']).read_text()[-1800:])
print('STDERR TAIL:',Path(meta['stderr']).read_text()[-1800:])
