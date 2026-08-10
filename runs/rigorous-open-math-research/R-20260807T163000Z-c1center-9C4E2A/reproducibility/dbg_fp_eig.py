import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility"))
import numpy as np
from c1trace_lib import a_fp, R1R2
from fast_lib import sec, norm_n, roots2_fast

R = 1000.0; fp = a_fp(R); a, b = fp, 1-fp
s1, s2 = roots2_fast(a, b, R)
print("fp=%.8f a=%.8f b=%.8f s1=%.8f s2=%.8f" % (fp, a, b, s1, s2))
print("sec(s1)=%.3e sec(s2)=%.3e" % (sec(s1,a,b,R), sec(s2,a,b,R)))
n1 = norm_n(s1, a, b, R); n2 = norm_n(s2, a, b, R)
print("n1=%.6f n2=%.6f" % (n1, n2))
print("sin^2(s1 a)=%.6f sin^2(s2 a)=%.6f" % (np.sin(s1*a)**2, np.sin(s2*a)**2))
print("R1 = %.6e (should be 0)" % (np.sin(s1*a)**2/n1 - np.sin(s2*a)**2/n2))
# count sec roots in (0, 10)
s = np.linspace(1e-9, 10, 20001)
M = sec(s, a, b, R)
ch = np.signbit(M[1:]) != np.signbit(M[:-1])
idx = np.nonzero(ch)[0]
print("sec roots near:", [round(float(s[i]), 4) for i in idx[:10]])
