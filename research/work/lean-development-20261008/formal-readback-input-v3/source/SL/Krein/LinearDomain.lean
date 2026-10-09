import SL.Krein.PolynomialBridge

   
                                                     

                                                                              
                                                                              
                                                                            
  

namespace SL.Krein

open MeasureTheory Set Filter

noncomputable section

def add_rep (R S : IntegralRepresentative) : IntegralRepresentative where
  Value := R.Value + S.Value
  First := R.First + S.First
  Second := R.Second + S.Second
  ValueContinuous := R.ValueContinuous.add S.ValueContinuous
  FirstContinuous := R.FirstContinuous.add S.FirstContinuous
  SecondMemLp := R.SecondMemLp.add S.SecondMemLp
  ValueIntegral := by
    intro X HX
    have HR : IntervalIntegrable R.First volume (-1) X :=
      (R.FirstContinuous.mono <| Icc_subset_Icc le_rfl HX.2).intervalIntegrable_of_Icc HX.1
    have HS : IntervalIntegrable S.First volume (-1) X :=
      (S.FirstContinuous.mono <| Icc_subset_Icc le_rfl HX.2).intervalIntegrable_of_Icc HX.1
    simp only [Pi.add_apply, intervalIntegral.integral_add HR HS]
    rw [R.ValueIntegral X HX, S.ValueIntegral X HX]
    abel
  FirstIntegral := by
    intro X HX
    have HR : IntervalIntegrable R.Second volume (-1) X :=
      (SL.Analysis.mem_l2_interval_integrable (by norm_num) R.SecondMemLp).mono_set <| by
        rw [uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1), uIcc_of_le HX.1]
        exact Icc_subset_Icc le_rfl HX.2
    have HS : IntervalIntegrable S.Second volume (-1) X :=
      (SL.Analysis.mem_l2_interval_integrable (by norm_num) S.SecondMemLp).mono_set <| by
        rw [uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1), uIcc_of_le HX.1]
        exact Icc_subset_Icc le_rfl HX.2
    simp only [Pi.add_apply, intervalIntegral.integral_add HR HS]
    rw [R.FirstIntegral X HX, S.FirstIntegral X HX]
    abel

def smul_rep (A : ℂ) (R : IntegralRepresentative) : IntegralRepresentative where
  Value := A • R.Value
  First := A • R.First
  Second := A • R.Second
  ValueContinuous := R.ValueContinuous.const_smul A
  FirstContinuous := R.FirstContinuous.const_smul A
  SecondMemLp := R.SecondMemLp.const_smul A
  ValueIntegral := by
    intro X HX
    simp only [Pi.smul_apply, intervalIntegral.integral_smul]
    rw [R.ValueIntegral X HX, smul_add]
  FirstIntegral := by
    intro X HX
    simp only [Pi.smul_apply, intervalIntegral.integral_smul]
    rw [R.FirstIntegral X HX, smul_add]

theorem add_rep_to_L2 (R S : IntegralRepresentative) :
    (add_rep R S).to_L2 = R.to_L2 + S.to_L2 := by
  unfold IntegralRepresentative.to_L2 SL.Analysis.to_L2
  exact MemLp.toLp_add _ _

theorem smul_rep_to_L2 (A : ℂ) (R : IntegralRepresentative) :
    (smul_rep A R).to_L2 = A • R.to_L2 := by
  unfold IntegralRepresentative.to_L2 SL.Analysis.to_L2
  exact MemLp.toLp_const_smul _ _

theorem add_rep_boundary (R S : IntegralRepresentative) (HR : boundary R) (HS : boundary S) :
    boundary (add_rep R S) := by
  simp only [boundary, add_rep, Pi.add_apply] at HR HS ⊢
  constructor
  · rw [HR.1, HS.1]
    ring
  · rw [HR.2, HS.2]
    ring

theorem smul_rep_boundary (A : ℂ) (R : IntegralRepresentative) (HR : boundary R) :
    boundary (smul_rep A R) := by
  simp only [boundary, smul_rep, Pi.smul_apply, smul_eq_mul] at HR ⊢
  constructor
  · rw [HR.1]
    ring
  · rw [HR.2]
    ring

def domain_submodule : Submodule ℂ L2 where
  carrier := domain
  zero_mem' := by
    have H0 := polynomial_mem_domain 0 (by simp [AuditRound5.residues_apply])
    convert H0 using 1
    unfold polynomial_L2 IntegralRepresentative.to_L2 SL.Analysis.to_L2
    simp [polynomial_rep, MemLp.toLp_zero]
  add_mem' := by
    intro F G HF HG
    obtain ⟨R, HR, HB⟩ := HF
    obtain ⟨S, HS, HC⟩ := HG
    exact ⟨add_rep R S, (add_rep_to_L2 R S).trans (by rw [HR, HS]), add_rep_boundary R S HB HC⟩
  smul_mem' := by
    intro A F HF
    obtain ⟨R, HR, HB⟩ := HF
    exact ⟨smul_rep A R, (smul_rep_to_L2 A R).trans (by rw [HR]), smul_rep_boundary A R HB⟩

theorem add_rep_action (R S : IntegralRepresentative) (C : ℝ) :
    (add_rep R S).action C = R.action C + S.action C := by
  unfold IntegralRepresentative.action SL.Analysis.to_L2
  rw [← MemLp.toLp_add]
  apply MemLp.toLp_congr
  apply ae_of_all
  intro X
  simp only [add_rep, Pi.add_apply]
  ring

theorem smul_rep_action (A : ℂ) (R : IntegralRepresentative) (C : ℝ) :
    (smul_rep A R).action C = A • R.action C := by
  unfold IntegralRepresentative.action SL.Analysis.to_L2
  rw [← MemLp.toLp_const_smul]
  apply MemLp.toLp_congr
  apply ae_of_all
  intro X
  simp only [smul_rep, Pi.smul_apply, smul_eq_mul]
  ring

def operator_linear (C : ℝ) : domain_submodule →ₗ[ℂ] L2 where
  toFun F := operator C ⟨F.val, F.property⟩
  map_add' F G := by
    let R := F.property.choose
    let S := G.property.choose
    have HR : R.to_L2 = F.val := F.property.choose_spec.1
    have HS : S.to_L2 = G.val := G.property.choose_spec.1
    have HE : (add_rep R S).to_L2 = (F + G).val := by rw [add_rep_to_L2, HR, HS]; rfl
    rw [operator_eq_action C ⟨(F + G).val, (F + G).property⟩ (add_rep R S) HE]
    exact add_rep_action R S C
  map_smul' A F := by
    let R := F.property.choose
    have HR : R.to_L2 = F.val := F.property.choose_spec.1
    have HE : (smul_rep A R).to_L2 = (A • F).val := by rw [smul_rep_to_L2, HR]; rfl
    rw [operator_eq_action C ⟨(A • F).val, (A • F).property⟩ (smul_rep A R) HE]
    exact smul_rep_action A R C

theorem operator_linear_apply (C : ℝ) (F : domain_submodule) :
    operator_linear C F = operator C ⟨F.val, F.property⟩ := rfl

theorem operator_linear_add (C : ℝ) (F G : domain_submodule) :
    operator_linear C (F + G) = operator_linear C F + operator_linear C G :=
  (operator_linear C).map_add F G

theorem operator_linear_smul (C : ℝ) (A : ℂ) (F : domain_submodule) :
    operator_linear C (A • F) = A • operator_linear C F :=
  (operator_linear C).map_smul A F

end

end SL.Krein
