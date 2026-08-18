# Research Ledger — R-20260816T210000Z-densbc-o1p

Task: DensBC O1' — concrete verifiable progress on a structured subclass.

## Chronological steps

1. Read upstream R-20260816T000000Z-densbc-o1 candidate_proof.md fully.
   Confirmed the reduced core O1': decide free run-base realizability
   (moment representability + membership in V).  Upstream Theorem 5 says
   full finiteness requires banded/diagonal moment structure.
2. Read upstream R-20260814T070000Z-densbc-3F8A2C candidate_proof.md for the
   audited Theorem E and F-densbc-01 corrected ratio
   M_k = (floor(k/2)/floor(L/2)) M_L.
3. Decided to target the structured subclass: H_beta (diagonal weighted l^2)
   with finite-degree polynomial Riesz representers / finite moment constraints.
   This specializes direction A and provides direction C examples.
4. Observed that for this subclass the representer moments are finitely
   supported, so the kept set N is cofinite and the run graph has finitely many
   components/free bases.
5. Derived the moment parameterization: V cap Q_sp^\perp is isomorphic to
   parameter vectors t satisfying the finite membership matrix equation Tt=0
   and the weighted l^2 norm condition Sum |t_b|^2 C_b(beta) < inf.
6. Classified C_b(beta): finite runs always admissible; infinite runs
   admissible iff beta > 3/2.
7. Obtained the main criterion: density iff ker(T|_{B_adm}) = {0}.  Checked
   that a linear combination of free bases is needed in general, not just
   individual zero columns.
8. Checked the coordinate reduction: Theorem 6 reproduces Theorem E
   (beta <= 3/2 AND no finite run).
9. Constructed Example 7: v_1 = x^4 + alpha x^6 (alpha real nonzero) gives a
   non-coordinate finite free-base obstruction for every beta.
10. Ran an independent adversarial subagent audit of candidate_proof.md.
    Verdict: REPAIRABLE_GAP.  Core sound; required fixing the complex
    conjugation in representer moments, the alpha convention in Example 7, the
    N index-set ambiguity, injectivity detail, and r=0 notation.
11. Repaired all audit issues in candidate_proof.md.  Re-verified changed
    points by inspection.
12. Wrote final artifacts (problem_contract, whiteboard, research_ledger,
    approach_registry, candidate_proof, run-manifest; plus audit_report).

## Decisions

- Did not attempt general O1' or arbitrary banded non-diagonal H in this pass;
  the chosen subclass is already a rigorous, checkable advance.
- Used no numerical evidence; all results are STRICT proofs.

## Failures / blocked routes

- Route "single zero column criterion is the whole answer" was identified as
  INSUFFICIENT during derivation: non-coordinate constraints can couple free
  bases, so a combination of nonzero columns can lie in the kernel.  The final
  theorem uses ker(T|_{B_adm}), which covers both cases.
- General banded non-diagonal O1' remains BLOCKED/PARTIAL (not attempted).

## Audit trail

- Independent auditor returned REPAIRABLE_GAP with 5 issues.
- All 5 issues fixed:
  1. a^{(j)}_k conjugate corrected.
  2. Example 7 alpha declared real.
  3. N index set ambiguity clarified.
  4. Injectivity and 0*inf convention clarified.
  5. r=0 zero-map notation clarified.
- A second independent audit (fresh subagent) returned REPAIRABLE_GAP with
  0 critical errors and 1 gap: Theorem 6 wording "every finite component
  contains at least one constrained degree" is false for the pinned singleton
  components {0}, {1} (they carry no free parameter).
- Fix applied: Theorem 6 now reads "every finite component that contains a free
  base contains at least one constrained degree"; Section 0 now states r finite
  explicitly.
- Final status: candidate_proof is STRICT on the stated subclass; both audits'
  findings are resolved.
