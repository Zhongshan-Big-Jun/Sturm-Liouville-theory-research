DRAFT_ONLY_NOT_A_SUBMISSION

# R11 minimal Blueprint v2.2 proposal structure

This route-local document is a mutable preparation aid.  It is not
`proposal.json`, does not live under `statistics/submissions/`, has not
been sent to the deterministic receiver, and must not be reviewed or
integrated as a proposal.  A new immutable proposal may be created only
after an independent audit binds the frozen proof package.

## 0. Planned submission and frozen base

```text
planned_submission_id:
  SUB-20260814-0103-MPO3AMINORDER-R11
request_event_id:
  97040bec-918f-4ed4-bc66-5cd550c5e936
author_agent_id:
  r10_min_mu2_audit
run_id:
  R-20260812T165103Z-mpo3a-cont4
base_blueprint_hash:
  sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242
base_inventory_hash:
  sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f
proof_package:
  ../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/derivation.md
proof_package_bytes:
  20003
proof_package_sha256:
  sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93
author_self_audit_sha256:
  sha256:74779447f7edcd4104482132b856169dc04fa895859be02235661ae8f3655cd0
independent_audit:
  PENDING -- hard blocker before proposal creation
```

## 1. Duplicate, status, and protected-node audit

### Result

```text
duplicate_finding: NONE
protected_existing_nodes_changed: []
existing_incoming_dependencies_changed: []
existing_nodes_in_write_set: {}
inventory_operations: []
new_node_ids_occupied_in_canonical: []
canonical_protected_node_count_checked: 73
```

The nearest canonical records were compared as follows.

- `CLM-NGE2-MPO3A-MAX-GLOBAL-ORDER-R9` and its proved inference are
  protected.  They assert the actual max theorem using the already known
  positive max twist.  The proposed conditional theorem instead proves the
  reusable implication for either relay orientation and either one fixed
  derivative sign; it asserts no new general min sign.  Its max
  specialization overlaps R9, but its quantified hypothesis and reusable
  conclusion are different.  It neither supersedes nor modifies R9.
- `CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10` and its proved inference are
  protected.  They are pointwise local at an already premise-complete root
  and explicitly assert no global root order.  The proposed restricted
  corollary uses R10 as a premise and proves continuity across words and
  closures, at-most-one, and reflection fixing.  It is strictly downstream,
  not a duplicate.
- `OBL-NGE2-MPO3A-MIN-N2-GENERAL-MU-R10` remains open and unchanged.
  The new result is only at `mu=2` and does not discharge the arbitrary-
  `mu` local interface inequality.
- The broad min/O3a obligations, max norm-one-crossing obligation, R9/R10
  attempts, taxonomy, evidence grades, validator, and all protected
  incoming dependencies remain unchanged.

All planned edges have an existing or newly added source and a newly added
target.  Consequently the protected-node hashes are unchanged by
construction.

## 2. Planned semantic operations

Exactly `14` Blueprint operations are planned: `5` `add_node` operations
and `9` `add_edge` operations.  There are no `update_node`,
`remove_edge`, taxonomy, deletion, or inventory operations.

### Node 1: proved reusable inference

```text
id:
  INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
type / epistemic_type:
  inference / mathematical_inference
status / proof_status / grade:
  proved / proved / B
proof_input_eligible:
  true
title:
  Either-orientation same-sign local twist implies global root order
statement:
  For either assignment of {1,R} to the signs of S, strict negative energy
  yields a unique global relay IVP and one continuous indexed residual;
  every common-terminal residual zero is automatically a premise-complete
  transverse 2n-event root, and terminal event-pair birth or death is
  first-order soft. Therefore a uniform strict orientation
  sigma partial_q A_n^c>0 at all such roots implies global at-most-one and
  reflection fixing as stated in
  CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11.
premise_inputs:
  - HYP-NGE2-DOMAIN
  - CLM-NGE2-ZERO-BOUND
  - CLM-NGE2-MPO3A-FULL-RELAY
definition_inputs:
  - DEF-NGE2-MPO3A-SELFCONSISTENCY
conclusion:
  CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
proof_package_sha256:
  sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93
unresolved_obligations:
  []
```

### Node 2: established reusable conditional claim

```text
id:
  CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
type / epistemic_type / claim_kind:
  claim / mathematical_claim / theorem
status / truth_status / grade:
  established / established / B
title:
  Either-orientation conditional global relay root order
statement:
  For every finite R>1, integer n>=2, frequency mu>1, and either relay orientation rho_- in {1,R} on S<0 with the other coefficient on S>0, if one sign sigma in {+1,-1} satisfies sigma partial_q A_n^c(mu,q)>0 at every premise-complete transverse common-terminal root, then the global indexed residual A_n(mu,q)=T_U^n(mu,q)-T_V^(n+1)(mu,q) is continuous on q>1, has at most one zero across all relay chambers and compatible closures, and every zero is fixed by reflection after positive reorientation.
exact_statement_sha256:
  sha256:fcb02db540fdab1a2a4b7201030e64a47c1756c16caad0c3f2c4fe315ae4cbc3
inference_inputs:
  - INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
refutation_inputs:
  []
```

### Node 3: proved restricted min inference

```text
id:
  INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
type / epistemic_type:
  inference / mathematical_inference
status / proof_status / grade:
  proved / proved / B
proof_input_eligible:
  true
title:
  Trusted negative min twist closes n=2, mu=2 global root order
statement:
  Specialize the either-orientation conditional global-order theorem to the
  min law, n=2, and mu=2. Every residual zero is automatically in the
  premise-complete four-event R10 scope; trusted R10 supplies
  partial_q A_2^c<0, so sigma=-1 proves the global restricted theorem in
  CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11.
premise_inputs:
  - CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
  - CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10
definition_inputs:
  []
conclusion:
  CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
proof_package_sha256:
  sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93
unresolved_obligations:
  []
```

### Node 4: established restricted min claim

```text
id:
  CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
type / epistemic_type / claim_kind:
  claim / mathematical_claim / theorem
status / truth_status / grade:
  established / established / B
title:
  Global min root order at n=2 and mu=2
statement:
  For every finite R>1, under the min relay with n=2 and mu=2, the global indexed residual A_2(2,q)=T_U^2(q)-T_V^3(q), q>1, is continuous and has at most one zero across all relay chambers and compatible closures; every zero is automatically a premise-complete transverse four-event common-terminal root and is fixed by reflection after positive reorientation.
exact_statement_sha256:
  sha256:2fa736de49562b7d9ba23ff321dfe998d6f8787b282cb9ecf6bbd6382c46cbda
inference_inputs:
  - INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
refutation_inputs:
  []
```

### Node 5: partial route record

```text
id:
  ATT-NGE2-MPO3A-CONT4-MIN-GLOBAL-ORDER-R11
type / epistemic_type:
  attempt / research_attempt
status / attempt_status / grade:
  partial / partial / B
title:
  Conditional relay order and restricted min global closure
statement:
  Extract a relay-sign-independent local-to-global theorem from negative
  energy, word-independent continuous dependence, Sturm indexing, terminal
  softness, oriented-zero topology, and reflection covariance. Combining it
  with trusted R10 closes min global at-most-one and reflection fixing only
  for n=2, mu=2. Root existence, arbitrary mu, all n, equal norm, and O3a
  remain open; the separate dual-Jacobi route continues the all-n local
  min-sign attack.
target_inputs:
  - GOAL-NGE2-MPO3A-CONT2
method_family:
  Negative-energy zero classification, relay IVP compactness, global scalar
  zero indexing, automatic 2n-event completeness, terminal event-pair
  softness, same-oriented-zero topology, and reflection covariance
route_key:
  mpo3a-cont4-min-global-order-r11
deliverable_contract:
  A reusable local-sign-to-global-order implication and every rigorously
  supported min specialization, while keeping existence, equal-norm,
  general-mu, general-n, and O3a obligations explicit.
expected_bottleneck:
  Proving the min local q-twist beyond n=2, mu=2, especially controlling
  off-diagonal transfer in the general-n dual Jacobi continuant.
```

The eventual node must also carry the five falsification tests recorded in
the proof/self-audit package: do not fix a word globally; do not apply R10
before automatic premise completeness; use `rho_-=R` at min joint
contacts; require second-order terminal softness; and do not infer
existence, general `mu/n`, equal norm, or O3a.

### Planned edges

```text
HYP-NGE2-DOMAIN
  --premise_input--> INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
CLM-NGE2-ZERO-BOUND
  --premise_input--> INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
CLM-NGE2-MPO3A-FULL-RELAY
  --premise_input--> INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
DEF-NGE2-MPO3A-SELFCONSISTENCY
  --definition_input--> INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
  --inference_input--> CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11
  --premise_input--> INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10
  --premise_input--> INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
  --inference_input--> CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11
GOAL-NGE2-MPO3A-CONT2
  --target_input--> ATT-NGE2-MPO3A-CONT4-MIN-GLOBAL-ORDER-R11
```

## 3. Exact planned write set

```json
{
  "existing_nodes": {},
  "new_node_ids": [
    "INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11",
    "CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11",
    "INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11",
    "CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11",
    "ATT-NGE2-MPO3A-CONT4-MIN-GLOBAL-ORDER-R11"
  ],
  "inventory_rows": {}
}
```

## 4. Exact planned read set at canonical `7eb62567...`

The deterministic incoming closure of the five new nodes under the nine
planned edges contains exactly `54` existing nodes:

```json
{
  "CLM-NGE2-BANGBANG": "semantic-sha256:c2da831e3743218571668231c7f98b188a5a3363ba1fa185baaeb4051d15f893",
  "CLM-NGE2-ENDPOINT-COUNT": "semantic-sha256:e36784da539e1faab0c3403c33349fccad0ddb77e412e372b6bfeec80a2e4a04",
  "CLM-NGE2-ENERGY-INVARIANT": "semantic-sha256:cbd00bec041c6bc6e7dbae4fa62b0e2957ea946e1706cf585aa911dc680a9274",
  "CLM-NGE2-EXACT2N-ALL": "semantic-sha256:aa8c454d1628e7582a8e9a621567ffff115d45521bd653c2e8eccc1445e96fd0",
  "CLM-NGE2-EXACT2N-MAX": "semantic-sha256:e6d890f47362efbf6a98553beb1089ca48b28e0d6569b55684b9e9e2957e7199",
  "CLM-NGE2-EXACT2N-MIN": "semantic-sha256:654c34d2c3b5af85b7745290c191b9ea8072b789f70f25ac729b9841433642b5",
  "CLM-NGE2-EXISTENCE": "semantic-sha256:8de200f175e075d3f237bbe2acd3c31d898098bfef5386734c066851fbf88031",
  "CLM-NGE2-FINITE-REDUCTION": "semantic-sha256:674fec0c357d4a6a7a54251a7a61a517af50658b5d8dc240781ac64f46367804",
  "CLM-NGE2-MAX-ENDPOINT-RIGIDITY": "semantic-sha256:1ec54081b0c277dff94f0532aba097288de980c3ad8b9ee951700e7a547c0aa6",
  "CLM-NGE2-MIN-ENDPOINT-RIGIDITY": "semantic-sha256:f609aaf51aeb2ad665699137e140f378a483044d1102d998ffdce539a033f140",
  "CLM-NGE2-MPO3A-ALL": "semantic-sha256:6f85432e60d0fe1c4e145c18904f7ca1a5afa32aa6c30119540d92339f702666",
  "CLM-NGE2-MPO3A-CELL-PHASE-R6": "semantic-sha256:34ddfc0ec931503621e7658d7186318b41b3f910214000e23c55bae7aaac040e",
  "CLM-NGE2-MPO3A-FULL-RELAY": "semantic-sha256:59581f99dcf540ddca1c9ec94818da1568b7eaebdce0f06b41fac8b81a3d2a46",
  "CLM-NGE2-MPO3A-HYBRID-TWIST-R6": "semantic-sha256:6e2749fd147662212ade344e6dec0a715a83e76cb954e031134748a99a134b7b",
  "CLM-NGE2-MPO3A-INTERNAL-PHASE-R8": "semantic-sha256:43f3bbdfa4b51c4504501ea9d5d68bf05ec1ca5b844da5dcf271da1f640d6702",
  "CLM-NGE2-MPO3A-MAX": "semantic-sha256:0926011d55103057d5641d97d1b4c4d3eeaf308f19a5f6de723a7fb6ebca5f1e",
  "CLM-NGE2-MPO3A-MIN": "semantic-sha256:b66ad3a2ff5a8c8f56a1d6f48e6c96a72f01e114029c03b5789159dfe68a8d27",
  "CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10": "semantic-sha256:157a7bf928676b7565e5e08e965909ab0657e48888d37095c43352a228bbbd21",
  "CLM-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7": "semantic-sha256:5a4e8e40668e50766f7594724eb357bddcf7b94139b86e8fdbf14582e39088ee",
  "CLM-NGE2-MPO3A-PROPERNESS": "semantic-sha256:b429060dd6662757e95cc783dcb737040dad2920cb3ac9ebc4ed15b13fe43695",
  "CLM-NGE2-MPO3A-SMALL-CONTRAST": "semantic-sha256:975ece9f6048cbe3c8bde1a68e273c92f23b6f4e6f706523ac42483814793f2d",
  "CLM-NGE2-MPO3A-STRUCTURE": "semantic-sha256:86658c00dea17604d3571c88e1624edc5cace6cbbd9a7eaf9548d45a8280cb20",
  "CLM-NGE2-MPO3A-SYMPLECTIC-NESTED": "semantic-sha256:4c11a291f871bf44dab3d4970f8b6457bbacafcac6842ae950bd9729be4d2c0e",
  "CLM-NGE2-ZERO-BOUND": "semantic-sha256:49bf4cf80c0026e580c61340ba7066bec075da0bb2f7e4ee8a019e981f0acab6",
  "DEF-BANGBANG-SWITCH-COUNT": "semantic-sha256:98d761a44bd051d9d05fe5cc257ef6491825bc57772a33b460c1ce6f553f8074",
  "DEF-NGE2-ENDPOINT-NORMING": "semantic-sha256:1d55990ee7d6e25f63744af2bd9c7d47becf0f092ff324002468a65d8fa063fa",
  "DEF-NGE2-MPO3A-SELFCONSISTENCY": "semantic-sha256:861dabf5b917094121f0525e49e5e3942199266698b821b0ed566a2d6a785366",
  "DEF-SL-BOX-ADJ-GAP": "semantic-sha256:c6ee9a0ef59b085763d3be78055528f0bf910eb75698f61b04d0ae3e01f8b13f",
  "GOAL-NGE2-MPO3A-CONT2": "semantic-sha256:6b58d8012244525e780e3173bfb8f8cc093b669a84cdcf2f184e63d20e837af4",
  "HYP-NGE2-DOMAIN": "semantic-sha256:86946c7b3ea4e0ec4424c2d92c3e8fd36144d4cd6c960acbf0a334b7062636b5",
  "INF-NGE2-BANGBANG": "semantic-sha256:55f5f4418c30f9de4411fff2a6ca89d9a50a53bb0668b47900a74edfe2d817fa",
  "INF-NGE2-ENDPOINT-COUNT": "semantic-sha256:d58961f2fe741c932cdeb8fc7fb4aecf8ab9bfdbe6eba5b9872b84d4364420f8",
  "INF-NGE2-ENERGY-INVARIANT": "semantic-sha256:933e45b816610a7a7691efd0cc02c7f6fe015767cad5175a3a1d6bfb70eedfca",
  "INF-NGE2-EXACT2N-MAX": "semantic-sha256:b6900fc244632b43c808465c3edb3d4c100e923605df3e90165813ad875b93f1",
  "INF-NGE2-EXACT2N-MIN": "semantic-sha256:d0443a902c7c3f235df6ce70410e8d4399cec1be04558ae96c932ca9e88eec99",
  "INF-NGE2-EXACT2N-SYNTHESIS": "semantic-sha256:009fdb5815dd109dd562f16fd11cff7a16ec0bd5006edd3da0bd45325bdffc17",
  "INF-NGE2-EXISTENCE": "semantic-sha256:847752867f67c060dbe8f03af8963e03e1babd34b6a729e38e2d59d6e86e7e01",
  "INF-NGE2-MAX-ENDPOINT-RIGIDITY": "semantic-sha256:9db2fe8bd5f3649a8b19452ab74dc67ef00c36785b35389181ec9499766c9871",
  "INF-NGE2-MIN-ENDPOINT-RIGIDITY": "semantic-sha256:77a721a79d2af5c49467c70e82c3d7b7af76b368180f9b4420d2e892d38ef81e",
  "INF-NGE2-MPO3A-CELL-PHASE-R6": "semantic-sha256:76505a7eb2ffa45225adf487ce6f8f250a2ed35aa415c5a9756536a507db5558",
  "INF-NGE2-MPO3A-FULL-RELAY": "semantic-sha256:67619802347bd09bf36fad79d71becc6a79a954e930d31ee3f1611864a544934",
  "INF-NGE2-MPO3A-HYBRID-TWIST-R6": "semantic-sha256:788fd7a0a1ab30540c1da2194e6ce6365ae60cc1eea04cc1a13a779b58f07dd8",
  "INF-NGE2-MPO3A-INTERNAL-PHASE-R8": "semantic-sha256:f377eb235ffcb122f315d646d9a56665dbb55cbfecc826a4f85c19cd1ce4df45",
  "INF-NGE2-MPO3A-MAX": "semantic-sha256:0b3aa5267fed0ca75f062d609dcf010d80e213f897b55580564626cd5bcd2896",
  "INF-NGE2-MPO3A-MIN": "semantic-sha256:60af73ec98a3eddf909cd1ede43120ec24d959e60e7977e458228fc4c3c3da71",
  "INF-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10": "semantic-sha256:04d7bb4c8d64824b2f1354adf34076d107fd2e124e758700a699228c64213820",
  "INF-NGE2-MPO3A-PHYSICAL-CONTINUANT-R7": "semantic-sha256:804abd6209285b16cfb62428a98700f2262049146855dd8c6b3b04f0712b139f",
  "INF-NGE2-MPO3A-PROPERNESS": "semantic-sha256:d698c67222bae7f4efb5f2f61df4c627d79197da50013140237ea487353656e6",
  "INF-NGE2-MPO3A-SMALL-CONTRAST": "semantic-sha256:9d2ce4f717c8f3ccced987a307b63b6a89a0d88734d5cff822473f0c67b63201",
  "INF-NGE2-MPO3A-STRUCTURE": "semantic-sha256:c40f12d8da042ca1858f28228c36148e9f77491cfac8500cf99bc4eaa036332a",
  "INF-NGE2-MPO3A-SYMPLECTIC-NESTED": "semantic-sha256:2d850dbc0f45b117b6cd84f045e8a6934b60c85cea809631a184b91e11039c98",
  "INF-NGE2-MPO3A-SYNTHESIS": "semantic-sha256:5423ba44ce6cc2f75f01b40dd96f1886c2ce8d533a342a028966f9cfaa91d349",
  "INF-NGE2-SYNTHESIS": "semantic-sha256:4a2995f805a72dea4e009ca4388baf814471b46cb262a64c65c3de8e6108ab62",
  "INF-NGE2-ZERO-BOUND": "semantic-sha256:014a9f5107989699237b856c4dd0fd50ec259eba0d8affa1bba5d801216a5dc4"
}
```

Before immutable proposal creation this closure must be recomputed from the
then-current canonical graph.  Any hash or membership change invalidates
this draft rather than authorizing an update to a protected node.

## 5. Required review-evidence structure

The eventual proposal should contain:

- `math_premise_contracts` for `HYP-NGE2-DOMAIN`,
  `CLM-NGE2-ZERO-BOUND`, `CLM-NGE2-MPO3A-FULL-RELAY`,
  `DEF-NGE2-MPO3A-SELFCONSISTENCY`, the newly proved conditional claim, and
  trusted `CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10`;
- two `math_proof_justifications`, one for each proved inference, both
  binding proof-package hash `66916110...`, with ordered steps, exact
  boundary cases, `external_results: []`, and
  `unresolved_obligations: []`;
- one `math_research_state_records` item for the partial attempt, explicitly
  recording that general min `mu/n`, root existence, equal norm, and O3a
  remain open;
- evidence references to `problem_contract.md`, `derivation.md`,
  `self_audit.md`, and the future independent audit bound to the exact
  derivation hash.

The conditional proof justification should enumerate: negative-energy zero
classification; global IVP/no Zeno; word-independent compactness and
indexed-zero continuity; automatic `2n`-event completeness; terminal
`rho_-` softness; same-oriented-zero topology; and reflection only after
at-most-one.

The restricted proof justification should enumerate: specialization to min
`rho_-=R,n=2,mu=2`; automatic four-event R10 premise completeness;
trusted R10 `partial_q A_2^c<0`; equality of chamber/global first
derivatives; and application with `sigma=-1`.

## 6. Hard stop before submission

```text
blocking_condition:
  No independent definition/logic/boundary/adversarial audit currently
  binds derivation SHA-256 66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93.
required_next_action:
  Obtain and freeze that audit; then recompute canonical hashes, duplicate
  audit, protected-node check, and the full semantic read set before
  creating a new immutable proposal.json.
forbidden_now:
  create submissions/SUB-20260814-0103-MPO3AMINORDER-R11/proposal.json;
  invoke receive_blueprint.py --validate-only;
  request Blueprint review;
  modify blueprint.json or evidence_inventory.csv.
```
