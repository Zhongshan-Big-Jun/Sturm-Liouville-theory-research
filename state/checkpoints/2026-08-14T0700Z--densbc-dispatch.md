# Checkpoint 2026-08-14T0700Z -- densbc-dispatch (general denseness criterion under boundary constraints)

## Completed
- User request: advance open problem "受一般边界条件约束的 Hilbert 空间中多项式稠密的充要条件"
  (summary §5.5 item 4); pipeline math-research-workflow loaded (session context).
- Git at dispatch: head 108aa25 pushed to parent + fork; dirty tree from another
  session only (AGENTS.md Qwen-VLM lines, _tmp_*.py, _xsoc1_work/); recorded.
- Gate: validate_pipeline.py 0 problems (6 advisory warnings, pre-existing).
- B0 novelty preflight recorded in packet (web sweeps 2026-08-14): arXiv 2101.11968
  (RKHS, polynomials and the classical moment problem); "Density questions in the
  classical theory of moments" (Ann. Inst. Fourier 31(3) 1981); Berg-Thill Zbl
  0744.44006; J. Approx. Theory 2002 (DOI 10.1016/s0021-9045(02)00019-9); eudml
  Sobolev density note.  Openness: no known published necessary-and-sufficient
  criterion for constrained-subspace polynomial density; H^s cases closed
  in-project.  Snapshot binding N/A (pre-v2.2 knowledge/); bound to git 108aa25.
- Packet written: agenda/task-packets/Q-20260814-densbc-3F8A2C.md (header fields,
  B0 section, 5-item hash-pinned source bundle, run location, upstream invocation,
  manager ingestion checklist, audit contract A1-A8).
- state/current.json updated (active task/run, next checkpoint pointer).
- Goal created: goal-1ed0a417-3ce1-417d-b5b3-09a0d2f5f629 (active).
- Solver dispatched: fresh background subagent 29aa5e2c-e6e9-43d1-bc44-37da7da376da,
  run root runs/rigorous-open-math-research/R-20260814T070000Z-densbc-3F8A2C/.

## Active
- Solver program: (1) general moment characterization for V = ∩ ker L_j / closed V
  (constrained moment problem); (2) sufficient criteria on V (beta<1 first-moment,
  jump-type); (3) diagonal-space complete classification conjecture: dense iff
  beta <= 3/2 OR constraints force M_2 = M_3 = 0; (4) constraint-kills-free-
  parameters mechanism (V = span{x^2,x^3}^\perp restores density for all beta);
  (5) literature deep-read with stable links only.
- After solver settles: adversarial audit (fresh subagent, audit contract A1-A8),
  then ingestion (run-manifest/tools/AGENTS.md session record/README/summary doc/
  RESUME/current.json), validate_pipeline gate, commit + push origin + fork.

## Blockers
- None known.

## Update 2026-08-14 21:00 (after solver delivery)
- Solver (29aa5e2c) delivered RIGOROUS_PARTIAL_RESULT (run-manifest 17:03, candidate_proof.md
  ~340 lines, 8 STRICT theorems A-H, 6 evidence scripts v1-v6 with exact rational checks,
  4 literature deep-reads recorded in status_and_literature.md).
- STRICT highlights: Theorem A master criterion (V ∩ Q^\perp = {0}); Theorem B/C
  constrained moment characterizations; Theorem D corrected constraints-restore-density
  ((i) all p_n in V + (ii) x^2,x^3 in V^\perp ⟹ dense for every beta, via M_{2m}=m·M_2
  recursion); Theorem E COMPLETE diagonal classification: dense iff (beta <= 3/2 AND R
  has no finite run) - recursion-graph/run analysis, Lemma 4.1, finite-run characterization;
  Theorem F first-moment on V; Theorem G jump on V (conditional on project growth lemma);
  Theorem H boundary-functional interpretation.
- FALSIFIED (with mechanisms): packet conjecture V=span{x^2,x^3}^\perp dense for all beta
  (FALSE for beta>3/2: free params relocate to M_4/M_5, w with M_{2m}=(m/2)M_4 has norm
  tail Σ m^{2-2β}); proposed criterion "beta<=3/2 OR M_2=M_3=0" (FALSE: R={4} gives a
  finite singleton run at degree 2 with free M_2, finite-support w kills density at any
  beta).  Corollary: monomial family always dense in diagonal space (failure is an
  artifact of the sparse family).
- OPEN CORE: O1 general non-diagonal H exact low-moment-survival criterion; O2 general
  L_j expansion killing free params for all beta; O3 fractional window (inherited).
- Auditor dispatched: fresh subagent a79cd94f-3fba-4f5b-bbd5-48d49a9cc20c (contract
  A1-A10: statements, moment characterizations, Theorem D, diagonal classification +
  falsification re-derivation, Theorems F/G/H, open core, literature, labels, regression).
- Solver final-report turn queued (send_message) - awaiting its reply message.

## Recovery
- Packet: agenda/task-packets/Q-20260814-densbc-3F8A2C.md
- Base criteria: docs/SL_denseness_criteria.tex (Theorems 2/3/5/8/11)
- state/RESUME.md (P0/M3 state + P1 + Lean scheduling note)
