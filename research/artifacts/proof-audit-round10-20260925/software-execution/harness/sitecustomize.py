import atexit, datetime, hashlib, json, os, pathlib, sys
_root=pathlib.Path(os.environ['REVIEW_ROOT']).resolve()
_write_events=[]

def _check_write(event, p):
    if not isinstance(p,(str,bytes,os.PathLike)): return
    q=pathlib.Path(os.fsdecode(p)).absolute()
    good=q.is_relative_to(_root) or q.is_relative_to(pathlib.Path(os.environ['TMPDIR']))
    _write_events.append({'event':event,'path':str(q),'allowed':good})
    if not good: raise PermissionError('review write outside private directory: '+str(q))

def _audit(event,args):
    if event=='open':
        path,mode,flags=args
        if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or (flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)):
            _check_write(event,path)
    elif event in ('os.mkdir','os.remove','os.rmdir','os.chmod','os.truncate'):
        _check_write(event,args[0])
    elif event in ('os.rename','os.link','os.symlink'):
        _check_write(event,args[0]); _check_write(event,args[1])
sys.addaudithook(_audit)

def _save():
    modules=[]
    for name,mod in list(sys.modules.items()):
        f=getattr(mod,'__file__',None)
        if name.startswith(('_gapn2','_sl_prufer','reflection_seeds')) or (f and pathlib.Path(f).name.startswith(('_gapn2','_sl_prufer','reflection_seeds'))):
            p=pathlib.Path(f).resolve() if f else None
            modules.append({'name':name,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p and p.is_file() else None})
    result={'pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'sys_path':sys.path,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'optimization':sys.flags.optimize,'modules':modules,'write_events':list(_write_events)}
    (_root/'logs'/('origins-'+os.environ.get('REVIEW_RUN','unknown')+'-'+str(os.getpid())+'.json')).write_text(json.dumps(result,indent=2))
atexit.register(_save)
# Capture actual worker state at entry to its first real solver job. This only
# observes frames/module identities; it does not replace any candidate function.
if os.environ.get('REVIEW_CAPTURE_WORKERS')=='1':
    def _worker_profile(frame,event,arg):
        if event=='call' and frame.f_code.co_name=='one_solve' and pathlib.Path(frame.f_code.co_filename).name=='_gapn2_symmetry_recon.py':
            sys.setprofile(None)
            _save()
    sys.setprofile(_worker_profile)
