# Research ledger

## 2026-08-27 — provenance and closure-first preflight

- Authoritative input: the frozen task in the current user request.  Blind restriction forbids
  internet and task-source lookup.  No literature status or novelty claim will be made.
- Workspace inventory before research: `plugin-skill.sha256`, `plugin-list.txt`,
  `events.jsonl`, `prompt.sha256`, `PROMPT.md`, `stderr.log`; none read for mathematical facts.
- Git probe: the current directory is not a Git repository, so there is no commit hash or
  dirty-tree state to preserve.
- Exact reduction `O1`: for `t>=1`, each visited vertex has at least one switch.  The final bit
  there is its last switch variable.  Distinct vertices have distinct last switch variables,
  all independent fair bits.  Unvisited lamps retain their forced initial zero.  Nearest-
  neighbour connectedness makes the visited set `[L_t,U_t]`.
- Exact lower-bound reduction `O2`: projecting to the base cannot increase TV.  Writing the
  number of `+1` increments as `K~Bin(t,1/2)`, translation of the start by two shifts `K` by
  one.  The TV distance between a unimodal lattice mass function and its unit shift telescopes
  to its maximum atom.  An explicit factorial inequality remains to be recorded.
- Coordinator direct upper-bound attempt: condition on `(L_t,U_t,S_t)`.  Agreement of these
  triples permits identical conditional lamps, so the triple-law TV is a valid upper bound.
  A reflection coupling of base walks starting at zero and two meets at site one, but equality
  of total ranges additionally requires the post-meeting walk to cover both pre-meeting
  extremes.  This is not yet quantified and may be too costly.  Thus the first exact gap is a
  full-state smoothing/coupling estimate, not the endpoint estimate.
- Cheapest falsification probe selected: exact dynamic programming for the translated triple
  law and, separately, the full state law at small `t`; this will test whether the range-triple
  comparison itself has `t^{-1/2}` scale and expose parity/small-time failures.  Computation is
  evidence only.
- Gate decision: `ESCALATE`, because direct range coupling and analytic kernel comparison are
  mechanism-distinct and can change whether `O3a` closes.

## 2026-08-27 — exact Tier 1 probe and route escalation

- Ran `python3 reproducibility/exact_small_cases.py --triple-max 80 --full-max 12` under
  CPython 3.14.4.  Arithmetic for probability numerators/denominators was exact integer
  arithmetic; displayed decimals alone used floating point.
- Triple TV values include `1` at `t=0,1,2`, `7/8` at `t=3,4`, and approximately
  `0.293458369254` at `t=80`; `sqrt(80)` times the latter is about `2.624771448870`.
- Full-state TV values include `3/4` at `t=1,2`, `21/32` at `t=3,4`, and exactly
  `68032659456/137438953472` at `t=12`, about `0.495002746582`.
- These finite checks support but do not prove the target scale.  They also confirm that the
  final lamps conceal range information, so equality with triple TV is false.
- Escalated to three mechanism-distinct proof routes per the explicit user request and the
  recorded `ESCALATE` gate.  Packets are in `subagents/packet_{a,b,c}.md`.

## 2026-08-27 — exact visible-hull and lower-bound lemmas

- Proved formula (3.1): a state's mass is a weighted sum over all enclosing exact base ranges,
  and depends on its lamp pattern only through the endpoint and outermost lit lamps.
- Consequently full-state TV equals visible-hull TV exactly, not just by an inequality.  This
  incorporates forced zeros outside the range and arbitrary zeros inside it.
- Proved the endpoint TV identity as the maximum atom of `Bin(t,1/2)` by unimodal telescoping.
- Gave a self-contained Markov/Chebyshev calculation yielding the uniform explicit lower bound
  `1/(4 sqrt(t))` for every integer `t>=1`.
- Durable delta: `O2` is closed locally and `O1b` is a new exact reduction.  Both await the
  independent package audit.

## 2026-08-27 — hard-limit continuation and route ingestion

- Continuation restrictions: preserve the frozen contract and all artifacts; read only this
  directory and installed plugin cache; no internet, new subagent, Route B retry, or new wave.
- Recomputed `sha256sum` before ingestion.  Route A matched its reported full hash
  `6ce207738f66fcd3b0b5b2c39175cf068be15f8b8532b76593e11b5cd386b647`.
  Route C matched
  `f260fe18d316ad8d58294700ad4bb3cd40514537728a7ac67ae576c19ca7bbf2`.
- No `subagents/route_b.md` exists.  Route B is recorded as INCOMPLETE_RETURN; no claim or
  failure mechanism is inferred from absence.
- Route A's supported result: for `t>=2`, (5.1) gives an explicit full-state
  `O(log(t)/sqrt(t))` upper bound.  Its Section 4 lower-bounds only that coupling's mismatch,
  not total variation; this distinction is retained.
- Route C's supported results: exact state-mass formula, exact normalized-range triple-TV
  identity, an alternative logarithmic-loss bound, and the exact V-shaped counterexample to
  parity-class unimodality.  Its array bound (17) remains open and is used only as a sufficient
  future obligation.
- Independently replayed `python3 reproducibility/verify_route_claims.py`; it exactly verified
  the killed-count table `(26,16,26)` and literal `t=1` full-state TV `3/4`.
- Replayed the full-state exact enumerator through `t=12`; output matched the earlier ledger.
- Integrated strongest exact partial theorem (7.1) into `candidate_proof.md`.  The fixed-
  constant upper bound `O3` remains open.
