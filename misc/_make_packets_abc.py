# -*- coding: utf-8 -*-
import hashlib, json, io, os

ROOT = r"F:\LaTeX\BVE research"

def h6(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:6].upper()

def write_utf8(path, text):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def make_packet(task_id, run_id, task_type, title, reason, source, bundle_rows, related, leads, ambiguities, constraints, run_root):
    return """# Research task packet

- **Task ID**: @@TASK@@
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T14:00:00Z
- **Task type**: @@TYPE@@
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

@@REASON@@

## Authoritative problem source

@@SOURCE@@

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
@@BUNDLE@@

## Related paper analyses

@@RELATED@@

## Relevant tool-library leads

@@LEADS@@

## Known ambiguities and bibliographic risks

@@AMBIG@@

## User constraints and available resources

@@CONSTRAINTS@@

## Required run location

@@RUNROOT@@

## Upstream invocation

Use $rigorous-open-math-research on the concrete problem in this task packet. Treat this
packet as project context, not as a verified theorem contract. Independently normalize and
audit the exact statement, and recheck every theorem used as a premise against its original
source and exact version. Follow the upstream skill's own problem-level workflow and output
protocol. Write all standard artifacts under RUN_ROOT. Return the upstream result status
verbatim together with the run root and artifact locations. Do not call
manage-math-research-program from inside the solver run.

## Manager ingestion checklist

- [ ] Preserve upstream status verbatim.
- [ ] Index the run root and artifact paths/hashes.
- [ ] Do not copy or replace upstream standard artifacts.
- [ ] Update the portfolio, maps, tool candidates, budget, checkpoint, and resume entry.
- [ ] Promote reusable knowledge only from exact source or audited artifact locations.
""".replace("@@TASK@@", task_id).replace("@@TYPE@@", task_type).replace("@@REASON@@", reason)\
     .replace("@@SOURCE@@", source).replace("@@BUNDLE@@", bundle_rows).replace("@@RELATED@@", related)\
     .replace("@@LEADS@@", leads).replace("@@AMBIG@@", ambiguities).replace("@@CONSTRAINTS@@", constraints)\
     .replace("@@RUNROOT@@", run_root)

specs = []

# --- Task A: independent audit of KEY LEMMA candidate proof ---
t = "Q-20260806-keylemma-audit-" + h6("independent audit KEY LEMMA candidate proof 2026-08-06")
r = "R-20260806T140000Z-keylemmaaudit-" + h6("independent audit KEY LEMMA candidate proof 2026-08-06")
reason = """A candidate complete proof of the KEY LEMMA was produced by run
R-20260806T070000Z-keylemma2b-0A6D8F (status CANDIDATE_COMPLETE_PROOF: both (LOG) and (FP)
forms closed, obligations R1/R2/L4box/L5box closed). The run itself states that upgrading
the label to INDEPENDENTLY_AUDITED_PROOF requires a second independent entity audit or
formalization. This task is that independent audit: verify the candidate proof and its
certificates from scratch, without trusting the producing run. A passing audit upgrades the
program's O2 obligation to closed and unlocks the integrated proof document."""
source = """Audit target:
- runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/candidate_proof.md
- runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/audit_report.md
- runs/rigorous-open-math-research/R-20260806T070000Z-keylemma2b-0A6D8F/problem_contract.md
The claim: for all q > 1, c in (0, 1/2), (LOG) G1 - G2 < 0 and (FP) Ftilde' < 0 (definitions
in the contract), with obligations R1/R2/L4box/L5box and bases L1/L2/B4/B5 as stated.
Audit requirements: (i) re-derive or independently check every identity (E1-E9), base lemma
(B4, B5), the (q,u) reformulation, IN >= 0 iff G2 >= 0, M2 (dIN/du < 0), CORNER, C4, and the
box closure (L4box, L5box); (ii) independently re-verify the four interval certificates
(cert_dM2dq_boxes.json, cert_L4box_boxes.json, cert_L5box_boxes.json, cert_c4_boxes.json)
and the strip certificate (cert_dM2dq_strip_boxes.json) with your own engine; (iii) check
the non-load-bearing caveats (riarith.iv_sqrt rounding, C4 identity IN = A*K(v) not
symbolically zeroed) for hidden dependence; (iv) deliver a verdict per obligation."""
bundle = """| Candidate proof | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/candidate_proof.md | audit target | recheck everything |
| Contract | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/problem_contract.md | normalized statement | recheck |
| Self-audit | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/audit_report.md | producer's audit (do NOT trust) | recheck |
| Certificates | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/cert_*.json | enclosures to re-verify | independent re-verification required |
| Scripts | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/ | reproducibility materials | rerun |
| Parent run | 2026-08-06 | runs/.../R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md | origin of reduction and bases | recheck |
| Origin | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | definitions of G, H, F~ | recheck |"""
related = "No independent structured analysis exists beyond the run reports listed above."
leads = """- tools/key-lemma-decomposition.md (reduction update)
- tools/interval-ad-certificate.md (interval certificate pattern)
Leads only; do not treat as verified premises."""
ambig = """- Do not trust the producing run's self-audit; verify from first principles.
- The odd secular equation is q tan(alpha2) + tan(c alpha2) = 0 (product-of-tangents form is FALSE).
- C1 (audited): (LOG) and (FP) are not logically equivalent; both must be checked separately.
- Box endpoints: L4box/L5box on (1,2]x[0.4,0.5] must be handled with endpoints included or by one-sided limits.
- The certificate engines: riarith (Decimal) has a known non-strict iv_sqrt; all sign conclusions must be
  reproduced with a sound engine (e.g. mpmath.iv with outward rounding and your own transcendental routines)."""
constraints = """- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3, sympy, mpmath); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe.
- Deliver audit_report.md with per-obligation verdicts and overall status label per the upstream protocol.
- The audit must not modify the audited candidate proof; report gaps precisely."""
specs.append((t, r, "rigorously audit", reason, source, bundle, related, leads, ambig, constraints,
              "runs/rigorous-open-math-research/" + r + "/"))

# --- Task B: O3a corrected conjecture C1 ---
t = "Q-20260806-o3a-c1-" + h6("O3a corrected conjecture C1 h single zero 2026-08-06")
r = "R-20260806T140000Z-o3ac1-" + h6("O3a corrected conjecture C1 h single zero 2026-08-06")
reason = """Obligation O3a (uniqueness up to reflection of the sign-consistent critical point of D
over the barrier family) was reduced in a prior run to branch lemmas; Lemma A was then
strictly refuted by an interval certificate (R >= ~1350), so the old route is void. The run
proved P1-P4 and stated the corrected structural conjecture C1 (h = g1 - g2 has exactly one
zero on the common range, the symmetric fixed point), numerically supported for all tested
R in {1.02, ..., 1e6}. Proving C1 is the new route to O3a and completes the 2-parameter
extremum step of the n=1 gap theorem."""
source = """The statement to prove is C1 in:
- runs/rigorous-open-math-research/R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md,
  Section C1 (corrected structural conjecture; numerically supported, not proved).
Conjecture C1: for every R > 1, h = g1 - g2 has exactly one zero in the common range
I = [a0, beta], beta = min(a_max1(R), b0); the zero is the symmetric fixed point a_fp(R).
Equivalently, O3a holds.
Proved supporting facts (recheck): P1 (FH with eigenvalue factor), P2 (residual identity
dR1/db = -dR2/da), P3 (branch slope identity g1'*g2' = 1 at the symmetric fixed point and
Hessian reduction), P4 (R=1 base: v = cos(pi x), endpoints a0 = arccos(1/4)/pi,
b0 = arccos(-1/4)/pi).  Refuted: Lemma A (pointwise g1' > g2' on the whole common range),
counterexample certificate cert_ce1.py at (R,a*) = (1500, 0.57364) and (1e4, 0.57364)."""
bundle = """| O3a run candidate | 2026-08-06 | runs/.../R-20260806T011500Z-o3abranch-E8E56F/candidate_proof.md | C1 statement + P1-P4 | recheck |
| Counterexample log | 2026-08-06 | runs/.../R-20260806T011500Z-o3abranch-E8E56F/counterexample_log.md | CE-1 certificate (Lemma A refuted) | recheck |
| Audit report | 2026-08-06 | runs/.../R-20260806T011500Z-o3abranch-E8E56F/audit_report.md | gaps G2-G4 | recheck |
| Solver library | 2026-08-06 | runs/.../R-20260806T011500Z-o3abranch-E8E56F/reproducibility/clean_lib.py, agentB_lib.py | numerics | evidence only |
| Prior reduction | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentB_O3a_fixed_point.md | T1-T4 origin | recheck |"""
related = "No independent structured analysis beyond the run reports listed above."
leads = """- tools/fh-hessian-branch-reduction.md (P1-P3 reduction pattern)
- tools/interval-ad-certificate.md (certificate pattern used to refute Lemma A)
- tools/residual-exactness.md (T3 identity; note Lemma A refutation)
Leads only; do not treat as verified premises."""
ambig = """- Lemma A is FALSE for R >= ~1350; any route using it must be discarded.
- T is not a global contraction; contraction-type arguments are refuted.
- Multi-sheet structure: at R=1500, R2(a,b)=0 with v(b)<0 has three solutions; only the third
  is the principal sheet; Lemma C must be understood via the fixed-point-relevant principal sheet.
- The common range I = [a0, beta] has beta = min(a_max1(R), b0); check the definition in the source.
- Large-R pseudo-fixed-points are residual minima, not roots; absolute residual tolerance is unreliable."""
constraints = """- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- At least 8 hours of effective research time before concluding; failure routes recorded in the ledger.
- Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3, mpmath); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe.
- On success the integrated proof goes to docs/SL_gap_n1_proof.tex (manager compiles)."""
specs.append((t, r, "solve", reason, source, bundle, related, leads, ambig, constraints,
              "runs/rigorous-open-math-research/" + r + "/"))

# --- Task C: O1 revision + re-audit ---
t = "Q-20260806-o1-revise-" + h6("O1 reduction revision R1-R4 and re-audit 2026-08-06")
r = "R-20260806T140000Z-o1revise-" + h6("O1 reduction revision R1-R4 and re-audit 2026-08-06")
reason = """The O1 reduction theorem (SUP/INF over the box class equals SUP/INF over the
2-parameter barrier/well families) was independently audited: the statement is TRUE but the
draft proof is REPAIRABLE_GAP (O1a operator presentation defect; O1b FH sign error; repair
list R1-R4). This task repairs the draft per the audit, produces a revised O1 proof, and
self-audits the revision so the program can close obligation O1."""
source = """Repair and re-audit target:
- runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md (the draft)
- runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/audit_report.md (verdicts)
- runs/rigorous-open-math-research/R-20260806T011500Z-o1audit-422A69/candidate_proof.md (R1-R4 repair list)
Required repairs (recheck before use):
- R1/O1a: replace the T_rho self-adjointness argument by the symmetric Hilbert-Schmidt operator
  S_rho = rho^(1/2) T_rho rho^(1/2) with ||S_rho - S_sigma||_HS -> 0 and Weyl inequality;
- R2/O1b: correct the moving-jump derivative sign to dD/deps = -(c_+ - c_-) f(x_j) (rightward),
  +(c_+ - c_-) f(x_j) (leftward); the stationarity consequence f_N(x_j) = 0 is unchanged;
- R3: state the sign convention for u_2 explicitly in the Wronskian argument;
- R4: justify the moving-jump FH formula via approximation (Dirac measure limit).
Deliver a revised O1 proof (as candidate_proof.md in this run) and an audit_report.md that
verifies every obligation O1a-O1f in the revised text."""
bundle = """| O1 draft | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/O1_reduction_draft.md | repair target | recheck |
| O1 audit | 2026-08-06 | runs/.../R-20260806T011500Z-o1audit-422A69/audit_report.md | verdicts O1a-O1f | recheck |
| Repair list | 2026-08-06 | runs/.../R-20260806T011500Z-o1audit-422A69/candidate_proof.md | R1-R4 | recheck |
| Obligation graph | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/obligation_graph.md | O1 dependencies | recheck |
| AEH paper | arXiv:2407.02459 | papers/fundamental_gap.txt | Lemma 2.1-2.2 source | recheck against original |
| Keller/MW | DOI 10.1137/0131042, 10.1002/cpa.3160290505 | papers/keller1976.txt, papers/mw1976.txt | background | recheck |"""
related = "No independent structured analysis beyond the audit run listed above."
leads = """- tools/gap-n1-reduction.md (reduction pattern; status REPAIRABLE_GAP)
- tools/feynman-hellmann.md, tools/bang-bang.md (leads inside O1)
Leads only; do not treat as verified premises."""
ambig = """- The draft must NOT be silently upgraded: the revised proof must re-audit O1a-O1f line by line.
- O1a continuity: use S_rho = rho^(1/2) T_rho rho^(1/2); bound ||S_rho - S_sigma||_HS <= C(R)||rho-sigma||_1^{1/2}.
- O1b: the two-sided derivative exists only where f(x_j) = 0; state one-sided versions.
- Boundary cases (a=0, b=1, a=b, constants) must be covered by the closed-family parameterization."""
constraints = """- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3); xelatex at D:\\texlive\\2024\\bin\\windows\\xelatex.exe.
- Deliver revised candidate_proof.md + audit_report.md; numeric spot checks are evidence only."""
specs.append((t, r, "solve", reason, source, bundle, related, leads, ambig, constraints,
              "runs/rigorous-open-math-research/" + r + "/"))

# write packets + register + run roots
p = os.path.join(ROOT, "index", "task-packets.json")
with io.open(p, "r", encoding="utf-8-sig") as f:
    tp = json.load(f)

for (t, r, ttype, reason, source, bundle, related, leads, ambig, constraints, runroot) in specs:
    packet = make_packet(t, r, ttype, "SL gap n=1", reason, source, bundle, related, leads, ambig, constraints, runroot)
    write_utf8(os.path.join(ROOT, "agenda", "task-packets", t + ".md"), packet)
    tp["items"].append({"task_id": t, "path": "agenda/task-packets/" + t + ".md",
        "problem_id": "O-2026-SL-GAP-3B7A2C", "state": "READY",
        "run_id": r, "dispatched_at": "2026-08-06T14:00:00Z"})
    rr = os.path.join(ROOT, "runs", "rigorous-open-math-research", r)
    os.makedirs(rr, exist_ok=True)
    manifest = {"schema_version": 1, "run_id": r, "project_id": "MRP-20260731-BVE-SL",
        "task_id": t, "upstream_skill": "$rigorous-open-math-research",
        "upstream_skill_version_or_hash": "v2026-08-05 (changelog)",
        "started_at": "2026-08-06T14:00:00Z", "completed_at": None,
        "run_root": "runs/rigorous-open-math-research/" + r,
        "task_packet_path": "agenda/task-packets/" + t + ".md",
        "task_packet_sha256": None, "upstream_status_verbatim": None, "artifacts": [],
        "environment": {"model": None, "tools": ["Python 3.10", "xelatex"], "formal_systems": [],
            "unknown_fields": ["model"]},
        "manager_ingestion_state": "DISPATCHED", "missing_or_unavailable_artifacts": [],
        "notes": ["manager-created run root"]}
    write_utf8(os.path.join(rr, "run-manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    write_utf8(os.path.join(rr, "task-packet-link.txt"), "task packet: agenda/task-packets/" + t + ".md\n")
    print(t, "->", r)

tp["updated_at"] = "2026-08-06T14:00:00Z"
write_utf8(p, json.dumps(tp, ensure_ascii=False, indent=2) + "\n")
print("ALL PACKETS WRITTEN")