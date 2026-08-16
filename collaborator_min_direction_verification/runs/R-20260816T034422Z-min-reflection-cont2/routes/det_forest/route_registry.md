# Route registry: MIN-REFL-C2-A

```yaml
route_id: MIN-REFL-C2-A
context_id: CTX-DEFAULT
research_status: rigorous_partial_result
transaction_status: none
target_id: OBL-NGE2-MPO3A-MIN-DET-H-POSITIVE-R35
target_semantic_sha256: semantic-sha256:3f22913f6cf51e3d6615a1f6469744d142608c70fb6bd73422d725fedaf175fd
blueprint_sha256: sha256:358354060d1429c27b18767092c8a7d481b09f767740f6498eda195513f70dc0
inventory_sha256: sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
mechanism_family: signed rooted-forest / interval-partition expansion
assigned_write_root: runs/R-20260816T034422Z-min-reflection-cont2/routes/det_forest
retrieval_queries_used: 1
retrieval_query_budget: 24
graph_depth_used: 0
node_return_limit_respected: true
formalization_status: not_requested
canonical_files_touched: false
submission_files_touched: false
physical_counterexample_status: none
novelty_status: unknown
```

## Trusted inputs

- `HYP-NGE2-DOMAIN`, `semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5`
- `DEF-NGE2-MPO3A-SELFCONSISTENCY`, `semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366`
- `CLM-NGE2-MPO3A-STRUCTURE`, `semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20`
- `CLM-NGE2-MPO3A-FULL-RELAY`, `semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46`
- `CLM-NGE2-MPO3A-INTERNAL-PHASE-R8`, `semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702`
- `CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7`, `semantic-sha256:5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee`
- `CLM-NGE2-MPO3A-MIN-DETERMINANT-PARITY-R35`, `semantic-sha256:bccb84587f0fb907314362677afbcc473037f8f1f26ef1aaa0d2368acf911014`

## Forbidden premises respected

`det(H)>0`, `H>0`, complementary inertia, reflection, uniqueness, all
R14/R17 noncanonical reductions, and finite floating evidence were not used.

## Completion record

```yaml
proved_exact_results:
  - all-n signed rooted-forest formula for det(H)
  - all-n alternating principal-minor expansion in W
  - all-n positive-jump scaled forced-charge formula
refuted_mechanisms:
  - coefficientwise-positive Cauchy-Binet/forest proof in raw W variables
  - proof from positive-block shape plus phase separation and scalar forcing alone
  - direct positive-factor identification of interval charges with C2-D drift, D, or D/I
first_failed_step: sign or quantitatively compensate physical interval charges Q_[j,k]
failure_class: missing full oscillator/common-terminal quantitative relation
restart_condition: derive shared-contrast, both-momentum, terminal compensation for F_N, possibly through a translation-curvature/second-variation identity
boundaries_open:
  - terminal soft-pair word-dimension change
  - arbitrary physical sign of F_N
  - q-Jacobi determinant-zero exclusion
target_resolved: false
```
