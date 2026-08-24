# Problem contract

## Objects and definitions
- n >= 1 integer, R > 1 real, s = sqrt(R) > 1, alpha = 1/s in (0,1).
- For y in R, c=cos(y), q=sin(y).
- E(y)=[[c,q],[-q,c]], C_s(y)=[[c^2-s^(-1)q^2,(1+s^(-1))cq],[-(1+s)cq,c^2-s q^2]].
- M_{n,s}(y)=E(y) C_s(y)^n, G_{n,s}(y)=(M_{n,s}(y))_{12}.

## Hypotheses
- n >= 1, R > 1 (so s>1, alpha in (0,1)).
- Open interval y in (0,pi).

## Target conclusion
- G_{n,s} has exactly 2n zeros in (0,pi), all simple.
- Endpoint zeros at y=0 and y=pi are not counted.

## Quantifier and dependency
- The bound 2n depends only on n; simplicity holds uniformly for all R>1.

## Equivalent formulation to be proved equivalent
- Start with G(y)=sin(y) P_n(z(y)), where z(y)=((s+1/s+2)cos^2(y)-(s+1/s))/2 and
  P_n(z)=U_n(z)+(1/s) U_{n-1}(z), U_k Chebyshev second kind.
- Then P_n has exactly n distinct real roots in (-1,1), all simple.
- Because y->z is two-to-one from (0,pi) onto (-(s+1/s)/2,1) with derivative nonzero
  at all preimages of roots, the claim follows.

## Boundary and degenerate cases
- y=0: c=1,q=0 => C_s=I, E=I, M=I, G=0 (endpoint, not counted).
- y=pi: c=-1,q=0 => C_s=I, E=-I, M=-I, G=0 (endpoint, not counted).
- y=pi/2: c=0,q=1 => z=-(s+1/s)/2 < -1; P_n has no root there because all its
  roots lie in (-1,1). Thus G != 0 at pi/2.
- R=1 (s=1, alpha=1) is outside the stated hypothesis; the same proof formula gives
  G=sin((2n+1)y), hence exactly 2n simple zeros in (0,pi). Thus the conclusion also
  holds on the boundary.

## Permitted outcomes
- affirmative proof; negative proof/counterexample; exact obstruction or partial theorem.
- This run obtains an affirmative proof.

## Completion criteria
- Uniform exact proof for every n>=1 and R>1 of count and simplicity.
- Formal verification is not required; an independent audit was not possible due to
  isolation ("do not spawn nested subagents"), so the status is candidate.

## Non-completion conditions
- Numerical scans do not complete the task.
- A degree or count argument only for finitely many n does not complete.
- Any proof relying on an external theorem without stated hypotheses is not complete.

## Forbidden moves
- Use of prior solution to this exact problem.
- Presenting numerical evidence as proof.
- Silent change of quantifiers or domain.

## Tool/context constraints
- Work only inside arm root; no internet/git/memory/prior-solution inspection.
- Scratch symbolic computation used only for checking, not as proof.
