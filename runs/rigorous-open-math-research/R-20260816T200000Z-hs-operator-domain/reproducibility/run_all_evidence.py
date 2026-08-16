# run_all_evidence.py
# Consolidated EVIDENCE runner: executes all exact sympy checks that corroborate the
# STRICT claims in candidate_proof.md.  Each block prints key verdict lines.
# EVIDENCE only: finite exact checks, not proofs.

import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
scripts = [
    "boundary_facts.py",
    "domain_poly_span.py",
    "degree_structure.py",
    "genericity_check.py",
    "krein_sobolev_membership.py",
    "krein_sobolev_deficit_fixed.py",
    "odd_proof_data.py",
    "monotonicity_data.py",
]

for s in scripts:
    p = os.path.join(HERE, s)
    print("=" * 70)
    print("### %s" % s)
    print("=" * 70)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout)
    if r.returncode != 0:
        print("STDERR:", r.stderr)
    sys.stdout.flush()
print("=" * 70)
print("ALL EVIDENCE SCRIPTS COMPLETED")
