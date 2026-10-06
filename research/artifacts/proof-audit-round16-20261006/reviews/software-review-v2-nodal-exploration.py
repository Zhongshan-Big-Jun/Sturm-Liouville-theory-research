from pathlib import Path
import sys, math, json
import numpy as np
import mpmath as mp
root=Path('F:/tools/math-audit-round16-20261006/software-review-v2/root')
sys.path.insert(0,str(root/'scripts'))
import _gapn2_second_variation_probe as V
mp.mp.dps=100
rows=[]
def mode_ref(blocks,w):
    w=mp.mpf(float(w));y=mp.mpf(0);v=mp.mpf(1);start=mp.mpf(0);parts=[];mass=mp.mpf(0)
    for lf,rf in blocks:
        l,r=mp.mpf(float(lf)),mp.mpf(float(rf));a=y;b=v/(w*mp.sqrt(r));k=w*mp.sqrt(r)
        mass+=r*mp.quad(lambda t:a* a*mp.cos(k*t)**2+2*a*b*mp.cos(k*t)*mp.sin(k*t)+b*b*mp.sin(k*t)**2,[0,l])
        parts.append((start,l,k,a,b));y=a*mp.cos(k*l)+b*mp.sin(k*l);v=k*(-a*mp.sin(k*l)+b*mp.cos(k*l));start+=l
    def sample(x):
        i=max(i for i,(s,*_) in enumerate(parts) if s<=x);s,l,k,a,b=parts[i]
        return (a*mp.cos(k*(x-s))+b*mp.sin(k*(x-s)))/mp.sqrt(mass)
    return sample
for blocks,left,idx in [([(1.,1.)],.5,1), ([(1.,1.)],.75,3), ([(1.,1.)],float(1/3),2), ([(.25,1.),(.5,4.),(.25,1.)],.5,1), ([(.5,1.),(2.**-50,4.),(.5-2.**-50,1.)],.5,1)]:
    p=V.SpectralProbe(blocks,6,8);right=math.nextafter(left,1.);delta=right-left
    _,cu,_,_,info=p.pairings(V.block_direction([0.,1/delta,0.],[0.,left,right,1.]),return_diagnostics=True)
    refs=[mode_ref(p.blocks,w) for w in p.roots]
    u=lambda i,t:refs[i](mp.mpf(left)+mp.mpf(delta)*t)
    cross=mp.quad(lambda t:u(0,t)*u(idx,t),[0,1]);square=mp.quad(lambda t:u(idx,t)**2,[0,1])
    rows.append(dict(blocks=blocks,left=left,right=right,delta=delta,index=idx+1,frequency=float(p.roots[idx]),cross_actual=float(cu[0,idx]),cross_ref=mp.nstr(cross,55),cross_absolute_error=mp.nstr(abs(mp.mpf(float(cu[0,idx]))-cross),30),square_actual=float(cu[idx,idx]),square_ref=mp.nstr(square,55),square_relative_error=mp.nstr(abs(mp.mpf(float(cu[idx,idx]))/square-1),30),info=info))
Path('F:/tools/math-audit-round16-20261006/software-review-v2-nodal-exploration.json').write_text(json.dumps(rows,indent=2,allow_nan=False),encoding='utf-8')
for r in rows: print(r['blocks'],r['left'],r['index'],r['cross_absolute_error'],r['square_relative_error'])
