import AuditRound10
open AuditRound10

namespace AuditRound10Controls

theorem flip_not_projection :
    (-J 1) ((-J 1) (fun _ => (1 : ℝ))) ≠ (-J 1) (fun _ => (1 : ℝ)) := by
  intro h
  have hi := congrFun h (0 : Fin (2 * 1))
  norm_num [J] at hi

theorem reflection_plus_sign_false :
    reflect ((0 : Vec 1) + (fun _ => (1 : ℝ))) ≠
      reflect (0 : Vec 1) + J 1 (fun _ => (1 : ℝ)) := by
  intro h
  have hi := congrFun h (0 : Fin (2 * 1))
  norm_num [reflect, J] at hi

theorem phase_off_by_one_false : ¬phase_root (fun x : ℝ => x) 1 (2 * Real.pi) := by
  intro h
  have he := h.2
  norm_num at he

end AuditRound10Controls
