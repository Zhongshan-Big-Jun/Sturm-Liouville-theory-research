# Proof-obligation graph

## T0

- ID: `T0`
- Statement: For every integer `n>=1` and every `s>1`, `G_{n,s}` has exactly `2n` simple zeros in `(0,pi)`.
- Quantifiers: uniform in `n,s`.
- Depends on: `O1`, `O2`, `O3`, `O4`, `O5`.
- Evidence/status: PROVED and independently audited. Bound proof package: candidate sha256 `59b46fa2ee1e2d6a38ad4d386c936405ad96f4861db4509872c6160a0c6791b6`; audit sha256 `4c8831a11edbdcb70c4599ef818e96633c507d2feef58a91659953b000f1c92f`.
- Proof or citation: `candidate_proof.md`; certified by `subagents/SUB-AUDIT.md`.
- Known edge cases: endpoints are zeros but excluded; `y=pi/2` requires a no-zero check.
- Verifier notes: no finite computation can close this node.

## O1

- Statement: Derive a polynomial `Q` with `G(y)=sin(y)Q(cos y)`, including exact degree.
- Quantifiers: all `n>=1`, `s>1`, all real `y`.
- Depends on: determinant/trace calculation and Cayley-Hamilton.
- Evidence/status: PROVED in `candidate_proof.md`, Section 1; independently reproduced in `subagents/SUB-ALG.md` and `subagents/SUB-ADV.md`; final audit PASS.
- Known edge cases: Cayley-Hamilton formula must include `n=1` without an undefined convention.

## O2

- Statement: Prove the reduced scalar polynomial has the exact number of simple roots in the required interval.
- Quantifiers: all `n>=1`, `s>1`.
- Depends on: `O1`.
- Evidence/status: PROVED in `candidate_proof.md`, Section 2; independently reproduced by a distinct sign mesh in `subagents/SUB-ALG.md` and by Sturm shooting in `subagents/SUB-OSC.md`; final audit PASS.
- Known edge cases: endpoint signs and possible root at the vertex of the quadratic substitution.

## O3

- Statement: Lift scalar roots bijectively to exactly `2n` roots in `x in (-1,1)` and then to `y in (0,pi)`, preserving simplicity.
- Depends on: `O1`, `O2`.
- Evidence/status: PROVED in `candidate_proof.md`, Section 3; independently reproduced in `subagents/SUB-ALG.md` and adversarially attacked in `subagents/SUB-ADV.md`; final audit PASS.

## O4

- Statement: Audit `n=1`, `y=0`, `y=pi`, `y=pi/2`, and `s=1` separately; exclude endpoint zeros.
- Depends on: `O1` and direct matrix/trigonometric checks.
- Evidence/status: PROVED in `candidate_proof.md`, Section 4; all three subagents separately audited the named cases; final audit PASS.

## O5

- Statement: Independent first-time adversarial audit of the integrated proof returns `PASS` with empty critical-error and gap lists.
- Depends on: candidate closure of `O1`-`O4`.
- Evidence/status: PROVED. Independent first-time verifier returned `PASS` with empty critical-error and gap lists in `subagents/SUB-AUDIT.md`.
