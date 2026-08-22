# Problem Contract: B3 fixed-n ratio supremum

## Normalized statement

For R > 1, let K_R = {ρ in L^∞(0,1): 1 ≤ ρ ≤ R a.e.}. Consider the Dirichlet string
problem

    -y'' = λ ρ(x) y,   y(0)=y(1)=0.

Write 0 < λ_1(ρ) < λ_2(ρ) < ... for the eigenvalues. For each integer n ≥ 1 define

    Λ_n^sup(R) = sup_{ρ in K_R} λ_{n+1}(ρ) / λ_n(ρ).

Conjecture (project, numerical): Λ_n^sup(R) is attained by the alternating
bang-bang configuration

    ρ = [1, R, 1, R, ..., 1]        (2n+1 blocks),
    w_1 / w_2 = sqrt(R),            w_2 = t = 1/((n+1) sqrt(R) + n),

and

    Λ_n^sup(R) = c_n(R) = ((π - y_n)/y_n)^2,

where y_n is the n-th balanced-phase root of the alternating secular polynomial
F_n(y).

## Completion criteria

1. Prove a Keller-type variational reduction showing every fixed-n maximizer can
   be taken from the alternating bang-bang family [1,R,1,...,1].
2. Inside the alternating family, prove λ_{n+1}/λ_n is maximized at the width
   ratio w_1/w_2 = sqrt(R) (and that the balanced-phase root y_n gives the
   maximum).
3. Prove the alternating secular polynomial F_n(y) (or Q_n(cos y)) has exactly
   2n roots in (0,π) for every n ≥ 1 and R > 1.

## Status conventions

- STRICT means a proof obligation is closed in the mathematical sense.
- Numerical evidence is not proof; it is labelled EVIDENCE.
- Open obligations are labelled OPEN.

## Pre-scan protocol (REUSE-GATE)

Every attempted route is first checked against research_map.md, tools/,
lean-proof/LEMMA_INDEX.md, scripts/op02_*.py, and prior runs. Hits are recorded as
REUSE: <slug/path>; misses as REUSE_MISS: <description>.
