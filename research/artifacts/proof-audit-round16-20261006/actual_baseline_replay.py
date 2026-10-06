"""Defect reproduction on frozen COMPLETE pre-edit sources, never live code.

A confirmed wrong result is evidence of the old bug, not repaired acceptance.
Unchanged sibling spectral/physical dependencies are checked against the
round16 baseline source snapshots. Outputs must use a new external path.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import numpy as np


def main():
	Parser=argparse.ArgumentParser();Parser.add_argument('--root',type=Path,required=True);Parser.add_argument('--output',type=Path,required=True);Args=Parser.parse_args()
	Work=Path(__file__).resolve().parent;Root=Args.root.resolve();Base=Work/'baseline_sources'
	for Rel in ('scripts/_sl_prufer.py','scripts/_sl_spectral_identity.py','scripts/_gapn2_symmetry_recon.py'):
		if (Base/Rel).read_bytes()!=(Root/Rel).read_bytes():
			raise RuntimeError('unchanged dependency mismatch: '+Rel)
	sys.path.insert(0,str(Root/'scripts'))
	def Load(Name,Rel):
		Spec=importlib.util.spec_from_file_location(Name,Base/Rel);Module=importlib.util.module_from_spec(Spec);sys.modules[Name]=Module;Spec.loader.exec_module(Module);return Module
	T=Load('round16_baseline_rigid1d','misc/rigid1d.py');V=Load('round16_baseline_variation','scripts/_gapn2_second_variation_probe.py')
	Rows=[]
	def Observe(Name,Condition,**Data):
		Rows.append({'name':Name,'defect_confirmed':bool(Condition),**Data})
		if not Condition:
			raise RuntimeError(Name)
	f=lambda z:(z-z*z/2)/15-F(1,2**62)*z
	Observe('integer endpoint false True',T.der_sign2(f,0,1,True,base_n=3,max_n=3)[0],right_derivative=str(-F(1,2**62)))
	Observe('Fraction same false statement rejected',not T.der_sign2(f,F(0),F(1),True,base_n=3,max_n=3)[0])
	f=lambda z:(F(1)+F(3,2**54))*z-z*z/2
	for Fn in (T.der_sign2,T.der_sign_adaptive):
		Kw={'base_n':1,'max_n':1} if Fn==T.der_sign2 else {'max_boxes':40,'min_w':F(1,2**60)}
		Observe(Fn.__name__+' adjacent float false True',Fn(f,1.,math.nextafter(1.,2.),True,**Kw)[0],right_derivative=str(-F(1,2**54)))
	for Order,n in ((32,20),(64,60)):
		P=V.SpectralProbe([(1.,2.)],61,Order);Lam,C,W,D=P.pairings(lambda x:2*np.ones_like(x));Q=V.q_formula(Lam,C,W,n,D);Expected=(2*n+1)*math.pi**2/2
		Observe('old oscillatory error '+str((Order,n)),Q<0 if Order==32 else abs(Q/Expected-1)>1,Q=Q,expected=Expected,Gram_error=float(np.max(np.abs(C-np.eye(61)))),first_mode=float(Lam[0]),last_mode=float(Lam[-1]))
	for Order in (64,128):
		Delta=2.**-50;P=V.SpectralProbe([(.5,1.),(Delta,1.),(.5-Delta,1.)],3,Order);Direction=V.block_direction([0,1/Delta,0],P.edges)
		Points,Weights,_,_=P.quadrature();_,C,_,_=P.pairings(Direction);Cell=Points.reshape(3,Order)[1]
		Observe('old folded coordinates '+str(Order),len(np.unique(Cell))==9 and C[0,0]<1.9,mass=float(Weights@Direction(Points)),first_pairing=float(C[0,0]),unique_nodes=len(np.unique(Cell)),nodes_at_right=int(np.sum(Cell==.5+Delta)))
	P=V.SpectralProbe([(1.,2.)],61,64);Lam,C,W,D=P.pairings(lambda x:2*np.ones_like(x));Q=V.q_formula(Lam,C,W,2,D)
	Observe('old low-mode positive control',abs(Q-5*math.pi**2/2)<2e-7,Q=Q)
	Result={'meaning':'confirmed old defects and one surviving low-mode positive control; not post-repair tests','all_confirmed':all(R['defect_confirmed'] for R in Rows),'count':len(Rows),'checks':Rows,'optimization':sys.flags.optimize,'complete_source_hashes':{str(P.relative_to(Base)):hashlib.sha256(P.read_bytes()).hexdigest() for P in Base.rglob('*.py')}}
	Args.output.write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('CONFIRMED',len(Rows),'frozen complete-source observations')


if __name__=='__main__':
	main()
