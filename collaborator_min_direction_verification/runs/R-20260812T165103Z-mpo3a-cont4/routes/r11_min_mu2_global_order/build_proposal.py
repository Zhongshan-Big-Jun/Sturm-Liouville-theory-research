"""Build the immutable R11 Blueprint proposal from the current canonical graph.

This route-local helper is deterministic apart from the proposal timestamp.  It
never edits canonical files and refuses to overwrite an existing proposal.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


SUBMISSION_ID = "SUB-20260814-0103-MPO3AMINORDER-R11"
AUTHOR = "r10_min_mu2_audit"
RUN_ID = "R-20260812T165103Z-mpo3a-cont4"
PROOF_SHA = "sha256:66916110c3d90b47c4054c77a744acc204b481f63f36321662dac165ae7d5c93"
SELF_AUDIT_SHA = "sha256:74779447f7edcd4104482132b856169dc04fa895859be02235661ae8f3655cd0"
INDEPENDENT_AUDIT_SHA = "sha256:b15764f21e75849293188edc74266cc14183223890a302700facbea06562d4a7"


def node(
    node_id: str,
    node_type: str,
    title: str,
    statement: str,
    status: str,
    grade: str,
    epistemic_type: str,
    **extra: object,
) -> dict[str, object]:
    value: dict[str, object] = {
        "id": node_id,
        "type": node_type,
        "title": title,
        "statement": statement,
        "status": status,
        "grade": grade,
        "mainline": "mathematics" if node_type in {"inference", "claim"} else "research",
        "epistemic_type": epistemic_type,
        "context_id": "CTX-DEFAULT",
    }
    value.update(extra)
    return value


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
    expected_blueprint = "sha256:7eb6256786ff20ce8dcf5bb1b8ce669337eb216a38e4e274c8292f1ef6456242"
    expected_inventory = "sha256:b6286574edbcb70ad22e5c6758a81f00dd01572c0764b8816be23cb6b166fb6f"
    if base_blueprint_hash != expected_blueprint or base_inventory_hash != expected_inventory:
        raise SystemExit(
            f"canonical snapshot changed: blueprint={base_blueprint_hash}, inventory={base_inventory_hash}"
        )

    conditional_inference = "INF-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11"
    conditional_claim = "CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11"
    restricted_inference = "INF-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11"
    restricted_claim = "CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11"
    attempt = "ATT-NGE2-MPO3A-CONT4-MIN-GLOBAL-ORDER-R11"
    new_ids = {
        conditional_inference,
        conditional_claim,
        restricted_inference,
        restricted_claim,
        attempt,
    }
    occupied = new_ids & {item["id"] for item in blueprint["nodes"]}
    if occupied:
        raise SystemExit(f"planned node IDs are occupied: {sorted(occupied)}")

    proof_package = {
        "path": "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/derivation.md",
        "sha256": PROOF_SHA,
    }
    conditional_statement = (
        "For every finite R>1, integer n>=2, frequency mu>1, and either relay orientation "
        "rho_- in {1,R} on S<0 with the other coefficient on S>0, if one sign sigma in "
        "{+1,-1} satisfies sigma partial_q A_n^c(mu,q)>0 at every premise-complete transverse "
        "common-terminal root, then the global indexed residual "
        "A_n(mu,q)=T_U^n(mu,q)-T_V^(n+1)(mu,q) is continuous on q>1, has at most one zero "
        "across all relay chambers and compatible closures, and every zero is fixed by "
        "reflection after positive reorientation."
    )
    restricted_statement = (
        "For every finite R>1, under the min relay with n=2 and mu=2, the global indexed "
        "residual A_2(2,q)=T_U^2(q)-T_V^3(q), q>1, is continuous and has at most one zero "
        "across all relay chambers and compatible closures; every zero is automatically a "
        "premise-complete transverse four-event common-terminal root and is fixed by "
        "reflection after positive reorientation."
    )
    new_nodes = [
        node(
            conditional_inference,
            "inference",
            "Either-orientation same-sign local twist implies global root order",
            "Negative relay energy, global relay well-posedness and word-independent continuous zero-time dependence, automatic 2n-event premise completeness, and terminal event-pair softness imply the conditional global-order theorem stated in CLM-NGE2-MPO3A-EITHER-CONDITIONAL-GLOBAL-ORDER-R11 for either relay orientation and either one uniform strict derivative sign.",
            "proved",
            "B",
            "mathematical_inference",
            premise_inputs=[
                "HYP-NGE2-DOMAIN",
                "CLM-NGE2-ZERO-BOUND",
                "CLM-NGE2-MPO3A-FULL-RELAY",
            ],
            definition_inputs=["DEF-NGE2-MPO3A-SELFCONSISTENCY"],
            conclusion=conditional_claim,
            proof_status="proved",
            proof_input_eligible=True,
            proof_package=proof_package,
            unresolved_obligations=[],
        ),
        node(
            conditional_claim,
            "claim",
            "Either-orientation conditional global relay root order",
            conditional_statement,
            "established",
            "B",
            "mathematical_claim",
            claim_kind="theorem",
            truth_status="established",
            inference_inputs=[conditional_inference],
            refutation_inputs=[],
        ),
        node(
            restricted_inference,
            "inference",
            "Trusted negative min twist closes n=2, mu=2 global root order",
            "Specialize the either-orientation conditional theorem to the min relay, n=2 and mu=2. Every global residual zero is automatically a premise-complete transverse four-event root, so trusted R10 supplies partial_q A_2^c<0; the sign sigma=-1 gives the restricted global-order and reflection theorem in CLM-NGE2-MPO3A-MIN-N2-MU2-GLOBAL-ORDER-R11.",
            "proved",
            "B",
            "mathematical_inference",
            premise_inputs=[
                conditional_claim,
                "CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10",
            ],
            definition_inputs=[],
            conclusion=restricted_claim,
            proof_status="proved",
            proof_input_eligible=True,
            proof_package=proof_package,
            unresolved_obligations=[],
        ),
        node(
            restricted_claim,
            "claim",
            "Global min root order at n=2 and mu=2",
            restricted_statement,
            "established",
            "B",
            "mathematical_claim",
            claim_kind="theorem",
            truth_status="established",
            inference_inputs=[restricted_inference],
            refutation_inputs=[],
        ),
        node(
            attempt,
            "attempt",
            "Conditional relay order and restricted min global closure",
            "Extract a relay-sign-independent local-to-global theorem from negative energy, word-independent continuous dependence, Sturm indexing, terminal softness, oriented-zero topology, and reflection covariance. Combining it with trusted R10 closes min global at-most-one and reflection fixing only for n=2, mu=2. Root existence, arbitrary mu, all n, equal norm, and O3a remain open; the separate dual-Jacobi route continues the all-n local min-sign attack.",
            "partial",
            "B",
            "research_attempt",
            attempt_status="partial",
            target_inputs=["GOAL-NGE2-MPO3A-CONT2"],
            method_family="Negative-energy zero classification, relay-IVP compactness, global scalar-zero indexing, automatic 2n-event completeness, terminal event-pair softness, same-oriented-zero topology, and reflection covariance",
            route_key="mpo3a-cont4-min-global-order-r11",
            deliverable_contract="A reusable local-sign-to-global-order implication and every rigorously supported min specialization, while retaining existence, equal-norm, general-mu, general-n, and O3a as explicit open obligations.",
            falsification_tests=[
                "Do not globalize by fixing one material word; prove continuity through event-pair birth, death, and collision.",
                "Do not apply the R10 local theorem until every global A_2 zero has been proved premise-complete with exactly four transverse events.",
                "Use rho_-=R on the min initial and terminal punctured cells and reverse the oriented-zero derivative sign.",
                "Prove terminal chamber/global residual agreement to second order before importing the chamber derivative.",
                "Do not infer root existence, arbitrary mu, n>2, equal-norm uniqueness, min O3a, or universal O3a.",
            ],
            expected_bottleneck="Proving the min local q-twist beyond n=2, mu=2, especially controlling off-diagonal transfer in the general-n dual Jacobi continuant.",
            provenance={
                "run_id": RUN_ID,
                "artifacts": [
                    "routes/r11_min_mu2_global_order/problem_contract.md",
                    "routes/r11_min_mu2_global_order/derivation.md",
                    "routes/r11_min_mu2_global_order/self_audit.md",
                    "routes/r11_min_mu2_global_order/independent_audit.md",
                ],
            },
        ),
    ]
    edges = [
        ("HYP-NGE2-DOMAIN", conditional_inference, "premise_input"),
        ("CLM-NGE2-ZERO-BOUND", conditional_inference, "premise_input"),
        ("CLM-NGE2-MPO3A-FULL-RELAY", conditional_inference, "premise_input"),
        ("DEF-NGE2-MPO3A-SELFCONSISTENCY", conditional_inference, "definition_input"),
        (conditional_inference, conditional_claim, "inference_input"),
        (conditional_claim, restricted_inference, "premise_input"),
        ("CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10", restricted_inference, "premise_input"),
        (restricted_inference, restricted_claim, "inference_input"),
        ("GOAL-NGE2-MPO3A-CONT2", attempt, "target_input"),
    ]
    operations = [{"op": "add_node", "node": item} for item in new_nodes]
    operations.extend(
        {"op": "add_edge", "source": source, "target": target, "role": role}
        for source, target, role in edges
    )

    candidate = json.loads(json.dumps(blueprint))
    candidate["nodes"].extend(new_nodes)
    candidate["edges"].extend(
        {"source": source, "target": target, "role": role}
        for source, target, role in edges
    )
    current_hashes = semantic_hashes(blueprint)
    closure = incoming_closure(candidate, new_ids) - new_ids
    read_set = {node_id: current_hashes[node_id] for node_id in sorted(closure)}
    if len(read_set) != 54:
        raise SystemExit(f"unexpected read-set closure size: {len(read_set)}")

    common_boundaries = [
        "Covers every finite R>1, integer n>=2, mu>1 and either relay orientation only conditionally on one uniform strict local derivative orientation at every premise-complete root.",
        "R=1, mu=1, and q=1 are outside the strict domain; no q-endpoint sign or root-existence assertion is used.",
        "Nonzero grazing is excluded by strict negative energy; joint event collisions and terminal event-pair closures remain in the global domain and are treated as negative-side contacts.",
        "The theorem proves no local twist sign for arbitrary min n or mu, no equal-norm result, and no O3a conclusion.",
    ]
    proposal = {
        "schema_version": "2.2",
        "submission_id": SUBMISSION_ID,
        "author_agent_id": AUTHOR,
        "run_id": RUN_ID,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "base_blueprint_hash": base_blueprint_hash,
        "base_inventory_hash": base_inventory_hash,
        "supersedes": None,
        "summary": "Add an audited either-orientation conditional local-sign-to-global-order theorem, specialize it with trusted R10 to the unconditional min n=2, mu=2 at-most-one/reflection theorem, and retain the larger min program as a partial attempt without modifying protected canonical nodes.",
        "operations": operations,
        "inventory_operations": [],
        "write_set": {
            "existing_nodes": {},
            "new_node_ids": [
                conditional_inference,
                conditional_claim,
                restricted_inference,
                restricted_claim,
                attempt,
            ],
            "inventory_rows": {},
        },
        "read_set": {"upstream_nodes": read_set},
        "rationale": {
            "research_status": "rigorous_restricted_theorem_with_reusable_conditional_bridge_and_universal_target_open",
            "scope": "The conditional theorem covers either relay orientation at fixed finite R>1, n>=2, mu>1 only under one uniform strict local q-derivative orientation. Trusted R10 discharges that hypothesis only for min n=2, mu=2, yielding global at-most-one and reflection fixing there. Existence, general min mu or n, equal norm, and O3a remain open.",
            "duplicate_policy": "The protected R9 max global-order theorem is one positive-sign instance of the new reusable implication; it is not changed. The protected R10 theorem is pointwise local and is an upstream premise for the new downstream min global corollary. No existing obligation or incoming protected dependency is changed.",
            "computation_policy": "No numerical or external-source result enters the proof. The package is exact analytic mathematics.",
            "audit_policy": f"The derivation {PROOF_SHA}, author self-audit {SELF_AUDIT_SHA}, and independent APPROVE audit {INDEPENDENT_AUDIT_SHA} are bound exactly.",
            "novelty_policy": "unknown; no priority claim",
        },
        "evidence_refs": [
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/problem_contract.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/derivation.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/self_audit.md",
            "../runs/R-20260812T165103Z-mpo3a-cont4/routes/r11_min_mu2_global_order/independent_audit.md",
        ],
        "review_evidence": {
            "logic_justifications": [],
            "method_matches": [],
            "literature_sources": [],
            "math_premise_contracts": [
                {
                    "node_id": "HYP-NGE2-DOMAIN",
                    "premise_kind": "problem_hypothesis",
                    "scope": "Every finite real R>1 and integer n>=2 in the accepted adjacent-gap problem.",
                    "contract_explanation": "Supplies the ambient R,n domain only. The proof introduces mu>1 and q>1 in the relay IVP and makes no existence or uniqueness assumption.",
                },
                {
                    "node_id": "CLM-NGE2-ZERO-BOUND",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "One-dimensional weighted Dirichlet Sturm zero count for consecutive modes in the accepted coefficient class.",
                    "contract_explanation": "Supports scalar nodal indexing and consecutive-mode interpretation. Relay-zero transversality, word continuity, and the exact 2n event count are proved in the package.",
                },
                {
                    "node_id": "CLM-NGE2-MPO3A-FULL-RELAY",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "Finite R>1, n>=2, either relay sign, and the exact two-scalar full-relay common-terminal formulation.",
                    "contract_explanation": "Supplies the relay model, indexed common-terminal residual, and accepted physical correspondence. The package independently proves its global q>1 IVP and automatic premise completeness at residual zeros.",
                },
                {
                    "node_id": "DEF-NGE2-MPO3A-SELFCONSISTENCY",
                    "premise_kind": "definition_contract",
                    "scope": "Max/min material assignment by the sign of S, effective switch convention, and the exactly 2n-event self-consistent class.",
                    "contract_explanation": "Fixes relay-sign terminology and a.e. event conventions; it is not a truth-bearing local-sign or existence premise.",
                },
                {
                    "node_id": conditional_claim,
                    "premise_kind": "newly_proved_mathematical_claim",
                    "scope": "Either relay orientation, fixed finite R>1, n>=2, mu>1, conditional on a common strict orientation of all local root derivatives.",
                    "contract_explanation": "The restricted inference uses this new proved implication only after specializing to min n=2, mu=2; it does not treat the conditional hypothesis as generally established.",
                },
                {
                    "node_id": "CLM-NGE2-MPO3A-MIN-N2-MU2-TWIST-R10",
                    "premise_kind": "established_mathematical_claim",
                    "scope": "Every arbitrary possibly asymmetric premise-complete transverse common-terminal min root at finite R>1, n=2, mu=2.",
                    "contract_explanation": "Supplies exactly partial_q A_2^c<0 in the permanent-scaling quotient and assumes neither reflection nor global order. Automatic root completeness and chamber/global derivative equality are established in the R11 package.",
                },
            ],
            "math_proof_justifications": [
                {
                    "node_id": conditional_inference,
                    "ordered_steps": [
                        "Conserve E=P^2-Q^2+rho S=1-q^2<0 across every relay event. This excludes nonjoint tangency; a joint zero has a strict punctured S<0 neighborhood and coefficient rho_-.",
                        "Construct the unique cellwise relay IVP and exclude finite Zeno accumulation by the complete zero classification and Rolle's theorem.",
                        "Use compactness and the surviving energy identity at limit zeros to prove word-independent continuous dependence in q through event birth, death, and collision.",
                        "Use the lifted phase inequality and scalar-zero simplicity to construct one globally continuous indexed residual A_n(mu,q) on all q>1.",
                        "At each residual zero, consecutive Dirichlet indexing, strict interlacing, and the Wronskian sign show that V/U crosses both relay levels exactly once on each U nodal cell, giving exactly 2n transverse active events and automatic premise completeness.",
                        "Continue the final rho_- chamber across the terminal joint contact. The coefficient mismatch acts over O(|delta|) time on positions O(|delta|), so zero-time errors are O(delta^2) and partial_q A_n=partial_q A_n^c.",
                        "Apply the same-oriented-zero lemma to sigma A_n. At-most-one follows across all chambers and closures; reflection produces another root and therefore must fix the unique root and trajectory.",
                    ],
                    "boundary_cases": common_boundaries,
                    "external_results": [],
                    "proof_package_sha256": PROOF_SHA,
                    "unresolved_obligations": [],
                },
                {
                    "node_id": restricted_inference,
                    "ordered_steps": [
                        "Specialize the conditional theorem to the min relay with rho_-=R, rho_+=1, n=2, and mu=2.",
                        "The conditional theorem itself proves that every global A_2(2,q) zero has exactly four active transverse events, both endpoint cells negative, and no interior joint zero, so it lies in trusted R10's arbitrary-asymmetric premise-complete scope.",
                        "Trusted R10 gives the smooth-chamber quotient derivative partial_q A_2^c<0 without reflection. Terminal softness proves that it equals the global derivative even at a terminal event-pair closure.",
                        "Set sigma=-1 in the conditional global-order theorem to obtain at most one q>1 root. Reflecting a root yields another root of the same global residual, so at-most-one and IVP uniqueness give reflection fixing.",
                    ],
                    "boundary_cases": [
                        "Covers every finite R>1 only at min n=2, mu=2, including arbitrary asymmetric premise-complete roots; no reflection premise is used.",
                        "The n=2 endpoint case contains two U nodal cells and exactly four active events, with no nonexistent interior-cell induction.",
                        "R=1, q=1, mu!=2, n>2, nontransverse roots, and positive-length-cell degeneracies are outside the strict local theorem; terminal pair closures are included by softness.",
                        "No root existence, q-endpoint sign, equal norm, general min order, min O3a, or universal O3a is asserted.",
                    ],
                    "external_results": [],
                    "proof_package_sha256": PROOF_SHA,
                    "unresolved_obligations": [],
                },
            ],
            "math_refutations": [],
            "math_research_state_records": [
                {
                    "node_id": attempt,
                    "record_kind": "partial_attempt",
                    "status_justification": "The route proves the reusable conditional local-to-global bridge and closes min n=2, mu=2 global at-most-one/reflection via trusted R10. Root existence, arbitrary mu, n>2, equal-norm orientation, and O3a remain open, and the general-n dual-Jacobi route has not established the needed local sign.",
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
                "new_node_count": len(new_nodes),
                "edge_count": len(edges),
                "read_set_count": len(read_set),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
