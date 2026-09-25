import Counterexamples
open AuditRound10
namespace Reviewer
theorem exact_negation_flip_not_projection : ¬ ((-J 1) ((-J 1) (fun _ => (1 : ℝ))) =
    (-J 1) (fun _ => (1 : ℝ))) := AuditRound10Controls.flip_not_projection
theorem exact_negation_reflection_plus_sign_false : ¬ (reflect ((0 : Vec 1) + (fun _ => (1 : ℝ))) =
    reflect (0 : Vec 1) + J 1 (fun _ => (1 : ℝ))) := AuditRound10Controls.reflection_plus_sign_false
theorem exact_negation_phase_off_by_one_false : ¬ (phase_root (fun x : ℝ => x) 1 (2 * Real.pi)) := AuditRound10Controls.phase_off_by_one_false
end Reviewer
