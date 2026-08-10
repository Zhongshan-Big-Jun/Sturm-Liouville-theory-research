# -*- coding: utf-8 -*-
import numpy as np
def W(u): return 3 + 2*u/np.tan(u)
def Wp(u): return 2*(np.sin(u)*np.cos(u)-u)/np.sin(u)**2
def N2(w): return W(w)**2 + W(w) + w*Wp(w)
for w in [2.7, 2.8, 2.856, 2.9, 3.0, 3.1, np.pi]:
    print(f'  w={w:.4f}: W={W(w):+.4f} Wp={Wp(w):+.4f} N2={N2(w):+.4f}')
print('scan:')
vals = [N2(w) for w in np.linspace(2*np.pi/3+1e-9, np.pi-1e-9, 5001)]
print('  max N2 =', max(vals), ' at w =', 2*np.pi/3+1e-9 + (np.pi-1e-9-2*np.pi/3-1e-9)*np.argmax(vals)/5000)
print('  min N2 =', min(vals))
