# Round 6 local formal algebra contract

Role: formalization AUTHOR. This package is not an independent final review or
approval. The submitted mathematical appendices are candidate evidence. The
coordinator owns AGENTS, reports, library propagation and Git operations.

## Exact target and mathematical meaning

Target: `SL.AuditRound6.local_algebra_root`, from
`lean-proof/SL/AuditRound6.lean`. The root has no assumed analytic theorem and no
extra mathematical hypotheses. Its concrete conjunction covers:

1. Over `Polynomial ℝ`, the linear span of `p_zero = 1`, `p_one = X`, both
   `p_even m` and `p_odd m` for every natural `m >= 2`, and `X^2,X^3` equals
   the top submodule. The sparse span without the two added monomials excludes
   `X^2`. All-index even and odd inductions, followed by polynomial induction,
   prove this; finite degree sampling is not used.
2. `four_traces` is an actual real linear map, ordered as
   `(B_+ p, B_- p, B_+ p'', B_- p'')`, where
   `B_+ p = p'(1) - (p(1)-p(-1))/2` and
   `B_- p = p'(-1) - (p(1)-p(-1))/2`.
   Its columns on `X^2,X^3,X^4,X^5` equal the displayed 4 by 4 `Matrix`.
   The determinant is 15360. The explicit inverse multiplies to the identity
   on both sides. The polynomial-valued linear map `four_trace_lift` is a
   right inverse, and subtracting this lift of the traces kills all four
   traces of every real polynomial.
3. The actual `p_even 3 - (7/2) • p_even 2` equals
   `X^6 - 5 X^4 + 7 X^2` and has four zero traces, while `p_even 2` has trace
   vector `(0,0,24,-24)` and hence nonzero four-trace vector.
4. In the actual inner product space `EuclideanSpace ℝ (Fin 2)`, take
   `v=(1,1)`, `w=(1,-1)`, `e0=(1,0)`, `e1=(0,1)`. The five inner products
   `<v,e0>=1`, `<v,e1>=1`, `<v,w>=0`, `<w,e0>=1`, `<w,e1>=-1` show why
   detecting both coordinates does not force them individually to vanish on
   the constraint kernel. This is a finite dimensional real counterexample.

The imported `SL.AuditRound5` source supplies the actual polynomial families,
derivative/evaluation maps and Krein residuals. It must be recompiled from
unchanged source into each final verification's fresh output directory.

## Excluded claims

This file does not establish complex polynomial statements by a scalar-field
shortcut. It does not formalize the weighted infinite-series counterexample,
Sobolev spaces, continuity of traces on Sobolev spaces, graph cores, spectral
coefficient asymptotics, fractional powers, the threshold 7/2, convergence,
topological density, or the full analytic appendices. Zero polynomial traces
are not identified here with membership in any unbounded operator domain.

The optional general Hilbert-space projection/orthogonal-complement identity
and the finite-dimensional tail-obstacle injection theorem are not advertised
as established. No renamed Boolean or assumed density conclusion stands in
for those missing results. The sparse-span equality with the full Krein
polynomial kernel is also outside the root's advertised scope.

## Evidence and independent handoff

The actual pinned runtime is Windows PE Lean 4.31.0 called through WSL.
Package objects come from the pinned Mathlib warm cache. Old project-local
objects are excluded from LEAN_PATH. No old Lean source, configuration, object,
canonical file, plugin source, or plugin cache is to be changed. Python runs
use `-B` / `PYTHONDONTWRITEBYTECODE=1` to avoid writing plugin bytecode caches.

One maintained-verifier extraction of the exact compound root is the shared
dependency/module inventory. A compact author probe records every public
declaration's elaborated type and axiom closure, together with reachable local
definitions. This avoids a full environment dump per public theorem.

For later blind readback, give only the actual elaborated root/public types,
the reachable local definitions and the preserved `AuditRound5` source,
without this intended-meaning text or author verdict. For a semantic/execution
review, add this contract, the two exact candidate appendices, source/runtime/
pin/module hashes, raw compiler logs, maintained-verifier receipts and replay
entrypoint. The latter explicitly requires comparison to the analytic source
and examination of the narrower real-algebra boundary.

A deliberately wrong expected root type must produce a target mismatch, and
the correct fixed expected type plus a compiling positive control must pass.
Author results and future independent results remain separate.

Execution status and final source identity are recorded in `REPORT.md` and
`RESULTS.json` after actual completion, not inferred from this contract.
