import LeanVerifyProbe
import AuditRound10
set_option maxRecDepth 100000
set_option maxHeartbeats 0
axiom LeanVerifyV2.expected_statement : (∀ {n : ℕ} (u v : AuditRound10.Vec n) (a : ℝ),
(AuditRound10.J n (u + v) = AuditRound10.J n u + AuditRound10.J n v) ∧ (AuditRound10.J n (a • v) = a • AuditRound10.J n v) ∧
    (AuditRound10.P_preserve n (u + v) = AuditRound10.P_preserve n u + AuditRound10.P_preserve n v) ∧
    (AuditRound10.P_preserve n (a • v) = a • AuditRound10.P_preserve n v) ∧
    (AuditRound10.P_break n (u + v) = AuditRound10.P_break n u + AuditRound10.P_break n v) ∧
    (AuditRound10.P_break n (a • v) = a • AuditRound10.P_break n v)) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n) (i : Fin (2 * n)),
AuditRound10.J n v i = v ⟨2 * n - 1 - i.val, by omega⟩) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.J n (AuditRound10.J n v) = v) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n) (i : Fin (2 * n)),
AuditRound10.P_preserve n v i = (v i - v i.rev) / 2 ∧
    AuditRound10.P_break n v i = (v i + v i.rev) / 2) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.J n (AuditRound10.P_preserve n v) = -AuditRound10.P_preserve n v) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.J n (AuditRound10.P_break n v) = AuditRound10.P_break n v) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.P_preserve n v + AuditRound10.P_break n v = v) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.P_preserve n (AuditRound10.P_preserve n v) = AuditRound10.P_preserve n v ∧
    AuditRound10.P_break n (AuditRound10.P_break n v) = AuditRound10.P_break n v) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
AuditRound10.P_preserve n (AuditRound10.P_break n v) = 0 ∧
    AuditRound10.P_break n (AuditRound10.P_preserve n v) = 0) ∧
(∀ {n : ℕ} (v : AuditRound10.Vec n),
(AuditRound10.P_preserve n v = v ↔ AuditRound10.J n v = -v) ∧
    (AuditRound10.P_break n v = v ↔ AuditRound10.J n v = v)) ∧
(∀ {n : ℕ} (u v : AuditRound10.Vec n),
dotProduct (AuditRound10.J n u) (AuditRound10.J n v) = dotProduct u v) ∧
(∀ {n : ℕ} (u v : AuditRound10.Vec n),
dotProduct (AuditRound10.P_preserve n u) (AuditRound10.P_break n v) = 0) ∧
(∀ {n : ℕ} (x : AuditRound10.Vec n),
AuditRound10.reflect (AuditRound10.reflect x) = x) ∧
(∀ {n : ℕ} (x v : AuditRound10.Vec n) (t : ℝ),
AuditRound10.reflect (x + t • v) = AuditRound10.reflect x - t • AuditRound10.J n v) ∧
(∀ {n : ℕ} (x u v : AuditRound10.Vec n) (t : ℝ)
    (hx : AuditRound10.reflect x = x),
AuditRound10.reflect (x + t • (AuditRound10.P_preserve n u + AuditRound10.P_break n v)) =
      x + t • (AuditRound10.P_preserve n u - AuditRound10.P_break n v)) ∧
(∀ {n : ℕ} (x v : AuditRound10.Vec n)
    (hx : AuditRound10.reflect x = x),
AuditRound10.reflect (x + v) = x + v ↔ AuditRound10.J n v = -v) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {k : ℕ} {x y : ℝ}
    (hx : AuditRound10.phase_root Phi k x) (hy : AuditRound10.phase_root Phi k y),
x = y) ∧
(∀ {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (k : ℕ) (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b)
    (hl : Phi a ≤ (k : ℝ) * Real.pi) (hr : (k : ℝ) * Real.pi ≤ Phi b),
∃! x : ℝ, x ∈ Set.Icc a b ∧ AuditRound10.phase_root Phi k x) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) {j k : ℕ} {x y : ℝ}
    (hx : AuditRound10.phase_root Phi j x) (hy : AuditRound10.phase_root Phi k y),
(x < y ↔ j < k)) ∧
(∀ {Phi : ℝ → ℝ}
    (hm : StrictMonoOn Phi (Set.Ici 0)) (index : ℕ → ℕ) (roots : ℕ → ℝ)
    (hi : StrictMono index) (hr : ∀ m, AuditRound10.phase_root Phi (index m) (roots m)),
StrictMono roots) ∧
(∀ {Phi : ℝ → ℝ}
    (hc : ContinuousOn Phi (Set.Ici 0))
    (hm : StrictMonoOn Phi (Set.Ici 0))
    (index : ℕ → ℕ) (hi : StrictMono index) (left right : ℕ → ℝ)
    (hleft : ∀ m, 0 ≤ left m) (horder : ∀ m, left m ≤ right m)
    (hl : ∀ m, Phi (left m) ≤ (index m : ℝ) * Real.pi)
    (hr : ∀ m, (index m : ℝ) * Real.pi ≤ Phi (right m)),
∃ roots : ℕ → ℝ,
      (∀ m, roots m ∈ Set.Icc (left m) (right m) ∧ AuditRound10.phase_root Phi (index m) (roots m)) ∧
      StrictMono roots)
#lean_verify_v2 AuditRound10.root expected LeanVerifyV2.expected_statement output "F:\\tools\\math-audit-round10-20260925\\formal-author\\evidence\\exact-root-01\\lean-verification-runs\\b29525305d2d46d1a1e9be63bb6bff7e\\declaration.json"
