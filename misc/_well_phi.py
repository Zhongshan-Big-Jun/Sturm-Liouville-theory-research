# -*- coding: utf-8 -*-
"""Well-family Phi~ shape analysis (E3 evidence)."""
import numpy as np

def Phi(m, x):
	W = np.sin(x)**2 + m*m*np.cos(x)**2
	return x*np.cos(x)/np.sin(x)/W

def dPhi_num(m, x, h=1e-7):
	return (Phi(m, x+h) - Phi(m, x-h))/(2*h)

for m in [1.1, 1.5, 2.0, 3.0, 5.0]:
	xs = np.linspace(1e-6, np.pi-1e-6, 4001)
	vals = Phi(m, xs)
	d = dPhi_num(m, xs[100:-100])
	print(f"m={m}: Phi(0+)={Phi(m,1e-6):.6f} Phi(pi/4)={Phi(m, np.pi/4):.6f} Phi(pi/2)={Phi(m, np.pi/2-1e-9):.6f} Phi max={vals.max():.6f} at x={xs[vals.argmax()]:.4f}, dPhi min={d.min():.6f} max={d.max():.6f}")
	# count sign changes of dPhi
	sc = np.signbit(d[1:]) != np.signbit(d[:-1])
	print("   dPhi sign changes:", int(sc.sum()))
