import sympy as sp, time
x, b, alpha = sp.symbols("x b alpha", real=True)
pi = sp.pi
def lam_prime(k):
    return -k**2*pi**2*((b-alpha) - (sp.sin(2*k*pi*b)-sp.sin(2*k*pi*alpha))/(2*k*pi))
def term1(xx, k, lp):
    return (lp/(k*pi))*(sp.sin(k*pi*xx)/(2*k*pi) - xx*sp.cos(k*pi*xx)/2)
def term2(xx, k, xp):
    return (sp.Rational(1,4))*(sp.sin(k*pi*(xx-2*alpha)) - sp.sin(k*pi*(xx-2*xp))) - (k*pi/2)*(xp-alpha)*sp.cos(k*pi*xx)
for k in (1,2):
    lp = lam_prime(k)
    t0=time.time(); J1 = sp.integrate(sp.sin(k*pi*x)*term1(x,k,lp),(x,0,1)); print("J1 k=%d: %.2fs"%(k,time.time()-t0))
    t0=time.time(); J2b = sp.integrate(sp.sin(k*pi*x)*term2(x,k,x),(x,alpha,b)); print("J2b k=%d: %.2fs"%(k,time.time()-t0))
    t0=time.time(); J2c = sp.integrate(sp.sin(k*pi*x)*term2(x,k,b),(x,b,1)); print("J2c k=%d: %.2fs"%(k,time.time()-t0))
    t0=time.time(); r = sp.expand(sp.expand_trig(sp.simplify(J2b+J2c))); print("expand k=%d: %.2fs"%(k,time.time()-t0))
