from pathlib import Path
import subprocess,json,datetime
O=Path('/mnt/f/tools/math-audit-round9-20260923');R=Path('/mnt/f/LaTeX/BVE research')
def require(v,m):
    if not v:raise RuntimeError(m)
def read(n):return json.loads((O/(n+'.json')).read_text())
Local=read('LOCAL_COMMIT_VERIFICATION');require(Local['status']=='PASS','Local committed bytes not checked')
Head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();require(Head==Local['commit'],'HEAD drift after verification')
require(subprocess.check_output(['git','branch','--show-current'],cwd=R,text=True).strip()=='main','Unexpected publication branch')
Baseline=read('baseline')['head'];Records=O/'remote-publication.json';Done=read('remote-publication') if Records.exists() else {'commit':Head,'operations':[]}
require(Done['commit']==Head,'Mismatched publication retry')
def run(args):
    Start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(['git',*args],cwd=R,capture_output=True,text=True)
    Row=dict(argv=p.args,cwd=str(R),start_utc=Start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
    Done['operations'].append(Row);Records.write_text(json.dumps(Done,ensure_ascii=False,indent=2)+'\n')
    require(p.returncode==0,'Git publication operation failed: '+repr(p.args)+' '+p.stderr)
    return p.stdout.strip()
for Remote in ['origin','fork']:
    Old=run(['ls-remote','--exit-code',Remote,'refs/heads/main']).split()
    require(Old in [[Baseline,'refs/heads/main'],[Head,'refs/heads/main']],'Remote advanced unexpectedly: '+Remote)
    if Old[0]!=Head:run(['push',Remote,'HEAD:refs/heads/main'])
    Now=run(['ls-remote','--exit-code',Remote,'refs/heads/main']).split();require(Now==[Head,'refs/heads/main'],'Remote post-state differs '+Remote)
    print(Remote+' main verified '+Head,flush=True)
