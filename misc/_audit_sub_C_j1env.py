import mpmath as mp
mp.mp.dps = 50
print("sin(0.8976) =", mp.sin(mp.mpf('0.8976')))
print("0.78193  =", mp.mpf('0.78193'))
print("claim sin(8976/10000) <= 0.78193 :", mp.sin(mp.mpf('0.8976')) <= mp.mpf('0.78193'))
print("cos(0.13) =", mp.cos(mp.mpf('0.13')), " >= 0.99155:", mp.cos(mp.mpf('0.13')) >= mp.mpf('0.99155'))
print("cos(1.4596) =", mp.cos(mp.mpf('1.4596')), " >= 0.11047:", mp.cos(mp.mpf('1.4596')) >= mp.mpf('0.11047'))
# F'' lower bound
v = 4*(mp.mpf('0.485')*mp.cos(mp.mpf('0.13')) + mp.cos(mp.mpf('1.4596'))) - mp.mpf(356)/625*mp.mpf('0.78193')
print("F'' lower bound =", v, " > 3/2:", v > mp.mpf('1.5'))
# F and F' values
def F(x):
    return mp.mpf('0.89')*mp.sin(mp.mpf(4)*x/5) - (x - mp.mpf('0.356'))*mp.sin(2*x)
def Fp(x):
    return mp.mpf('0.89')*mp.mpf(4)/5*mp.cos(mp.mpf(4)*x/5) - mp.sin(2*x) - 2*(x-mp.mpf('0.356'))*mp.cos(2*x)
print("F'(24/25) =", Fp(mp.mpf('24')/25), " in (-1/20,0):", -mp.mpf('0.05') < Fp(mp.mpf('24')/25) < 0)
print("F'(97/100) =", Fp(mp.mpf('97')/100), " > 0:", Fp(mp.mpf('97')/100) > 0)
print("F(24/25) =", F(mp.mpf('24')/25), " >= 49/1000:", F(mp.mpf('24')/25) >= mp.mpf('49')/1000)
print("F(97/100) =", F(mp.mpf('97')/100), " >= 49/1000:", F(mp.mpf('97')/100) >= mp.mpf('49')/1000)
# u_c <= 89/100 check on [0.841, 1.1220]
def uc(x): return x*mp.sin(2*x)/(mp.sin(mp.mpf(4)*x/5) + mp.mpf('0.4')*mp.sin(2*x))
mx = None
for i in range(5001):
    x = mp.mpf('0.841') + (mp.mpf('1.1220')-mp.mpf('0.841'))*mp.mpf(i)/5000
    v = uc(x)
    mx = v if mx is None else max(mx, v)
print("max u_c on [0.841,1.1220]:", mx, " <= 0.89:", mx <= mp.mpf('0.89'))
