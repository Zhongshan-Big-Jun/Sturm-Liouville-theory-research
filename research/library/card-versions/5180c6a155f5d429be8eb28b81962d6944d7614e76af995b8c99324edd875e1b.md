---
{"author_ids": ["01a0cd06-5c53-7572-aa00-e55c12964b1f", "01a06f46-dd03-7c83-9267-32048412c359"], "conditions": ["Dirichlet [0,1]; finitely many fixed real block values in [m,M] with m>0", "C2 interface path stays in the open ordered simplex; no collisions and positive local block-width lower bound", "Fixed simple eigenvalue index; real eigenfunction weighted norm integral rho u^2=1 and u_prime(0)>0", "Use the pencil Laurent finite-part Green kernel with dx forcing and weighted zero gauge; not the ordinary L2 orthogonal inverse", "Additional mass, tangency or other feasibility constraints must be imposed separately"], "created": "2026-09-23", "evidence": [{"locator": "Per-claim scope and limitations", "path": "research/artifacts/literature-absorption-20260923/reviews/interfaces/runtime/report.json", "sha256": "2d1715c9e70ffabb070309951095607336b50e689efac7becd921d8a2ff40a3f"}, {"locator": "Native call and exact input identities; private primary-source availability", "path": "research/artifacts/literature-absorption-20260923/reviews/interfaces/provenance.json", "sha256": "262e2c35376c4e081786967c0caf25e208db59dd6404c6ec2efe066bfc6bf4d6"}, {"locator": "Exact proposed card reviewed independently", "path": "literature/absorption-20260923/interfaces/cards/P3-bounded-interface-chain-rule.json", "sha256": "b3f7a76670dc4aa09b322b77a03d53bd168bc036018c548b34a7e9d83d828113"}], "evidence_status": "INDEPENDENT_ANALYTIC_REVIEW_APPROVED_WITH_DECLARED_LIMITS", "integration_status": "ACTIVE_SCOPED_REVIEW; REVALIDATE_EACH_APPLICATION", "review_status": {"packet_sha256": "e7e17f4fdd4036aa5c1b0f1a93e804eb49a8e80fb020e74431da1883355cd9a6", "report": "research/artifacts/literature-absorption-20260923/reviews/interfaces/runtime/report.json", "reviewer_id": "01a0cd1d-8ccf-7b91-9cfc-7cc51936aa0a", "scope": "Exact original mathematical content and source mapping; no complete Lean formalization or canonical acceptance", "verdict": "APPROVED"}, "scope": "Theorem P is an author-proved local result for this finite family. Beyond it, differentiability, weak product rules and inverse mapping hypotheses remain conditional. No global inertia or optimization classification.", "sources": [{"authorship": "original author derivation or source adaptation, not independently accepted", "locator": "Theorem P, (P1)-(P9) and proof", "path": "literature/absorption-20260923/interfaces/derivations/P3-interface-chain-rule.md", "sha256": "92eba63b76df55ea4280ff78de20b47d1a6941e3daeb69c21be0a9b0a78b77c6"}, {"authorship": "original author derivation or source adaptation, not independently accepted", "locator": "C1-C6 and actual execution", "path": "literature/absorption-20260923/interfaces/derivations/calibrations.md", "sha256": "1d568b2149ddf54ece55b5d761a34fe5a93f0e549b7236ec6f52b632173514c9"}, {"locator": "V1-V4", "path": "research/artifacts/proof-audit-round9-20260923/analytic-repair.md", "sha256": "cb26b534c5a163d6409de3393db6c79bdb73fc6a5ea7a2036d52e44ea4bb9be0"}, {"locator": "39 executed author checks; not independent acceptance", "path": "literature/absorption-20260923/interfaces/evidence/run-20260923T070250443181Z/stdout.json", "sha256": "df1b01c80717ebc569cf70d7ff190ce7ff7fdd0d274440fe87dff86966adee58"}], "structured_content": {"A": "pairing(mu,u_k^2)", "B": "pairing(eta,u_k^2)", "E": "double integral u_k(x) Gtilde_k(x,y) u_k(y) dmu(x)dmu(y)", "eigenvalue_second": "2 lambda_k A^2-2 lambda_k^2 E-lambda_k B", "eta": "sum s_i d_i^2 delta_prime_(a_i)-sum s_i e_i delta_(a_i)", "exact_calibration": "c_left=1,c_right=4,a=1/2; theta=acos(1/sqrt(3)); w1=2theta,w2=2(pi-theta); lambda_a=2lambda, lambda_aa=6lambda+(3/2)w^3 tan(w/2)", "gap_second": "Hbar_(n+1)(mu,mu)-Hbar_n(mu,mu)-sum s_i[d_i^2 f_prime(a_i)+e_i f(a_i)]", "half_gap": "Q_path=gap_second/2, including every acceleration term", "mu": "-sum s_i d_i delta_(a_i)", "normalized_derivative": "v=-(A/2)u_k+lambda_k integral Gtilde_k(x,y)u_k(y)dmu(y)", "regularity_proved": "Eigenvalue analytic in interface positions; eigenfunction once differentiable in H0^1 and uniformly in x; v_prime can jump", "review_boundary": "Analytic proof and numerical author checks await independent acceptance. L10 bridge, general measure paths, G1 prime and uniqueness remain open."}, "summary": "A local transfer-matrix proof gives weighted-normalized eigenfunction derivatives and the complete interface chain rule, including finite geometric and path-acceleration terms. Exact single-interface and atomic benchmarks calibrate the signs and half-gap factor.", "title": "Second derivative along finite noncolliding fixed-density interfaces", "tool_id": "finite-interface-second-derivative", "updated": "2026-09-23"}
---
## mu

-sum s_i d_i delta_(a_i)

## eta

sum s_i d_i^2 delta_prime_(a_i)-sum s_i e_i delta_(a_i)

## A

pairing(mu,u_k^2)

## B

pairing(eta,u_k^2)

## E

double integral u_k(x) Gtilde_k(x,y) u_k(y) dmu(x)dmu(y)

## normalized_derivative

v=-(A/2)u_k+lambda_k integral Gtilde_k(x,y)u_k(y)dmu(y)

## eigenvalue_second

2 lambda_k A^2-2 lambda_k^2 E-lambda_k B

## gap_second

Hbar_(n+1)(mu,mu)-Hbar_n(mu,mu)-sum s_i[d_i^2 f_prime(a_i)+e_i f(a_i)]

## half_gap

Q_path=gap_second/2, including every acceleration term

## regularity_proved

Eigenvalue analytic in interface positions; eigenfunction once differentiable in H0^1 and uniformly in x; v_prime can jump

## exact_calibration

c_left=1,c_right=4,a=1/2; theta=acos(1/sqrt(3)); w1=2theta,w2=2(pi-theta); lambda_a=2lambda, lambda_aa=6lambda+(3/2)w^3 tan(w/2)

## review_boundary

Analytic proof and numerical author checks await independent acceptance. L10 bridge, general measure paths, G1 prime and uniqueness remain open.
