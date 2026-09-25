from pathlib import Path
import json
Base=Path(__file__).resolve().parent
Project=Base/'project'
Common='import AuditRound11\nopen scoped Matrix\nopen AuditRound11\n'
Sources={
'PositiveControls.lean':'''example : (Matrix.fromBlocks (0 : Square 1) 1 1 (0 : Square 1)).det = -1 := by
  rw [off_diagonal_determinant]
  norm_num
example : (Matrix.fromBlocks (0 : Square 0) 1 1 (0 : Square 0)).det = 1 := by
  rw [off_diagonal_determinant]
  norm_num
example : parity_sign 1 * reversal 1 = -(reversal 1 * parity_sign 1) := by
  simp [parity_sign, reversal, Matrix.fromBlocks_multiply, Matrix.fromBlocks_neg]
example : (boundary_even 4).det = 336 ∧ (boundary_odd 4).det = 432 := by
  norm_num [boundary_even, boundary_odd, Matrix.det_fin_two]
example : (boundary_even 0).det = 0 ∧ (boundary_odd 0).det = 0 := by
  norm_num [boundary_even, boundary_odd, Matrix.det_fin_two]
example (L : ℕ) (h : 4 ≤ L) (b : PairIndex 2 → ℝ) :
    ∃! a, boundary_full (L : ℝ) *ᵥ a = b := (boundary_correction L h).2 b
example (x v : PairIndex 3 → ℝ) (h : reversal 3 *ᵥ v = v) :
    physical_reflection (x + v) - physical_reflection x = -v :=
  (reflection_parity x v).2.mpr h
''',
'NegativeDeterminantSign.lean':'''example : (Matrix.fromBlocks (0 : Square 1) 1 1 (0 : Square 1)).det = 1 := by
  rw [off_diagonal_determinant]
  norm_num
''',
'NegativeDiagonalBlocks.lean':'''example (hwrong : ∀ J : PairedMatrix 1,
    J * reversal 1 = -(reversal 1 * J) →
    J.det = (parity_matrix J).toBlocks₁₁.det * (parity_matrix J).toBlocks₂₂.det) :
    False := by
  have ha : parity_sign 1 * reversal 1 = -(reversal 1 * parity_sign 1) := by
    simp [parity_sign, reversal, Matrix.fromBlocks_multiply, Matrix.fromBlocks_neg]
  have hz := anticommuting_blocks (parity_sign 1) ha
  have he := hwrong (parity_sign 1) ha
  rw [hz.1, hz.2] at he
  norm_num [parity_sign, Matrix.det_fromBlocks_zero₂₁, Matrix.det_neg] at he

example : ∀ J : PairedMatrix 1, J * reversal 1 = -(reversal 1 * J) →
    J.det = (parity_matrix J).toBlocks₁₁.det * (parity_matrix J).toBlocks₂₂.det := by
  intro J h
  rw [(anticommuting_blocks J h).1, (anticommuting_blocks J h).2]
  norm_num
''',
'NegativeBoundaryFormula.lean':'''example : (boundary_even 4).det = 2 * 4 * (4 + 2) * (2 * 4 + 1) := by
  norm_num [boundary_even, Matrix.det_fin_two]
''',
'NegativePhysicalSign.lean':'''example : physical_reflection (fun _ : PairIndex 1 => (1 : ℝ)) -
    physical_reflection (fun _ : PairIndex 1 => (0 : ℝ)) = (fun _ => (1 : ℝ)) := by
  ext i
  cases i <;>
    simp [physical_reflection, reversal, Matrix.mulVec, dotProduct,
      Fintype.sum_sum_type, Matrix.fromBlocks, Matrix.one_apply]
'''
}
for Name,Text in Sources.items():
	(Project/Name).write_text(Common+Text)
Control=Base/'closure-control-project'
Control.mkdir(exist_ok=True)
(Control/'lean-toolchain').write_text('leanprover/lean4:v4.31.0\n')
(Control/'ClosureControl.lean').write_text('namespace Round11Control\naxiom hidden : False\ndef hiddenProp : Prop := hidden.elim\ntheorem contaminated : hiddenProp := hidden.elim\ntheorem valid : True := True.intro\nend Round11Control\n')
for Name,Declaration,Type in [('positive','Round11Control.valid','True'),('hidden-axiom','Round11Control.contaminated','Round11Control.hiddenProp'),('wrong-type','Round11Control.valid','False'),('missing-target','Round11Control.missing','True')]:
	(Base/f'control-{Name}.json').write_text(json.dumps({'file':'ClosureControl.lean','declaration':Declaration,'expected_type':Type,'universes':[]},indent=2)+'\n')
print('prepared controls')
