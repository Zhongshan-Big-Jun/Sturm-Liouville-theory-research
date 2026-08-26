# Reproducibility

All commands run from the repository-less workspace root, with Python 3.14.4.

- `python3 reproducibility/enumerate_triples.py 40` prints exact range-triple TV values for times 0 through 40.
- `python3 reproducibility/audit_exact.py 100` verifies the exact small-time table and probes AVI/MC on `0<=t<=100` using integer arithmetic.
- `python3 -m py_compile reproducibility/enumerate_triples.py reproducibility/audit_exact.py` checks script syntax.

There are no random seeds, floating-point decisions, network calls, or external data dependencies. The AVI/MC assertions in `audit_exact.py` are explicitly finite conjecture probes and are not general proof certificates.
