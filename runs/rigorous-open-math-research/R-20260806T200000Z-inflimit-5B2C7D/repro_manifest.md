# Reproducibility manifest

Run: R-20260806T200000Z-inflimit-5B2C7D
Task: Q-20260806-inflimit-5B2C7D (INF R->infinity limit for D = lambda_2 -
lambda_1 over the symmetric well family [R,1,R]).

## Inputs and versions

| Item | Version/identifier | Path | Role |
|---|---|---|---|
| Task packet | 2026-08-06T20:00Z, DRAFT | agenda/task-packets/Q-20260806-inflimit-5B2C7D.md | problem context |
| Gap extremals doc | 2026-08-05 | docs/SL_gap_extremals.tex (+ .pdf) | numeric statement source |
| Original limit script | 2026-08-05 | scripts/op03_gap_inflimit.py | evidence |
| Manager re-check | 2026-08-06 | scripts/verify_inflimit.py | evidence |
| Prior-run limit scripts | 2026-08-05 | runs/rigorous-open-math-research/R-20260805T000000Z-gapn1-a1b2c3/agentC_inflim.py, agentC_inflim2.py | evidence |
| O1 reduction proof (context) | audited 2026-08-06 | runs/rigorous-open-math-research/R-20260806T151000Z-o1reaudit-5A1C3D/candidate_proof.md | context only |
| SL gap n=1 proof doc | 2026-08-06 | docs/SL_gap_n1_proof.tex (section 4) | context (machinery) |
| Tool-library leads | 2026-08-05 | tools/transfer-matrix-secular.md, tools/balanced-phase.md, tools/sturm-oscillation.md | leads only |

## Environment

- OS: Windows (PowerShell). Timezone Asia/Shanghai. Research date 2026-08-06.
- Python 3.10.11 at C:\Users\HuangZY\AppData\Local\Programs\Python\Python310\python.exe.
- numpy 2.2.6, scipy 1.15.3, sympy 1.13.1, mpmath 1.3.0.
- xelatex at D:\texlive\2024\bin\windows\xelatex.exe.
- Model/tool chain: codex CLI (model field unknown; recorded as UNKNOWN, not
  invented).
- Formal systems: none used (interval arithmetic performed with mpmath.mpf
  high precision and independent high-precision floats; see evidence scripts).

## Reproduced numeric claims (before proof work)

With the limiting system as stated in the packet:
  u* = 0.3299225081196866
  mu_1bar(u*) = 22.668138824360177
  mu_2bar(u*) = 47.61200496279252
  Dbar(u*) = 24.94386613843234
  3*pi^2 = 29.60881320326807
  ratio Dbar(u*)/(3 pi^2) = 0.8424473472539981
Matches the doc and both scripts to 1e-9 or better.  Evidence:
reproducibility/01_reproduce_claims.py.

## Restrictions and unknown fields

- Do not modify files outside RUN_ROOT (evidence scripts may be added under
  scripts/).
- Do not modify upstream run artifacts.
- Do not call manage-math-research-program from inside this solver run.
- Unknown: exact model identifier; effective wall-clock "8 hours" is the
  research effort target and cannot be independently verified in-process
  (recorded honestly).
- Internet access: enabled; search used for novelty and premise verification.

## Evidence scripts (this run)

All under reproducibility/ (see README inside that directory for the exact
commands and outputs):
  - 01_reproduce_claims.py        : reproduces the packet numerics.
  - 02_limiting_curve.py          : Dbar(u), S(u), Dbar'(u), sign structure.
  - 03_secular_convergence.py     : fixed-u convergence of mu_k(R,u).
  - 04_sliver_probe.py            : boundary sliver profiles (u->0, u->1/2).
  - 05_interval_value.py          : rigorous interval enclosure of Dbar(u*).
  - 06_symbolic_identities.py     : sympy verification of S = Dbar' and G.
  - 07_fixed_u_tables.py          : convergence rates and tables.
Every script records inputs, expected outputs, and a checksum of its own
source in its header; the run root manifest stores SHA-256 of each artifact.

## Script 19 v2 correction record (2026-08-07, session 30)

- v1 of 19_verify_lemma_A_doubleprime_chain.py used v = -cot t; the correct
  parameter is v = u/ell = -t cot t (from tan t = -t ell/u).
- Because f(t) = 2t^4/(t^2+v^2+v) is decreasing in v >= 0, the v1 certificate
  (smaller v) remained a valid upper bound; the formula was wrong nonetheless.
- v2 (delivered, sha256 47E737FA...): certified f-max = 5.422510 on
  [3/sqrt(2), pi), ratio def2/def1 <= 0.825511 < 1, phase brackets ok,
  identity G-Dbar=(def1-def2)/u^2 holds to 1e-42 at 480 points.  PASS.
- The same correction is applied in docs/SL_gap_n1_inf_limit_proof.tex
  (Lemma 2.4) and tools/lemma-A-doubleprime.md.

## Certification outputs (scripts 16-19, re-run 2026-08-07)

- 16_certify_all_regions.py: PASS, 18.15 s.  Worst certified values per
  region: A 42723.99 (424460 cells), B 293.3558 (687915 cells), C 25.0594
  (sanity at wcap-1e-6; analytic min exactly 25), D 77.6670 (193241 cells).
  Tails: A coefficient 1678953 >= 25, B coefficient 1791.6 >= 25, D tail
  C*sqrt(1e8) = 1529.0 >= 25.
- 17_certify_medium_region.py: PASS, 61.0 s.  115185 cells, 9645 skipped
  (w < 2); worst corner bound 27.9874 >= 25 at (R, u) ~ (9.78e7, 0.2).
- 18_verify_lemma_A_doubleprime.py: PASS.  Fmax <= 0.835879 < 0.84;
  ratio def2/def1 <= 0.772379 < 1 (independent chain); grid 400 pts: UB <= LB
  everywhere, worst ratio 0.7686.
- 19_verify_lemma_A_doubleprime_chain.py: PASS, 7.9 s.  Phase brackets ok at
  4x61 points; f <= 2t^2 <= 9 on (pi/2, 3/sqrt(2)]; certified f <= 9 on
  [3/sqrt(2), pi) with worst cell bound 5.422510; ratio <= 0.825511 < 1;
  identity verified to 1e-42 on 480 points.

## Artifact hashes

| Item | File | sha256 | Role |
|---|---|---|---|
| Problem contract | problem_contract.md | 0C0B705BAE55798D9F2D578F4FE27D6347D26AC7D1E623B0AC17785BDAC45D7F | normalized contract |
| Candidate proof | candidate_proof.md | see run-manifest.json | deliverable summary |
| Obligation graph | obligation_graph.md | see run-manifest.json | T1/T2/T3 obligations |
| Approach registry | approach_registry.md | see run-manifest.json | routes/failures |
| Audit report | audit_report.md | see run-manifest.json | self-audit |
| Status/literature | status_and_literature.md | see run-manifest.json | premises/novelty |
| Research ledger | research_ledger.md | D71296925B497A0144A0CD9D3FAC63E1A5BF1AB6A8984474CC4D555DD2D2132F | R-001..R-021 |
| Formal proof | docs/SL_gap_n1_inf_limit_proof.tex | see run-manifest.json | 10-page PDF source |
| Formal proof PDF | docs/SL_gap_n1_inf_limit_proof.pdf | see run-manifest.json | deliverable |
| n=1 proof doc | docs/SL_gap_n1_proof.tex | see run-manifest.json | INF limit section |
| Overview doc | docs/SL_spectral_topics_summary.tex | see run-manifest.json | open-problem update |

Scripts 01-19 sha256 (reproducibility/):
01 84A399068A9B08AB0C65607DC44F5D21126E5DF3312F0FD2CB61F4BF716208FB
02 4FBFF8156036E365039BDFDFF77DF13944F81844DF933A5153D38BFA5C4D0826
03 14155BDAFE2C54A1DAA8FA1E6C13DE8E68FA53261DC0650A5417A0355D55460E
04 1E991D34161E749F824B969000DFA698894A08523D734DD51806CE9205063B08
05 C6CBAF39E9802E103E35DC6C0C508356C9BB1431863089A71F6675B4E242E5CE
06 A0F8A12D16D3DD6464EC17C7E11895B394E23A8F61BB295935E6D5383607EEFF
07 4EFB2B62963EEFC9BF1F5E84E81C41E28949EA4521D97D69043285AC9D37CF88
08 1864A64969796B1676D9B071F89472B8E9A71C11B992A53E57272014146B542B
09 01AE53BFE6B50FE1EED8C1B78218B66D558B3C84201C47D0CE054BE700D54EF5
10 454E481B8D84392118C953E10A75612878B3C7C6FA837147305AD77EB64CD256
11 864104DBAA364A1EAF22EBE21615B2258B6C4BA48215B15DD7F82F2B19FDB79F
12 40557C18FE15FCFFC8CB5B56DC5E47A0AF06C4B2E8267479E57D1C2C1488D77A
13 50786220D7AB0B5DFBD15C0B2FB2D125D2DFFEB746298FC4E2CAD2380D6400A1
14 34C32AD8BF8BC83DF14931FC53C77FAA37F547D84B6CEAD01F8333B0DE5E2B07
15 F14F77D5CA4DC9C403C9180BAB40895A27BBAD11A5000CA057898E9A7BCA204D
16 348E8A55E4FC593CBB4C3E8AC46ED93465982A1B06134575A2804475B5387EC1
17 80468EB0C4A78B161F2B696CF731D3D11666815005FA1FD83E4BD3A1A3E9DADF
18 27067BF8A379B53FA0C22161E7C9716BA2CC314B858820FE105B91BBE443B83B
19 47E737FA2B02C774F33995E850C3B4B0256B78EE014F811E0F8AB806AE0301C7

Probe/diagnostic scripts (probe_*.py, probe_debug*.py): diagnostic only, hashes
computed at finalize (see the file listing; not part of the proof chain).

## Reproduction commands

PYTHONUTF8=1; python reproducibility/<NN>_*.py from the run root.  All scripts
print their own sha256 in the header and are deterministic (fixed grids,
directed rounding).  Scripts 16-19 re-run on 2026-08-07 with the outputs
recorded above; scripts 01-15 were run during the research phase with PASS
(recorded in research_ledger.md R-001..R-021).

## Restrictions and unknown fields

- model identifier: unknown (recorded honestly, not invented).
- The effective 8-hour research target is tracked by the manager in
  state/current.json; the model cannot independently verify wall-clock time.
- mpmath.iv is outward-rounded by design; independent directed-rounding
  Decimal engine cross-checks the load-bearing constants.
