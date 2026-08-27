# Counterexample and stress-test log

## Exact small cases

- Triple-law TV is exactly one for `t=0,1,2`, so any triple coupling threshold below three with
  `C<sqrt(2)` fails.  This does not refute a full-state bound.
- Full-state TV is `3/4` at `t=1,2`; parity does not make it one.
- Through `t=80`, `sqrt(t)` times triple TV rises from about `1.52` at `t=3` to about `2.62` at
  `t=80`; this warns against constants guessed from tiny times.
- Through `t=12`, `sqrt(t)` times full-state TV reaches about `1.715`.
- Exact numerators, denominators, and replay code are in
  `reproducibility/exact_small_cases.py` and the captured run in the research ledger.

## Fragile claims to attack

- A reflected meeting of base walks does not by itself equalize visited ranges.
- Conditional fair lamps do not make the range observable; zero boundary lamps hide parts of
  it.  Consequently triple-law TV is only an upper bound and need not equal full-state TV.
- A universal adjacent-start smoothing theorem for every symmetric Markov chain is false in
  general; any analytic route must exploit this chain's one-dimensional/lamp structure.
