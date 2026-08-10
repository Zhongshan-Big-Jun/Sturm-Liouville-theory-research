# batch_e15.py - parallel e15 sweep
import json, subprocess, os, sys, time
from concurrent.futures import ProcessPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
py = r"C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe"
Rs = [1.02, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 4.0, 6.0, 10.0, 20.0, 50.0, 100.0, 200.0,
      500.0, 600.0, 700.0, 800.0, 850.0, 875.0, 884.0, 886.0, 888.0, 890.0, 895.0, 900.0,
      910.0, 920.0, 950.0, 1000.0, 1500.0, 2000.0, 5000.0, 10000.0, 100000.0, 1000000.0]

def run_one(R):
    f = os.path.join(HERE, "e15_%g.json" % R)
    t1 = time.time()
    r = subprocess.run([py, os.path.join(HERE, "e15_authoritative.py"), "--R", str(R), "--out", f, "--ngrid", "160"],
                       capture_output=True, text=True, encoding="utf-8", cwd=HERE)
    line = r.stdout.strip() or ("ERR " + r.stderr[-300:])
    return R, line, time.time()-t1

if __name__ == "__main__":
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=5) as ex:
        for R, line, dt in ex.map(run_one, Rs):
            print("R=%g [%.0fs] %s" % (R, dt, line), flush=True)
    # merge
    out = {}
    for R in Rs:
        f = os.path.join(HERE, "e15_%g.json" % R)
        if os.path.exists(f):
            with open(f, encoding="utf-8") as fh:
                out["R=%g" % R] = json.load(fh)
    with open(os.path.join(HERE, "e15_authoritative.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    print("DONE %d total %.0fs" % (len(out), time.time()-t0))
