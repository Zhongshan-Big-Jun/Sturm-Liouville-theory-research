# Pilot v4 independent blind reviews

Review method: each substantive candidate was sent to a fresh reviewer with only
the deidentified bundle (problem + candidate files). Public reports below include
arm identity for the results table; the reviewers themselves did not see arm labels.
Some non-candidates with no usable artifact are marked NO_ARTIFACT without a full
reviewer pass.

## A/U3 (U3 LICT_Z)
- Verdict: REPAIRABLE_GAP
- Score: 78/100 (correctness 30, contract 14, progress 15, calibration 9, citation 5, reproducibility 5)
- Summary: Correct high-level invariant-cycle strategy; main arc sound if structural facts hold. Load-bearing VAN2 strata description and proper-base-change justification are not rigorous as written; audit was self-audit only.
- Fatal issues: none; repairable.

## C/U3 (U3 LICT_Z)
- Verdict: PASS
- Score: 92/100 (correctness 38, contract 17, progress 15, calibration 9, citation 9, reproducibility 4)
- Summary: Faithful proof via Arapura–Greer–Zhang Theorem 3.1 with hypotheses checked; plus substantial residue route. Independent residue proof has a minor slicing gap, not fatal.
- Fatal issues: none.

## D/U3 (U3 LICT_Z)
- Verdict: PASS
- Score: 93/100 (correctness 38, contract 18, progress 15, calibration 8, citation 9, reproducibility 5)
- Summary: Correct quote of AGZ Theorem 3.1; identifies invariant submodule as ker(T-I); enough for the problem. Minor notation imprecision in optional recap.
- Fatal issues: none.

## B/U3 (U3 LICT_Z)
- Verdict: PASS
- Score: 86/100 (correctness 36, contract 17, progress 14, calibration 8, citation 7, reproducibility 4)
- Summary: Sound Wang-sequence/residue proof under standard semistable interpretation. Bertini slicing step terse; final_response.md is only a fragment.
- Fatal issues: none.

## C/U2 (U2 TV asymptotics)
- Verdict: WRONG_PROBLEM
- Score: 29/100 (correctness 6, contract 4, progress 2, calibration 6, citation 8, reproducibility 3)
- Summary: Proves a different reading: (0,2) interpreted as base 0 with lamp at 2 lit. Under canonical wreath notation (lamp config, base), (0,2) is base 2 with all lamps off; that case was not solved, and the candidate discarded it because no clean constant arises.
- Fatal issues: solves self-invented interpretation.

## C/U1 (U1 Batchelor)
- Verdict: PARTIAL_NOT_COMPLETE
- Score: 38/100 (correctness 10, contract 4, progress 8, calibration 7, citation 6, reproducibility 3)
- Summary: Strong literature reconnaissance (Huang–Xu and An–Xu) and a plausible strategy, but no blueprint/proof delivered. Cited all-time result has stronger hypotheses; matching-strength theorem gives only limsup.
- Fatal issues: no proof.

## E/U2 (U2 TV asymptotics)
- Verdict: PARTIAL_NOT_COMPLETE
- Score: 34/100 (correctness 5, contract 9, progress 7, calibration 5, citation 5, reproducibility 3)
- Summary: Good proof plan, exact identity, and target constants, but all lemma files are statements/obligations only; no proofs or verifier results. Reflection-range hypothesis and coupling reduction have likely gaps.
- Fatal issues: no proof of asymptotic.

## E/U1 (U1 Batchelor)
- Verdict: PARTIAL_NOT_COMPLETE
- Score: 36/100 (correctness 6, contract 5, progress 8, calibration 9, citation 5, reproducibility 3)
- Summary: Honest exploratory route map with Fourier-sector reduction, but central low-frequency-mass lemma left open; some route claims are dubious.
- Fatal issues: no proof.

## B/U1 (U1 Batchelor)
- Verdict: NO_ARTIFACT
- Score: 2/100 (correctness 0, contract 0, progress 0, calibration 2, citation 0, reproducibility 0)
- Summary: final_response is a 122-byte status note about a search; no theorem, proof, or citation.

## No usable artifact (NO_ARTIFACT, score 0)
- A/U1, A/U2, B/U2, D/U1, D/U2, E/U3
- These bundles contained only the problem statement (or a status file with no proof); no candidate result was produced.
