import LeanVerifyProbe
import SLVerified
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (∀ (p : Polynomial ℝ), SL.AuditRound5.residues p = 0 → SL.Krein.polynomial_L2 p ∈ SL.Krein.domain) ∧
    (∀ (p : Polynomial ℝ) (hp : SL.AuditRound5.residues p = 0) (c : ℝ), SL.Krein.operator c (SL.Krein.polynomial_domain p hp) = SL.Krein.polynomial_L2 (-p.derivative.derivative + Polynomial.C c * p)) ∧
    (SL.Krein.polynomial_L2 SL.AuditRound5.p_zero ∈ SL.Krein.domain ∧ SL.Krein.polynomial_L2 SL.AuditRound5.p_one ∈ SL.Krein.domain ∧ (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_even m) ∈ SL.Krein.domain) ∧ (∀ m : ℕ, 2 ≤ m → SL.Krein.polynomial_L2 (SL.AuditRound5.p_odd m) ∈ SL.Krein.domain)) ∧
    (∀ (p : Polynomial ℝ) (hp : SL.AuditRound5.residues p = 0) (c : ℝ), SL.Krein.first_linear_inner (SL.Krein.operator c (SL.Krein.polynomial_domain p hp)) (SL.Krein.polynomial_L2 p) = (((∫ x in (-1 : ℝ)..1, (p.derivative.eval x) ^ 2) + c * (∫ x in (-1 : ℝ)..1, (p.eval x) ^ 2) - (p.eval 1 - p.eval (-1)) ^ 2 / 2 : ℝ) : ℂ))
#lean_verify_v2 SLVerified.krein_polynomial_root expected LeanVerifyV2.expected_statement output "F:\\LaTeX\\BVE research\\research\\artifacts\\lean-development-20261008\\verification\\targets\\krein-polynomial\\lean-verification-runs\\812d593b74534925a5d4d73b07537898\\declaration.json"
