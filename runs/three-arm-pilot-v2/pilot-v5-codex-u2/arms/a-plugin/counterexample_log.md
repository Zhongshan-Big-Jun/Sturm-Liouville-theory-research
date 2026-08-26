# Counterexample and edge-case log

- Mandatory cases queued: `t=0,1,2,3`; even/odd endpoint parity; one-point and two-point ranges; path extrema attained repeatedly; initial lamps at 0 and 2 forced zero.
- Fragile claim to attack: naive reflection coupling of bases alone couples endpoints but can leave different pre-meeting lamps. It is not accepted as a full-state coupling unless those residual lamps are rigorously erased or coupled.
- Fragile claim to attack: conditioning only on endpoint is insufficient for lamp laws; the range endpoints are also needed.
- Falsified: for fixed `t,R,e`, the exact both-boundaries count `H_t^R(A,e)` need not be unimodal in parity-spaced `A`; at `(t,R,e)=(6,4,2)` it is `[1,0,1]` for `A=0,2,4`.
- Falsified: the component whose first visited extreme is the upper boundary is not always increasing with its start. At `(t,R,e)=(30,6,0)` and `A=0,2,4,6`, its counts are `[0,4928259,7948612,7303360]`.
- Falsified route: reflection of bases until meeting at 1, followed by synchronous increments and even optimal conditional lamp coupling, has mismatch bounded below by a constant times `log(t)/sqrt(t)` for explicit large `t`; see hash-verified `subagents/direct_coupling.md`. The old lamps at harmonic-distributed pre-meeting depths cause the loss.
- Corrected local artifact error: recurrence (13) in `subagents/range_translation.md` misses transitions creating a new extreme. Minimal counterexample: `C_1(-1,0,-1)=1` from the single step `-1`, while that displayed RHS is zero. The correct forward update sends `(l,u,z)` to `(min(l,z-1),u,z-1)` and `(l,max(u,z+1),z+1)`.
- Falsified abstract shortcut: coordinatewise ordering of two coupled extrema triples does not imply `TV(joint)<=TV(LZ)+TV(UZ)` for general arrays; the desired comparison, if true, must use a simple-walk path invariant.
