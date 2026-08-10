import json, numpy as np
for R in [1500.0, 10000.0, 100000.0, 1e6]:
    d = json.load(open("runs/rigorous-open-math-research/R-20260807T163000Z-c1center-9C4E2A/reproducibility/e15_%g.json" % R))
    valid = [r for r in d["rows"] if np.isfinite(r[5])]
    print("=== R=%g: %d valid rows ===" % (R, len(valid)))
    # print hp at sample rows and sign changes
    signs = []
    for i, r in enumerate(valid):
        if i > 0 and valid[i-1][6]*r[6] < 0:
            signs.append(i)
    print("hp sign-change at row indices:", signs[:20])
    for i in sorted(set([0, len(valid)//8, len(valid)//4, 3*len(valid)//8, len(valid)//2, 5*len(valid)//8, 3*len(valid)//4, 7*len(valid)//8, len(valid)-1])):
        r = valid[i]
        print("  a=%.6f b=%.6f g1p=%.6f u=%.6f Phi=%.6f h=%+.8f hp=%+.8f" % tuple(r))
