import LeanVerifyProbe
import AuditRound12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : open scoped Matrix in open AuditRound12 in (
(∀ (n : ℕ),
(∀ i : Fin n, (order n (Sum.inl i)).val = i.val ∧
      (order n (Sum.inr i)).val = n+n-1-i.val) ∧
    (∀ i : Pair n, order n (Sum.swap i) = (order n i).rev) ∧
    (∀ i : Pair n, sign n i = (-1 : ℝ) ^ (order n i).val) ∧
    paired (orderedP n) = P n ∧ paired (orderedS n) = S n) ∧
(∀ (n : ℕ),
P n * P n = 1 ∧ E n * E n = 1 ∧ S n * S n = 1 ∧
    (P n)ᵀ = P n ∧ (E n)ᵀ = E n ∧ (S n)ᵀ = S n) ∧
(∀ (n : ℕ),
P n * Be n = Be n ∧ P n * Bo n = -Bo n ∧
    (Be n)ᵀ * Be n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Bo n)ᵀ * Bo n = (2 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) ∧
    (Be n)ᵀ * Bo n = 0 ∧
    S n * Be n = Bo n * E n ∧ S n * Bo n = Be n * E n) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
KpOdd K = E n * rawKe K * E n ∧
    KpEven K = E n * rawKo K * E n) ∧
(∀ {n : ℕ} (K : Matrix (Fin (n+n)) (Fin (n+n)) ℝ),
(orderedBe n)ᵀ * K * orderedBe n = rawKe (paired K) ∧
    (orderedBo n)ᵀ * K * orderedBo n = rawKo (paired K) ∧
    (orderedBo n)ᵀ * (orderedS n * K * orderedS n) * orderedBo n =
      E n * ((orderedBe n)ᵀ * K * orderedBe n) * E n ∧
    (orderedBe n)ᵀ * (orderedS n * K * orderedS n) * orderedBe n =
      E n * ((orderedBo n)ᵀ * K * orderedBo n) * E n) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
(normalizedBe n)ᵀ * normalizedBe n = 1 ∧
    (normalizedBo n)ᵀ * normalizedBo n = 1 ∧
    (normalizedBe n)ᵀ * K * normalizedBe n = (1/2 : ℝ) • rawKe K ∧
    (normalizedBo n)ᵀ * K * normalizedBo n = (1/2 : ℝ) • rawKo K) ∧
(∀ {n : ℕ} (v : Fin n → ℝ),
rawKo (outer (oddVector v)) = (4 : ℝ) • outer v ∧
    rawKe (outer (oddVector v)) = 0 ∧
    KpOdd (outer (oddVector v)) = 0 ∧
    (v ≠ 0 → rawKo (outer (oddVector v)) ≠ 0)) ∧
(∀ {n : ℕ} (K : Matrix (Pair n) (Pair n) ℝ),
(-S n) * K * (-S n) = Kp K ∧
    (-S n) * Be n = Bo n * (-E n) ∧
    (-S n) * Bo n = Be n * (-E n) ∧
    (normalizedBo n)ᵀ * Kp K * normalizedBo n =
      E n * ((normalizedBe n)ᵀ * K * normalizedBe n) * E n ∧
    (normalizedBe n)ᵀ * Kp K * normalizedBe n =
      E n * ((normalizedBo n)ᵀ * K * normalizedBo n) * E n) ∧
(∃ K : Matrix (Pair 1) (Pair 1) ℝ,
      Kᵀ = K ∧ P 1 * K = K * P 1 ∧ rawKo K ≠ KpOdd K)
)
#lean_verify_v2 AuditRound12.audit_root expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round12-20260926\\formal-author\\evidence\\exact-root\\lean-verification-runs\\950bd52b7f1e47d4bc1904aad1c5f4a1\\declaration.json"
