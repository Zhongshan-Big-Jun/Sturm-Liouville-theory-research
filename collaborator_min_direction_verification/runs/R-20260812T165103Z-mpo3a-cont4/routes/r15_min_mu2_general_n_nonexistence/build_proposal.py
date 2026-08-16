"""Build the immutable R15 Blueprint proposal from the current canonical graph."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


SUBMISSION_ID = "SUB-20260814-1738-MPO3AMINMU2NGEN-R15"
AUTHOR = "/root"
RUN_ID = "R-20260812T165103Z-mpo3a-cont4"
BASE_BLUEPRINT = "sha256:0120d1fb32af1a30449575995efccb6d1afcce416ee671ad00a5f296400fd799"
BASE_INVENTORY = "sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f"
PROOF_SHA = "sha256:97816827f2044ee7abbc2f80b90d0323c48298d3f797dfb6a15379127ed9509e"
CHECKER_SHA = "sha256:e72deabb74c2e1b88f02dfdabae7e242d418e23354dff4640db4f1f088ecdb42"
CHECKER_JSON_SHA = "sha256:52c84d41496f406c1e83d6a8bd6e977b20fdef3d3c4bbaf6c7abbc73c2f93e65"
SELF_AUDIT_SHA = "sha256:684aa7a05edff5be564f493d157f29044624e61b2a16db2aa74921211fb99a12"
MANIFEST_SHA = "sha256:44c99d2d779ecf03a6f258c6c334afdd0d2ab6448e1326edddd7621c6464667f"
INDEPENDENT_AUDIT_SHA = "sha256:f49cc644bf8a0dd5a6159688dd55f0853381fc0d3c57da64209a005ac15acb71"
INDEPENDENT_CHECKER_SHA = "sha256:1a9c3e2d810eba915f6a3e9536d23ad4bd0e10caedb765c0f8b62c3431d6160a"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    sys.path.insert(0, str(root / "tools"))
    from blueprint_common import atomic_write_json, sha256_file  # noqa: PLC0415
    from receive_blueprint import incoming_closure, semantic_hashes  # noqa: PLC0415

    blueprint_path = root / "blueprint.json"
    inventory_path = root / "evidence_inventory.csv"
    blueprint = json.loads(blueprint_path.read_text(encoding="utf-8"))
    base_blueprint_hash = sha256_file(blueprint_path)
    base_inventory_hash = sha256_file(inventory_path)
    if base_blueprint_hash != BASE_BLUEPRINT or base_inventory_hash != BASE_INVENTORY:
        raise SystemExit(
            f"canonical snapshot changed: blueprint={base_blueprint_hash}, inventory={base_inventory_hash}"
        )

    inference_id = "INF-NGE2-MPO3A-MIN-MU2-NGE3-NONEXISTENCE-R15"
    claim_id = "CLM-NGE2-MPO3A-MIN-MU2-NGE3-NONEXISTENCE-R15"
    attempt_id = "ATT-NGE2-MPO3A-CONT4-MIN-MU2-NGE3-R15"
    new_ids = {inference_id, claim_id, attempt_id}
    occupied = new_ids & {item["id"] for item in blueprint["nodes"]}
    if occupied:
        raise SystemExit(f"planned node IDs are occupied: {sorted(occupied)}")

    proof_package = {
        "path": "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/derivation.md",
        "sha256": PROOF_SHA,
    }
    inference = {
        "id": inference_id,
        "type": "inference",
        "title": "Interface contraction forbids every mu=2 min word with n at least three",
        "statement": "The accepted finite-contrast relay structure and sharp internal phase allocation, together with exact mu=2 two-momentum interface elimination, imply a strict positive-cell amplitude contraction in both traversal directions. Every n>=3 min word contains an internal negative-positive-negative triple whose shared positive-cell ratio and reciprocal are both strict contractions, yielding the nonexistence theorem in CLM-NGE2-MPO3A-MIN-MU2-NGE3-NONEXISTENCE-R15.",
        "status": "proved",
        "grade": "B",
        "mainline": "mathematics",
        "epistemic_type": "mathematical_inference",
        "context_id": "CTX-DEFAULT",
        "premise_inputs": [
            "HYP-NGE2-DOMAIN",
            "CLM-NGE2-MPO3A-STRUCTURE",
            "CLM-NGE2-MPO3A-FULL-RELAY",
            "CLM-NGE2-MPO3A-INTERNAL-PHASE-R8",
        ],
        "definition_inputs": ["DEF-NGE2-MPO3A-SELFCONSISTENCY"],
        "conclusion": claim_id,
        "proof_status": "proved",
        "proof_input_eligible": True,
        "proof_package": proof_package,
        "unresolved_obligations": [],
    }
    claim = {
        "id": claim_id,
        "type": "claim",
        "title": "No strict minimum-law full-relay root at mu=2 for n at least three",
        "statement": "For every finite R>1 and every integer n>=3, there is no strict premise-complete transverse common-terminal full-relay root with 2n events under the minimum saturation law at relay frequency mu=2. The statement permits arbitrary asymmetry and requires neither reflection nor the endpoint norm equation.",
        "status": "established",
        "grade": "B",
        "mainline": "mathematics",
        "epistemic_type": "mathematical_claim",
        "context_id": "CTX-DEFAULT",
        "claim_kind": "theorem",
        "truth_status": "established",
        "inference_inputs": [inference_id],
        "refutation_inputs": [],
    }
    attempt = {
        "id": attempt_id,
        "type": "attempt",
        "title": "Minimum-law mu=2 internal composition obstruction",
        "statement": "Eliminate a physical mu=2 positive-negative interface exactly and prove its positive-cell amplitude ratio lies in (0,1). Time reversal gives the reciprocal ratio at the opposite interface. This closes nonexistence for every min word with n>=3 by one internal negative-positive-negative triple. The n=2 slice remains governed by the trusted R10/R11 theorems; general mu, the maximum law, and universal O3a remain open.",
        "status": "partial",
        "grade": "B",
        "mainline": "research",
        "epistemic_type": "research_attempt",
        "context_id": "CTX-DEFAULT",
        "attempt_status": "partial",
        "target_inputs": ["GOAL-NGE2-MPO3A-CONT2"],
        "method_family": "Exact half-angle interface elimination, strict semialgebraic amplitude contraction, oscillator transfer time reversal, and arbitrary-word overlap compatibility",
        "route_key": "mpo3a-cont4-min-mu2-general-n-nonexistence-r15",
        "deliverable_contract": "A proof or refutation of the mu=2 minimum-law premise-complete root set for every n>=3, with all noncovered signs, frequencies, degeneracies, and O3a scopes explicit.",
        "falsification_tests": [
            "Reconstruct the interface amplitudes from both raw momentum equations rather than assigning a and b from their signs.",
            "Check that reversing a negative-positive pair retains contrast r=sqrt(R) and yields 1/z_j, not z_j or a formula with reciprocal contrast.",
            "Verify that I_2,I_3,I_4 are internal precisely for every n>=3 and that n=2 has no such triple.",
            "Do not promote the empty mu=2,n>=3 slice to general mu, max law, boundary words, existence, or universal O3a.",
        ],
        "expected_bottleneck": "Extending the strict interface contraction away from mu=2; at general mu the remaining n=2 complementary-inertia inequality retains full common-angle transcendental constraints.",
        "provenance": {
            "run_id": RUN_ID,
            "artifacts": [
                "routes/r15_min_mu2_general_n_nonexistence/problem_contract.md",
                "routes/r15_min_mu2_general_n_nonexistence/derivation.md",
                "routes/r15_min_mu2_general_n_nonexistence/general_n_exact_check.py",
                "routes/r15_min_mu2_general_n_nonexistence/general_n_exact_check.json",
                "routes/r15_min_mu2_general_n_nonexistence/self_audit.md",
                "routes/r15_min_mu2_general_n_nonexistence/freeze_manifest.json",
                "routes/r15_min_mu2_general_n_nonexistence_independent_audit/independent_audit.md",
                "routes/r15_min_mu2_general_n_nonexistence_independent_audit/independent_orientation_check.py",
            ],
        },
    }
    nodes = [inference, claim, attempt]
    edges = [
        ("HYP-NGE2-DOMAIN", inference_id, "premise_input"),
        ("CLM-NGE2-MPO3A-STRUCTURE", inference_id, "premise_input"),
        ("CLM-NGE2-MPO3A-FULL-RELAY", inference_id, "premise_input"),
        ("CLM-NGE2-MPO3A-INTERNAL-PHASE-R8", inference_id, "premise_input"),
        ("DEF-NGE2-MPO3A-SELFCONSISTENCY", inference_id, "definition_input"),
        (inference_id, claim_id, "inference_input"),
        ("GOAL-NGE2-MPO3A-CONT2", attempt_id, "target_input"),
    ]
    operations = [{"op": "add_node", "node": item} for item in nodes]
    operations.extend(
        {"op": "add_edge", "source": source, "target": target, "role": role}
        for source, target, role in edges
    )

    candidate = json.loads(json.dumps(blueprint))
    candidate["nodes"].extend(nodes)
    candidate["edges"].extend(
        {"source": source, "target": target, "role": role}
        for source, target, role in edges
    )
    current_hashes = semantic_hashes(blueprint)
    closure = incoming_closure(candidate, new_ids) - new_ids
    read_set = {node_id: current_hashes[node_id] for node_id in sorted(closure)}

    proposal = {
        "schema_version": "2.2",
        "submission_id": SUBMISSION_ID,
        "author_agent_id": AUTHOR,
        "run_id": RUN_ID,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "base_blueprint_hash": base_blueprint_hash,
        "base_inventory_hash": base_inventory_hash,
        "supersedes": None,
        "summary": "Add an independently audited exact theorem that the strict premise-complete minimum-law mu=2 root set is empty for every n>=3, while retaining n=2, general mu, max, and universal O3a at their existing statuses.",
        "operations": operations,
        "inventory_operations": [],
        "write_set": {
            "existing_nodes": {},
            "new_node_ids": [inference_id, claim_id, attempt_id],
            "inventory_rows": {},
        },
        "read_set": {"upstream_nodes": read_set},
        "rationale": {
            "research_status": "rigorous_restricted_nonexistence_theorem_with_universal_target_open",
            "scope": "Finite R>1, minimum relay, mu=2, integer n>=3, strict premise-complete transverse common-terminal roots only. Arbitrary asymmetry is covered. The theorem excludes the root set in this slice but says nothing about n=2, mu!=2, max, boundary/grazing words, or universal O3a.",
            "duplicate_policy": "No canonical node states this all-n mu=2 nonexistence slice. Trusted R10/R11 cover only min n=2,mu=2 and are not changed. The earlier route-local n=3 composition package was never canonical and is strictly subsumed by this arbitrary-n proof.",
            "computation_policy": "No numerical evidence is a premise. Symbolic scripts verify exact algebraic identities and indexing only; the arbitrary-index contradiction is analytic.",
            "audit_policy": f"The proof {PROOF_SHA}, exact checker {CHECKER_SHA}, checker result {CHECKER_JSON_SHA}, author audit {SELF_AUDIT_SHA}, freeze manifest {MANIFEST_SHA}, independent four-part audit {INDEPENDENT_AUDIT_SHA}, and independent checker {INDEPENDENT_CHECKER_SHA} are bound exactly.",
            "novelty_policy": "unknown; no priority claim",
        },
        "evidence_refs": [
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/problem_contract.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/derivation.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/general_n_exact_check.py",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/general_n_exact_check.json",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/self_audit.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence/freeze_manifest.json",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence_independent_audit/independent_audit.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r15_min_mu2_general_n_nonexistence_independent_audit/independent_orientation_check.py",
        ],
        "review_evidence": {
            "logic_justifications": [],
            "method_matches": [],
            "literature_sources": [],
            "math_premise_contracts": [
                {
                    "node_id": "HYP-NGE2-DOMAIN",
                    "premise_kind": "problem_hypothesis",
                    "scope": "Finite real R>1 and integer n>=2 in the accepted adjacent-gap problem.",
                    "contract_explanation": "Supplies the ambient finite-contrast and integer-index domain only; the proof specializes to mu=2, min, and n>=3.",
                },
                {
                    "node_id": "CLM-NGE2-MPO3A-STRUCTURE",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "Every self-consistent max/min point has the accepted exact simple event and nodal structure.",
                    "contract_explanation": "Supplies simple active events, alternating internal cells, and nonzero event amplitudes under the strict transverse premise-complete scope.",
                },
                {
                    "node_id": "CLM-NGE2-MPO3A-FULL-RELAY",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "Finite R>1, n>=2, either relay law, and the exact possibly asymmetric common-terminal full-relay representation.",
                    "contract_explanation": "Supplies the physical relay equations, momentum matching, material allocation, and correspondence used by the two-cell elimination.",
                },
                {
                    "node_id": "CLM-NGE2-MPO3A-INTERNAL-PHASE-R8",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "Every internal positive/negative cell of a strict premise-complete root for either law and every finite R>1.",
                    "contract_explanation": "At mu=2 it gives 0<theta_positive<pi/3 and pi/3<theta_negative<pi/2, hence the strict half-angle domain used to prove 0<a<1.",
                },
                {
                    "node_id": "DEF-NGE2-MPO3A-SELFCONSISTENCY",
                    "premise_kind": "definition_contract",
                    "scope": "Max/min sign law, exactly 2n effective switches, and a.e. identification.",
                    "contract_explanation": "Fixes minimum-law terminology and effective-event scope; it is not used as an existence, symmetry, or uniqueness premise.",
                },
            ],
            "math_proof_justifications": [
                {
                    "node_id": inference_id,
                    "ordered_steps": [
                        "For a mu=2 physical positive-negative interface, solve both continuous-momentum equations in half-angle variables x and y to obtain the exact amplitude ratios a(x,y,r) and b(x,y,r).",
                        "Use the strict R8 phase domain to introduce X=x^2, Y=y^2 and kappa. The physical inequalities kappa_0<kappa<kappa_N<kappa_D give a positive denominator, while the exact boundary-gap factorization makes a-1<0; therefore 0<a(x,y,r)<1 at every such interface.",
                        "For an arbitrary 2n-event minimum-law word, define z_j=A_(j+1)/A_j. A forward positive-negative pair gives z_j=a(x_j,y_(j+1),r).",
                        "Reverse the adjacent negative-positive pair. The oscillator identity J M_omega J=M_omega^{-1} reverses both momenta and changes material order (R,1) to the same canonical order (1,R) without replacing r by 1/r, so 1/z_j=a(x_j,y_(j-1),r).",
                        "Every n>=3 word contains the internal negative-positive-negative triple I_2,I_3,I_4. Thus a(x_3,y_2,r)a(x_3,y_4,r)=1, while both factors lie strictly in (0,1), a contradiction.",
                    ],
                    "boundary_cases": [
                        "The first admissible case n=3 has exactly the required I_2,I_3,I_4 triple; n=2 has no positive internal cell with two negative neighbors and is excluded.",
                        "Both endpoint cells and the norm equation are unused because the contradiction is wholly internal; arbitrary asymmetry and global sign reversal are covered.",
                        "R=1, mu!=2, the maximum law, phase endpoints, grazing, collided events, collapsed feasibility, zero-length cells, nontransverse roots, and endpoint escape are outside the theorem.",
                        "The conclusion is nonexistence of strict premise-complete common-terminal roots in this slice only; it does not assert an inertia sign, root existence elsewhere, general min uniqueness, max uniqueness, or universal O3a.",
                    ],
                    "external_results": [],
                    "proof_package_sha256": PROOF_SHA,
                    "unresolved_obligations": [],
                }
            ],
            "math_refutations": [],
            "math_research_state_records": [
                {
                    "node_id": attempt_id,
                    "record_kind": "partial_attempt",
                    "status_justification": "The route completely proves the stated mu=2,min,n>=3 nonexistence theorem. It remains partial relative to the active O3a program because n=2, general mu, the maximum law, boundary closures, and universal O3a are not resolved by this route.",
                }
            ],
            "research_claim_contracts": [],
            "research_inference_justifications": [],
            "research_state_records": [],
        },
    }

    submission = root / "submissions" / SUBMISSION_ID
    proposal_path = submission / "proposal.json"
    if proposal_path.exists():
        raise SystemExit(f"immutable proposal already exists: {proposal_path}")
    submission.mkdir(parents=False, exist_ok=False)
    atomic_write_json(proposal_path, proposal, overwrite=False)
    print(
        json.dumps(
            {
                "proposal": str(proposal_path),
                "proposal_sha256": sha256_file(proposal_path),
                "base_blueprint_sha256": base_blueprint_hash,
                "base_inventory_sha256": base_inventory_hash,
                "operation_count": len(operations),
                "new_node_count": len(nodes),
                "edge_count": len(edges),
                "read_set_count": len(read_set),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
