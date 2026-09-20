import SL.AuditRound2
import SL.ThirdOrderClosedForms
import SL.BalancedPhase

/-! Author-only compatibility checks against existing compiled SL modules.
These equations connect formulas, not the unproved full spectral theorems. -/
namespace AuditRound2SourceBridge

theorem recurrence_interface {K : Type*} [Field K] (a1 a2 a3 v : ℕ → K) :
    SL.AuditRound2.third_order_solution a1 a2 a3 v =
      SL.ThirdOrder.IsSolution a1 a2 a3 v := rfl

theorem p_at_one (j : ℕ) :
    SL.AuditRound2.k1_p j = SL.ThirdOrderClosedForms.PEven 1 j := by
  simp [SL.AuditRound2.k1_p, SL.ThirdOrderClosedForms.PEven]

theorem q_at_one (j : ℕ) :
    SL.AuditRound2.k1_q j = SL.ThirdOrderClosedForms.QEven 1 j := by
  simp [SL.AuditRound2.k1_q, SL.ThirdOrderClosedForms.QEven]

theorem r_at_one (j : ℕ) :
    SL.AuditRound2.k1_r j = SL.ThirdOrderClosedForms.REven 1 j := rfl

theorem theta_identity (s : ℝ) :
    SL.AuditRound2.candidate_theta s = SL.BalancedPhase.theta s := rfl

end AuditRound2SourceBridge

set_option pp.proofs false
set_option pp.universes true
#print SL.ThirdOrder.IsSolution
#print SL.ThirdOrderClosedForms.PEven
#print SL.ThirdOrderClosedForms.QEven
#print SL.ThirdOrderClosedForms.REven
#print SL.BalancedPhase.theta
#print AuditRound2SourceBridge.recurrence_interface
#print axioms AuditRound2SourceBridge.recurrence_interface
#print AuditRound2SourceBridge.p_at_one
#print axioms AuditRound2SourceBridge.p_at_one
#print AuditRound2SourceBridge.q_at_one
#print axioms AuditRound2SourceBridge.q_at_one
#print AuditRound2SourceBridge.r_at_one
#print axioms AuditRound2SourceBridge.r_at_one
#print AuditRound2SourceBridge.theta_identity
#print axioms AuditRound2SourceBridge.theta_identity
