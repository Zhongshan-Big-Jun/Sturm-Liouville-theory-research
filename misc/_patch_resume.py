# -*- coding: utf-8 -*-
import io
p = r"state\RESUME.md"
src = io.open(p, encoding="utf-8-sig").read()

old_obj = """## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF conjectured at symmetric [R,1,R].  HONEST STATUS (2026-08-10 audit): SUP side CLOSED
(O1 reduction, O2 KEY LEMMA, O3b bounds, O3a/C1 barrier-family uniqueness via phase-ratio
rigidity: for every R>1 exactly one sign-consistent good root in the BARRIER family,
necessarily symmetric a+b=1).  INF side: O1 reduction to the well family D^well(a,b) is
CLOSED; symmetric-well R->inf limit (Theorem A) is CANDIDATE_COMPLETE_PROOF; but the
WELL-FAMILY RIGIDITY (global inf over the full well family attained at the symmetric well
[R,1,R]) is OPEN (numerically supported only).  O3a/C1 does NOT cover the well family;
the barrier<->well identity D^well(a,b)=D^bar(1-b,1-a) is FALSE (R=4, a=0.2, b=0.8:
11.0482 vs 9.6580) - removed from docs."""
new_obj = """## Current objective
Prove (n=1): over 1<=rho<=R, SUP(lambda_2-lambda_1) attained by symmetric 3-block [1,R,1] at u*(R);
INF conjectured at symmetric [R,1,R].  HONEST STATUS (2026-08-10 session 51): SUP side CLOSED
(O1 reduction, O2 KEY LEMMA, O3b bounds, O3a/C1 barrier-family uniqueness via phase-ratio
rigidity).  INF side: O1 reduction to the well family D^well(a,b) is CLOSED; symmetric-well
R->inf limit (Theorem A) is CANDIDATE_COMPLETE_PROOF; WELL-FAMILY RIGIDITY small-R SOLVED:
theorem 2026-08-10 - for 1<R<=3/2 every sign-consistent good root of the well family is
symmetric a+b=1 (docs/SL_gap_n1_well_rigidity_R32.pdf, 11 pp zero warnings; phase-ratio
monotonicity Psi~'<0 via factorization + H>0 + tan(u/2) rationalization).  General R>3/2
rigidity OPEN: gaps (a) symmetric-line 1D analysis (f(v) unique zero, D(v) single peak),
(b) R>3/2 candidate route (prove N1=0 at good roots + N1<0 on off-axis E=0 branches),
(c) Theorem A independent re-verification CANDIDATE, (d) extremizer existence/good-root
condition partial.  O3a/C1 does NOT cover the well family; the barrier<->well identity
D^well(a,b)=D^bar(1-b,1-a) is FALSE (R=4, a=0.2, b=0.8: 11.0482 vs 9.6580) - removed."""
assert old_obj in src, "obj block"
src = src.replace(old_obj, new_obj)

old_read = """1. `docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf` (O3a complete proof, 40 pages, audited 2026-08-10 incl. Audit E replay + dual-subagent audit, F-210/F-211 fixed)"""
new_read = """1. `docs/SL_gap_n1_well_rigidity_R32.pdf` (INF well-family small-R rigidity theorem, 11 pp, 2026-08-10; gaps (a)-(d) registered; evidence log misc/_well_explore_log.md)
2. `docs/SL_gap_n1_O3a_phase_rigidity_proof.pdf` (O3a complete proof, 40 pages, audited 2026-08-10 incl. Audit E replay + dual-subagent audit, F-210/F-211 fixed)"""
assert old_read in src, "read block"
src = src.replace(old_read, new_read)

# renumber the following read-list entries 2..8 -> 3..9
for i in range(2, 9):
    old_line = f"{i}. "
    new_line = f"{i+1}. "
    # only the list items at the start of lines under "Read these files first"
    idx = src.find(old_read)
    seg = src[idx:]
    seg = seg.replace(f"\n{i}. ", f"\n{i+1}. ", 1)
    src = src[:idx] + seg
# fix the last item number 8 -> 9 handled above; verify

old_last = """## Last completed action
2026-08-10: audited and integrated the two user-provided n>=2 gap-extremal proofs"""
new_last = """## Last completed action
2026-08-10 (session 51): proved the INF-side well-family small-R phase-rigidity theorem
(1<R<=3/2, any sign-consistent good root is symmetric a+b=1; docs/SL_gap_n1_well_rigidity_R32.pdf,
11 pp zero warnings); closed the Sun 2022 class judgment (piecewise continuous with bounded
jumps, NOT our box class); created misc/_well_explore_log.md (all EVIDENCE with scripts and
precision), tools/well-family-rigidity.md, updated AGENTS.md (session 51), ledger R-112, and
this RESUME. Corrected the FH sign formula (dD/da=-(R-1)f(a), dD/db=+(R-1)f(b)).

Earlier (2026-08-10): audited and integrated the two user-provided n>=2 gap-extremal proofs"""
assert old_last in src, "last block"
src = src.replace(old_last, new_last)

old_next = """## Exact next action
1. Optional: independent verifier pass on INF-limit Lemma A'' chain (pending per skill policy).
2. Open problems remaining (per summary section 5.5): switch positions/block lengths,
   reflection symmetry, uniqueness/classification, closed-form optimal values max/min D_n,
   n=1 certificate kernel formalization, MDE unified theory, H^s density criteria,
   p-Laplacian, etc.
3. validate_project.py, budget settlement, stage summary on stage close."""
new_next = """## Exact next action
1. Gap (a): strict 1D proof on the symmetric line (f(v) unique zero, D(v) single peak,
   endpoint limits) - closes INF side for 1<R<=3/2 when combined with the small-R theorem.
2. Gap (b): R>3/2 well-family rigidity via candidate route (N1=0 at good roots identity
   + N1<0 on off-axis E=0 branches).
3. Gap (c): independent verifier pass on INF-limit Lemma A'' chain (pending per skill policy).
4. Open problems remaining (per summary section 5.5): switch positions/block lengths,
   reflection symmetry, uniqueness/classification, closed-form optimal values max/min D_n,
   n=1 certificate kernel formalization, MDE unified theory, H^s density criteria,
   p-Laplacian, etc.
5. validate_project.py, budget settlement, stage summary on stage close."""
assert old_next in src, "next block"
src = src.replace(old_next, new_next)

old_block = """## Blockers or missing inputs
- None blocking the SUP side.  The INF side well-family rigidity (n=1) is the remaining open obligation (2026-08-10)."""
new_block = """## Blockers or missing inputs
- None blocking the SUP side.  INF side: small-R (1<R<=3/2) well-family rigidity proven
  (2026-08-10); the remaining open obligations are the symmetric-line 1D analysis (gap a)
  and the general-R rigidity (gap b)."""
assert old_block in src, "blockers"
src = src.replace(old_block, new_block)

io.open(p, "w", encoding="utf-8", newline="\n").write(src)
print("RESUME.md updated")
