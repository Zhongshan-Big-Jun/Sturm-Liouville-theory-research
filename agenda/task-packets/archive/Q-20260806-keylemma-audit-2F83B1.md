# Research task packet

- **Task ID**: Q-20260806-keylemma-audit-2F83B1
- **Project ID**: MRP-20260731-BVE-SL
- **Created**: 2026-08-06T14:00:00Z
- **Task type**: rigorously audit
- **Portfolio problem ID**: O-2026-SL-GAP-3B7A2C
- **Task state**: DRAFT

## Project reason for this task

A candidate complete proof of the KEY LEMMA was produced by run
R-20260806T070000Z-keylemma2b-0A6D8F (status CANDIDATE_COMPLETE_PROOF: both (LOG) and (FP)
forms closed, obligations R1/R2/L4box/L5box closed). The run itself states that upgrading
the label to INDEPENDENTLY_AUDITED_PROOF requires a second independent entity audit or
formalization. This task is that independent audit: verify the candidate proof and its
certificates from scratch, without trusting the producing run. A passing audit upgrades the
program's O2 obligation to closed and unlocks the integrated proof document.

## Authoritative problem source

Audit target:
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
symbolically zeroed) for hidden dependence; (iv) deliver a verdict per obligation.

## Source bundle

| Item | Version | Path | Role | Verification note |
|---|---|---|---|---|
| Candidate proof | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/candidate_proof.md | audit target | recheck everything |
| Contract | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/problem_contract.md | normalized statement | recheck |
| Self-audit | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/audit_report.md | producer's audit (do NOT trust) | recheck |
| Certificates | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/cert_*.json | enclosures to re-verify | independent re-verification required |
| Scripts | 2026-08-06 | runs/.../R-20260806T070000Z-keylemma2b-0A6D8F/reproducibility/ | reproducibility materials | rerun |
| Parent run | 2026-08-06 | runs/.../R-20260806T011500Z-keylemma-E58FB1/candidate_proof.md | origin of reduction and bases | recheck |
| Origin | 2026-08-05 | runs/.../R-20260805T000000Z-gapn1-a1b2c3/agentA_O2_single_crossing.md | definitions of G, H, F~ | recheck |

## Related paper analyses

No independent structured analysis exists beyond the run reports listed above.

## Relevant tool-library leads

- tools/key-lemma-decomposition.md (reduction update)
- tools/interval-ad-certificate.md (interval certificate pattern)
Leads only; do not treat as verified premises.

## Known ambiguities and bibliographic risks

- Do not trust the producing run's self-audit; verify from first principles.
- The odd secular equation is q tan(alpha2) + tan(c alpha2) = 0 (product-of-tangents form is FALSE).
- C1 (audited): (LOG) and (FP) are not logically equivalent; both must be checked separately.
- Box endpoints: L4box/L5box on (1,2]x[0.4,0.5] must be handled with endpoints included or by one-sided limits.
- The certificate engines: riarith (Decimal) has a known non-strict iv_sqrt; all sign conclusions must be
  reproduced with a sound engine (e.g. mpmath.iv with outward rounding and your own transcendental routines).

## User constraints and available resources

- Chinese final reporting; ASCII punctuation in all files; citations with clickable links.
- Environment: Python 3.10 (numpy 2.2.6, scipy 1.15.3, sympy, mpmath); xelatex at D:\texlive\2024\bin\windows\xelatex.exe.
- Deliver audit_report.md with per-obligation verdicts and overall status label per the upstream protocol.
- The audit must not modify the audited candidate proof; report gaps precisely.

## Required run location

runs/rigorous-open-math-research/R-20260806T140000Z-keylemmaaudit-2F83B1/

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
