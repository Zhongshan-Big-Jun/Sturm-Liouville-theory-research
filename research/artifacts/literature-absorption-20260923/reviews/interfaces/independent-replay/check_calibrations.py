"""Author checks only: direct matrices, Laurent coefficients, exact calibrations.
No project imports or writes. Print JSON for the execution harness to retain.
"""
import sys, json, platform
import mpmath as mp
import sympy as sp
mp.mp.dps = 70
Checks = []

def serial(Value):
	if isinstance(Value, (mp.mpf, mp.mpc)):
		return str(Value)
	if isinstance(Value, dict):
		return {Key:serial(Val) for Key,Val in Value.items()}
	if isinstance(Value, (list,tuple)):
		return [serial(Val) for Val in Value]
	return Value

def equal(Name, Actual, Expected, Tolerance=mp.mpf('1e-55')):
	Error=abs(Actual-Expected)
	Passed=Error <= Tolerance*(1+abs(Expected))
	Checks.append({'name':Name,'actual':str(Actual),'expected':str(Expected),'absolute_error':str(Error),'relative_scale_tolerance':str(Tolerance),'passed':bool(Passed)})
	return Passed

def condition(Name, Passed, Detail):
	Checks.append({'name':Name,'passed':bool(Passed),'detail':serial(Detail)})

def transfer(Lambda, Width, Density):
	W=mp.sqrt(Lambda*Density)
	C=mp.cos(W*Width)
	S=mp.sin(W*Width)
	return mp.matrix([[C,S/W],[-W*S,C]])

def secular(Lambda, Edge, Left=mp.mpf(1), Right=mp.mpf(4)):
	return (transfer(Lambda,1-Edge,Right)*transfer(Lambda,Edge,Left))[0,1]

def physical_root(Guess, Edge):
	return mp.findroot(lambda Value:secular(Value,Edge),(Guess*mp.mpf('.995'),Guess*mp.mpf('1.005')),tol=mp.mpf('1e-65'))

def mode_data(Lambda, Edge):
	W=mp.sqrt(Lambda)
	Y=mp.sin(W*Edge)/W
	Yprime=mp.cos(W*Edge)
	LeftNorm=mp.quad(lambda X:(mp.sin(W*X)/W)**2,[0,Edge])
	RightNorm=4*mp.quad(lambda X:(Y*mp.cos(2*W*X)+Yprime*mp.sin(2*W*X)/(2*W))**2,[0,1-Edge])
	Norm=LeftNorm+RightNorm
	Fz=mp.diff(lambda Z:secular(Z,Edge),Lambda)
	Fzz=mp.diff(lambda Z:secular(Z,Edge),Lambda,2)
	Numerator=lambda Z:mp.sin(mp.sqrt(Z)*Edge)/mp.sqrt(Z)*mp.sin(2*mp.sqrt(Z)*(1-Edge))/(2*mp.sqrt(Z))
	P=Numerator(Lambda)
	Pz=mp.diff(Numerator,Lambda)
	G=Pz/Fz-P*Fzz/(2*Fz**2)
	U=Y/mp.sqrt(Norm)
	Up=Yprime/mp.sqrt(Norm)
	Fa=mp.diff(lambda A:secular(Lambda,A),Edge)
	Faa=mp.diff(lambda A:secular(Lambda,A),Edge,2)
	Fza=mp.diff(lambda A:mp.diff(lambda Z:secular(Z,A),Lambda),Edge)
	First=-Fa/Fz
	Second=-(Faa+2*Fza*First+Fzz*First**2)/Fz
	Jump=mp.mpf(3)
	DensityHessian=2*Lambda*Jump**2*U**4-2*Lambda**2*Jump**2*U**2*G
	Geometric=2*Lambda*Jump*U*Up
	return {'lambda':Lambda,'norm':Norm,'u':U,'up':Up,'G':G,'first_transfer':First,'second_transfer':Second,'density_hessian':DensityHessian,'geometric':Geometric,'residue':P/Fz}

# An independent symbolic identity fixes the physical secular convention.
Omega,Edge=sp.symbols('omega edge', positive=True, real=True)
Physical=(sp.sin(Omega*Edge)*sp.cos(2*Omega*(1-Edge))+sp.cos(Omega*Edge)*sp.sin(2*Omega*(1-Edge))/2)/Omega
Trig=(3*sp.sin((2-Edge)*Omega)+sp.sin((3*Edge-2)*Omega))/(4*Omega)
condition('symbolic physical matrix secular equals trigonometric form',sp.trigsimp(sp.expand_trig(Physical-Trig))==0,{'identity':'F=(3 sin((2-a)omega)+sin((3a-2)omega))/(4 omega)'})

Base=mp.mpf('0.5')
Theta=mp.acos(1/mp.sqrt(3))
Modes=[]
for Index,T in enumerate([Theta,mp.pi-Theta],start=1):
	W=2*T
	Lambda=W**2
	Data=mode_data(Lambda,Base)
	Modes.append(Data)
	Prefix=f'single-interface k={Index}'
	equal(Prefix+' exact root',secular(Lambda,Base),0)
	equal(Prefix+' integrated normalization',Data['norm'],1/Lambda)
	equal(Prefix+' residue weighted norm',Data['residue'],-Data['u']**2)
	equal(Prefix+' Laurent finite part',Data['G'],1/(6*Lambda)+mp.tan(T)/(24*W))
	equal(Prefix+' FH sign',Data['first_transfer'],Lambda*3*Data['u']**2)
	equal(Prefix+' exact first derivative',Data['first_transfer'],2*Lambda)
	equal(Prefix+' exact second derivative',Data['second_transfer'],6*Lambda+mp.mpf('1.5')*W**3*mp.tan(T))
	equal(Prefix+' complete interface chain rule',Data['second_transfer'],Data['density_hessian']+Data['geometric'])
	condition(Prefix+' omit acceleration is rejected',abs(Data['second_transfer']-Data['density_hessian'])>1,{'omission_error':abs(Data['geometric'])})

Velocity=mp.mpf(2)/5
Acceleration=-mp.mpf(1)/7
for Index,Data in enumerate(Modes,start=1):
	Lambda=Data['lambda']
	U=Data['u']
	Up=Data['up']
	A=-3*Velocity*U**2
	B=-3*(2*Velocity**2*U*Up+Acceleration*U**2)
	Energy=9*Velocity**2*U**2*Data['G']
	Predicted=2*Lambda*A**2-2*Lambda**2*Energy-Lambda*B
	Expected=Data['second_transfer']*Velocity**2+Data['first_transfer']*Acceleration
	equal(f'curved path k={Index} full acceleration',Predicted,Expected)
	Rows=[]
	for Step in [mp.mpf('0.001'),mp.mpf('0.0005'),mp.mpf('0.00025')]:
		Positive=physical_root(Lambda,Base+Velocity*Step+Acceleration*Step**2/2)
		Negative=physical_root(Lambda,Base-Velocity*Step+Acceleration*Step**2/2)
		FD=(Positive+Negative-2*Lambda)/Step**2
		Rows.append({'step':Step,'finite_difference':FD,'expected':Expected,'error':abs(FD-Expected)})
	condition(f'curved path k={Index} finite differences converge at order two',all(mp.mpf('3.8')<Rows[I]['error']/Rows[I+1]['error']<mp.mpf('4.2') for I in range(2)),Rows)
	Data['curved_path_second']=Expected
	Data['finite_differences']=Rows

GapSecond=Modes[1]['curved_path_second']-Modes[0]['curved_path_second']
HalfGap=GapSecond/2
equal('half-gap convention',2*HalfGap,GapSecond)
condition('using full gap as Q is rejected',abs(HalfGap-GapSecond)>1,{'Q':HalfGap,'D_second':GapSecond})

# Scaling the complete density has a nonzero normalized eigenfunction derivative.
for Index in [1,2,3]:
	Lambda=(Index*mp.pi)**2/mp.mpf(3)
	equal(f'constant density scaling k={Index} second',mp.diff(lambda T:Lambda/(1+T),0,2),2*Lambda)
	equal(f'constant density scaling k={Index} normalized kernel component',mp.diff(lambda T:1/mp.sqrt(1+T),0),-mp.mpf('0.5'))
condition('dropping normalization kernel component is rejected',mp.diff(lambda T:1/mp.sqrt(1+T),0)!=0,{'orthogonal_forcing':'zero','actual_coefficient':'-1/2'})

# A midpoint mass, separate from moving a finite jump.
def atom_secular(Lambda, Mass):
	Point=mp.matrix([[1,0],[-Lambda*Mass,1]])
	return (transfer(Lambda,mp.mpf('.5'),1)*Point*transfer(Lambda,mp.mpf('.5'),1))[0,1]

Atom=[]
for Index in [1,2]:
	Lambda=(Index*mp.pi)**2
	Fz=mp.diff(lambda Z:atom_secular(Z,0),Lambda)
	Fm=mp.diff(lambda Mass:atom_secular(Lambda,Mass),0)
	First=-Fm/Fz
	Fzz=mp.diff(lambda Z:atom_secular(Z,0),Lambda,2)
	Fzm=mp.diff(lambda Mass:mp.diff(lambda Z:atom_secular(Z,Mass),Lambda),0)
	Second=-(2*Fzm*First+Fzz*First**2)/Fz
	ExpectedFirst=-2*mp.pi**2 if Index==1 else mp.mpf(0)
	ExpectedSecond=6*mp.pi**2 if Index==1 else mp.mpf(0)
	equal(f'midpoint atomic mass k={Index} first',First,ExpectedFirst)
	equal(f'midpoint atomic mass k={Index} second',Second,ExpectedSecond)
	Atom.append({'index':Index,'first':First,'second':Second})
equal('midpoint atomic half gap', (Atom[1]['second']-Atom[0]['second'])/2,-3*mp.pi**2)

Mass=mp.mpf('0.2')
AtomicRoots=[mp.findroot(lambda Z:atom_secular(Z,Mass),(mp.pi**2*mp.mpf('.65'),mp.pi**2*mp.mpf('.85'))),4*mp.pi**2]
LayerRows=[]
for Epsilon in [mp.mpf('0.1'),mp.mpf('0.05'),mp.mpf('0.025'),mp.mpf('0.0125')]:
	def layer_secular(Z):
		return (transfer(Z,mp.mpf('.5')-Epsilon,1)*transfer(Z,2*Epsilon,1+Mass/(2*Epsilon))*transfer(Z,mp.mpf('.5')-Epsilon,1))[0,1]
	Roots=[mp.findroot(layer_secular,(Root*mp.mpf('.98'),Root*mp.mpf('1.02'))) for Root in AtomicRoots]
	LayerRows.append({'epsilon':Epsilon,'roots':Roots,'absolute_errors':[abs(Root-Target) for Root,Target in zip(Roots,AtomicRoots)]})
condition('finite layer midpoint atom eigenvalue convergence samples',all(LayerRows[I+1]['absolute_errors'][K]<LayerRows[I]['absolute_errors'][K] for I in range(3) for K in range(2)),LayerRows)
# Off-shell matrix limit, not just a root fitting test.
Offshell=[]
for Epsilon in [mp.mpf('0.01'),mp.mpf('0.001'),mp.mpf('0.0001')]:
	Z=mp.mpf('7.3')
	Layer=transfer(Z,2*Epsilon,1+Mass/(2*Epsilon))
	Target=mp.matrix([[1,0],[-Z*Mass,1]])
	Error=max(abs(Layer[I,J]-Target[I,J]) for I in range(2) for J in range(2))
	Offshell.append({'epsilon':Epsilon,'max_entry_error':Error})
condition('finite layer off-shell jump matrix convergence samples',all(Offshell[I+1]['max_entry_error']<Offshell[I]['max_entry_error']/8 for I in range(2)),Offshell)

Result={'status':'PASS' if all(Item['passed'] for Item in Checks) else 'FAIL', 'role':'author development evidence, not independent review', 'python':sys.version,'platform':platform.platform(),'mpmath_version':mp.__version__,'sympy_version':sp.__version__,'mp_dps':mp.mp.dps,'checks':Checks,'check_count':len(Checks),'single_interface':serial(Modes),'path':serial({'velocity':Velocity,'acceleration':Acceleration,'Q':HalfGap}),'atomic_mass':serial(Atom),'atomic_reference_roots':serial(AtomicRoots),'layer_samples':serial(LayerRows),'bounds':'High precision floating computations and symbolic finite identity only; not interval-certified roots, global signs, differentiability proof, or all parameter verification.'}
print(json.dumps(Result,ensure_ascii=False,indent=2))
sys.exit(0 if Result['status']=='PASS' else 1)
