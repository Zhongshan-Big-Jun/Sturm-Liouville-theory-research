# Reproducibility manifest

## Immutable context

- Blueprint SHA-256:
  `0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799`
- Evidence inventory SHA-256:
  `b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f`
- Upstream derivation:
  `../r11_min_n2_general_mu/derivation.md`
- Cross-only no-go:
  `../r13_min_n2_cross_relaxation_no_go/derivation.md`

## Exact check

From the project root, run:

```powershell
& 'E:\ai_auto_solve\O3a_blueprint_v22_research_20260808\.venv\Scripts\python.exe' `
  'runs\R-20260812T165103Z-mpo3a-cont4\routes\r14_min_n2_ratio_bernstein\exact_checker.py'
```

Expected status: `PASS`.

The checker verifies algebraic identities only.  It intentionally reports
that the four final coefficient signs remain open.

