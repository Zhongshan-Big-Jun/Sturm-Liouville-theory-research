from pathlib import Path
import datetime,hashlib,json,sys
import numpy as np
import _gapn2_symmetry_recon as rcmod
import reflection_seeds as seeds
import _sl_prufer as sl
root=Path(__file__).resolve().parent.parent
manifest=json.loads((root/'manifest-before.json').read_text())
rows=[]
def check(name,ok,detail=None):
 rows.append({'name':name,'passed':bool(ok),'detail':detail})
 if not ok:raise RuntimeError(name+': '+str(detail))
expected={str(Path(x['copy']).resolve()):x['sha256'] for x in manifest['files']}
for r in manifest['files']:
 check('frozen-and-copy-hash-'+r['original'],all(hashlib.sha256(Path(r[k]).read_bytes()).hexdigest()==r['sha256'] for k in ['snapshot','copy']))
check('packet-still-frozen',hashlib.sha256(Path(manifest['packet']).read_bytes()).hexdigest()==manifest['packet_sha256'])
for name in ['spectrum','spectrum-opt','reflection','reflection-opt','variation-sup','variation-inf','variation-r1','adversarial-final','recon-linux-tmp','recon-observed','recon-asymmetric-center']:
 d=json.loads((root/'logs'/(name+'.run.json')).read_text())
 check('actual-returncode-'+name,d['returncode']==0 and d['sources_unchanged'],{'seconds':d['seconds'],'returncode':d['returncode']})
origins=[]
for p in sorted((root/'logs').glob('origins-*.json')):
 d=json.loads(p.read_text())
 for m in d['modules']:
  check('import-origin-'+p.name+'-'+m['name'],m['path'] in expected and m['sha256']==expected[m['path']],m)
 origins.append({'file':str(p),'pid':d['pid'],'modules':d['modules'],'blocked_write_attempts':[e for e in d['write_events'] if not e['allowed']]})
# Parent, forkserver, and both workers are distinct captured processes.
observed=[x for x in origins if Path(x['file']).name.startswith('origins-recon-observed-') and x['modules']]
check('worker-origin-coverage',len(observed)==4,[x['pid'] for x in observed])
for name in ['sup','inf','r1']:
 d=json.loads((root/'results'/('variation-'+name+'.json')).read_text())
 check('cli-defaults-'+name,(d['retained_modes'],d['gauss_order_per_interval'],d['digits'])==(61,64,60))
 for p,h in d['source_sha256'].items():check('cli-source-'+name+'-'+Path(p).name,p in expected and h==expected[p])
 records=d['root_index_records'];rt=sl.indexed_roots(d['blocks'],61)[0]
 check('cli-root-index-records-'+name,len(records)==61 and all(r['index']==j+1 and r['certified'] is False and r['phase_bracket'][0]<=r['target_phase']<=r['phase_bracket'][1] and r['bracket'][0]<=r['frequency']<=r['bracket'][1] for j,r in enumerate(records)))
 check('cli-root-record-identity-'+name,np.array_equal(rt,np.array([r['frequency'] for r in records])))
 check('cli-mode-pair-'+name,np.allclose([d['lambda_n'],d['lambda_np1']],rt[[1,2]]**2,rtol=2e-13,atol=0))
for folder in ['recon','recon-observed']:
 for mode in ['sup','inf']:
  p=root/'results'/folder/('_gapn2_symmetry_recon_n2_'+mode+'-seeds.json');d=json.loads(p.read_text());rc=rcmod.Recon(2,4,mode)
  check('main-seed-counts-'+folder+'-'+mode,len(d['random_seeds'])==2 and len(d['sector_seeds'])==20)
  for path,h in d['source_sha256'].items():check('main-source-'+folder+'-'+mode+'-'+Path(path).name,path in expected and h==expected[path])
  labels=set()
  for seed in d['sector_seeds']:
   widths=rc.z_to_widths(seed['Z']);e=np.cumsum(widths)[:-1];b=np.array(seed['BaseEdges']);delta=e-b;sgn=-1 if seed['Sector']=='preserve' else 1
   ck=seeds.check_sector_seed(b,widths,seed['Sector'],Direction=seed['Direction'],ExpectedStep=seed['UsedStep'])
   check('main-geometry-'+folder+'-'+mode+'-'+seed['label'],np.array_equal(widths,np.array(seed['Widths'])) and np.array_equal(e,np.array(seed['Edges'])) and np.max(np.abs(delta-sgn*delta[::-1]))<=2e-8*np.max(np.abs(delta)) and seed['label'].startswith('pure_reflection:'))
   labels.add(seed['label'])
  check('main-ordinary-random-separation-'+folder+'-'+mode,all(x['origin']=='random_width' and x['label'].startswith('random_width:') and x['label'] not in labels for x in d['random_seeds']))
for mode in ['sup','inf']:
 p=root/'results/recon-asymmetric-center'/('_gapn2_symmetry_recon_n2_'+mode+'-seeds.json');d=json.loads(p.read_text())
 check('actual-main-records-rejected-center-'+mode,len(d['sector_seeds'])==10 and all(x['status']=='rejected_seed' and 'not reflection-symmetric' in x['reason'] for x in d['sector_seeds']) and d['converged']==0)
 for path,h in d['source_sha256'].items():check('rejection-run-source-'+mode+'-'+Path(path).name,hashlib.sha256(Path(path).read_bytes()).hexdigest()==h)
report={'status':'PASS','count':len(rows),'checks':rows,'module_origin_records':origins,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(root/'results/artifact-validation.json').write_text(json.dumps(report,indent=2))
(root/'manifest-after.json').write_text(json.dumps({'packet_sha256':manifest['packet_sha256'],'sources_unchanged':True,'files':manifest['files'],'review_scripts':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'harness').glob('*.py')}},indent=2))
print(json.dumps({'status':'PASS','count':len(rows),'observed_main_forkserver_worker_pids':[x['pid'] for x in observed]}))
