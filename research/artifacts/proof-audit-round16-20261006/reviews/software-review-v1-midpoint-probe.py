from pathlib import Path
import hashlib
import json
import math
import sys
import mpmath as mp
import numpy as np

root=Path('F:/tools/math-audit-round16-20261006/software-review-v1/root')
sys.path.insert(0,str(root/'scripts'))
import _gapn2_second_variation_probe as V
import _gapn2_symmetry_recon as S

rows=[]
for left in (.125,.5,.875):
    right=math.nextafter(left,1.)
    length=right-left
    probe=V.SpectralProbe([(1.,1.)],4,64)
    direction=V.block_direction([0.,1/length,0.],[0.,left,right,1.])
    lam,cu,cw,diag,info=probe.pairings(direction,return_diagnostics=True)
    with mp.workdps(90):
        a,b,h=mp.mpf(left),mp.mpf(right),mp.mpf(1/length)
        ref=np.empty((4,4))
        norms=[]
        for wave in probe.roots:
            w=mp.mpf(float(wave))
            norms.append(mp.quad(lambda x:(mp.sin(w*x)/w)**2,[0,1]))
        for k,wave_k in enumerate(probe.roots):
            for l,wave_l in enumerate(probe.roots):
                wk,wl=mp.mpf(float(wave_k)),mp.mpf(float(wave_l))
                ref[k,l]=float(h*mp.quad(lambda x:(mp.sin(wk*x)/wk)*(mp.sin(wl*x)/wl)/mp.sqrt(norms[k]*norms[l]),[a,b]))
    # In-memory comparison only: anchor at the common cell's left endpoint.
    states=np.array([S.eigenfunction_states(probe.blocks,wave,[left])[0] for wave in probe.roots])
    waves=probe.roots
    phase=waves*(length/2)
    center=states[:,0]*np.cos(phase)+states[:,1]*(length/2)*np.sinc(phase/np.pi)
    slope=-states[:,0]*waves*np.sin(phase)+states[:,1]*np.cos(phase)
    cc,ss=V._cos_sin_integrals(waves,length)
    alternative=(np.outer(center,center)*cc+np.outer(slope,slope)*ss)/length
    rows.append(dict(left=left,right=right,length=length,
        density_origin_midpoint=float(left+length/2),midpoint_collapses=(left+length/2==left),
        result=cu.tolist(),reference=ref.tolist(),runtime_left_anchor_comparison=alternative.tolist(),
        max_absolute_error=float(np.max(np.abs(cu-ref))),
        cross_1_2=dict(actual=float(cu[0,1]),reference=float(ref[0,1]),left_anchor=float(alternative[0,1])),
        second_mode_diagonal=dict(actual=float(cu[1,1]),reference=float(ref[1,1]),left_anchor=float(alternative[1,1])),
        diagnostics=info))
out=Path('F:/tools/math-audit-round16-20261006/software-review-v1-midpoint-probe.json')
out.write_text(json.dumps(dict(rows=rows,source_sha256=hashlib.sha256(Path(V.__file__).read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8')
for row in rows:
    print(row['left'],row['midpoint_collapses'],row['cross_1_2'],row['second_mode_diagonal'])
