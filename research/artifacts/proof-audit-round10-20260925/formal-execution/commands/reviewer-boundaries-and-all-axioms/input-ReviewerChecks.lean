import Lean
import AuditRound10
open Lean Elab Command Meta
open AuditRound10

set_option maxRecDepth 100000
set_option maxHeartbeats 0

namespace Reviewer

def anti : Vec 1 := fun i => if i.val = 0 then 1 else -1

theorem anti_eigen : J 1 anti = -anti := by
  funext i
  have hi : i.val = 0 ∨ i.val = 1 := by omega
  rcases hi with hi | hi <;> simp [J, anti, Fin.val_rev, hi]

theorem nontrivial_projections :
    P_preserve 1 anti = anti ∧ P_break 1 anti = 0 ∧
    P_preserve 1 (fun _ => (1 : ℝ)) = 0 ∧ P_break 1 (fun _ => (1 : ℝ)) = (fun _ => (1 : ℝ)) := by
  have h := (projection_fixed_iff anti).1.mpr anti_eigen
  refine ⟨h, ?_, ?_, ?_⟩
  · rw [← h]
    exact (projection_annihilation anti).2
  · funext i
    norm_num [P_preserve, J]
  · funext i
    norm_num [P_break, J]

theorem dimension_zero (x : Vec 0) : reflect x = x := by
  funext i
  exact Fin.elim0 i

theorem zero_level_degenerate :
    ∃! x : ℝ, x ∈ Set.Icc 0 0 ∧ phase_root (fun y : ℝ => y) 0 x := by
  apply bracket_unique_root continuous_id.continuousOn strictMono_id.strictMonoOn
  all_goals norm_num

theorem positive_level_degenerate :
    ∃! x : ℝ, x ∈ Set.Icc Real.pi Real.pi ∧ phase_root (fun y : ℝ => y) 1 x := by
  apply bracket_unique_root continuous_id.continuousOn strictMono_id.strictMonoOn
  · exact Real.pi_pos.le
  all_goals norm_num

theorem nonconsecutive_example :
    ∃ roots : ℕ → ℝ, (∀ m, phase_root (fun y : ℝ => y) (2*m) (roots m)) ∧
      StrictMono roots := by
  refine ⟨fun m => ((2*m : ℕ) : ℝ) * Real.pi, ?_, ?_⟩
  · intro m
    constructor
    · positivity
    · rfl
  · apply indexed_roots_strict_mono strictMono_id.strictMonoOn (fun m => 2*m)
    · intro a b hab
      omega
    · intro m
      constructor
      · positivity
      · rfl

end Reviewer

elab "#audit_all " out:str : command => do
  let env := (← getEnv).setExporting false
  let names := env.constants.toList.map Prod.fst |>.filter (fun n => n.toString.startsWith "AuditRound10.")
  let mut rows := #[]
  for name in names.mergeSort (fun a b => a.toString ≤ b.toString) do
    let some info := env.checked.get.find? name | continue
    let ax ← collectAxioms name
    let typ ← liftTermElabM <| withOptions
      (fun o => o.setBool `pp.explicit false |>.setBool `pp.all false |>.setBool `pp.universes true |>.setNat `pp.maxSteps 10000000 |>.setBool `pp.deepTerms true)
      (do return (← ppExpr info.type).pretty)
    rows := rows.push <| Json.mkObj [("name", toJson name.toString), ("unsafe",toJson info.isUnsafe), ("axioms",toJson (ax.map Name.toString)), ("type",toJson typ)]
  IO.FS.writeFile out.getString ((Json.arr rows).pretty ++ "\n")

#audit_all "F:\\tools\\math-audit-round10-20260925\\formal-reviewer\\independent-35c0ed5b7a9f\\evidence\\all-declaration-audit.json"
