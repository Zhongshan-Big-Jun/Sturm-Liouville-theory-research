from pathlib import Path
import contextlib,hashlib,importlib.util,io,json,subprocess,sys,datetime
import numpy as np
D=Path(__file__).resolve().parent
P=D/'_gapn2_second_variation_probe.py'
Spec=importlib.util.spec_from_file_location('candidate',P);M=importlib.util.module_from_spec(Spec);Spec.loader.exec_module(M)
def require(C,Message):
	if not C:raise RuntimeError(Message)
def reject(F,Message):
	try:F()
	except ValueError as E:
		require('resolv' in str(E) or 'rounding' in str(E) or 'collapse' in str(E),Message+': wrong reason '+str(E));return str(E)
	raise RuntimeError(Message+': invalid geometry accepted')
Mode='optimized' if sys.flags.optimize else 'normal';Rows=[]
Blocks=((.29343444668877966,1.),(.20656555331122034,4.),(.5,1.))
Centers=np.cumsum([L for L,_ in Blocks])[:-1]
for W in [1e-20,1e-16,np.nextafter(0.,1.)]:
	Rows.append(dict(kind='unresolved-geometry',width=float(W),error=reject(lambda:M.checked_bump_breaks(Blocks,Centers,W,64),'narrow support')))
Breaks=M.checked_bump_breaks(Blocks,Centers,5e-4,64);X,Weights,_=M.quadrature_rule(Blocks,64,Breaks)
Masses=[float(np.sum(Weights*(np.abs(X-C)<5e-4)/(1e-3))) for C in Centers]
require(max(abs(X-1) for X in Masses)<2e-12,'default mass not preserved')
Rows.append(dict(kind='default-unit-masses',masses=Masses))
# Adjacent representable knots can contain no distinct interior quadrature nodes.
# The endpoint guard passes for this large bump; the actual node guard must reject.
C=.5;W=.01;Left=C-W;Gap=np.nextafter(Left,np.inf)-Left
TinyBlocks=((Left,1.),(Gap,2.),(1.-Left-Gap,1.))
Rows.append(dict(kind='unresolved-quadrature',error=reject(lambda:M.checked_bump_breaks(TinyBlocks,[C],W,64),'collapsed quadrature')))
for W in ['1e-20','1e-16']:
	Args=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(P),'2','4','sup','--bump-width',W]
	Start=datetime.datetime.now(datetime.timezone.utc).isoformat();Run=subprocess.run(Args,cwd=D,capture_output=True,text=True)
	Stem=D/(Mode+'-cli-width-'+W);Stem.with_suffix('.stdout.log').write_text(Run.stdout);Stem.with_suffix('.stderr.log').write_text(Run.stderr)
	require(Run.returncode==2 and 'resolv' in Run.stderr,'CLI did not reject unresolved bump')
	require('Q_linear_bump' not in Run.stdout,'CLI printed invalid P3 contribution')
	Rows.append(dict(kind='cli-rejection',width=W,argv=Args,start=Start,exit_code=Run.returncode,stdout=Stem.with_suffix('.stdout.log').name,stderr=Stem.with_suffix('.stderr.log').name))
Out=dict(status='PASS',mode=Mode,candidate_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),checks=Rows,scope='Author numerical resolution regression, not independent approval or rigorous quadrature bound')
(D/('f1-'+Mode+'.json')).write_text(json.dumps(Out,indent=2)+'\n')
print('PASS',Mode,len(Rows),'groups',Masses)
