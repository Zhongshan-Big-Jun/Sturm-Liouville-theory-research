# Actual Lean declaration and definition readback

Generated from the completed author replay declarations.json. This is machine readback, not an independent mathematical review. Every namespace declaration, including compiler-generated auxiliaries, is retained. Explicit elaborated expressions and the complete type/body dependency graph remain in the raw JSON.

| Source SHA-256 | 3cbc7e84dab06ffdc2cc974a9d7553c47847eca4227e49024f04a1e91ccc486e |
| --- | --- |
| Replay run UUID | ec5fe5fe-5513-4a27-8a73-283b42166f2d |

## AuditRound8.B_curved_counterexample

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
LT.lt.{0} 1500 (3015 / 2) ∧
  LT.lt.{0} (3015 / 2) 1515 ∧
    LT.lt.{0} (19 / 100) (48743 / 100000) ∧
      LT.lt.{0} (48743 / 100000) (1 / 2) ∧
        LT.lt.{0} (AuditRound8.wCritical 1500) (48743 / 100000) ∧
          LT.lt.{0} (48743 / 100000) (AuditRound8.wCritical (3015 / 2))
```

## AuditRound8.C

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ → ℝ → ℝ
```

Actual body:

```lean
fun a b u => Real.pi ^ 2 * b / (2 * u ^ 2) - 2 * a ^ 4 * b ^ 3 / (3 * u ^ 2 * (1 + b + b ^ 2 * a ^ 2))
```

## AuditRound8.D_curved_counterexample

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
LT.lt.{0} 1500 (3015 / 2) ∧
  LT.lt.{0} (3015 / 2) 1515 ∧
    LT.lt.{0} 0 (4995815 / 10000000) ∧
      LT.lt.{0} (4995815 / 10000000) (1 / 2) ∧
        LT.lt.{0} (AuditRound8.wCap (3015 / 2)) (4995815 / 10000000) ∧
          LT.lt.{0} (4995815 / 10000000) (AuditRound8.wCap 1515)
```

## AuditRound8.D_gap_signs

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
LT.lt.{0} (AuditRound8.capGap (3015 / 2) (4995815 / 10000000)) 25 ∧
  LT.lt.{0} 25 (AuditRound8.capGap 1515 (4995815 / 10000000))
```

## AuditRound8.I2

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ → ℝ
```

Actual body:

```lean
fun a u => u / 2 - u * Real.sin (2 * a) / (4 * a)
```

## AuditRound8.S

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ → ℝ
```

Actual body:

```lean
fun a u => 2 * AuditRound8.mubar1 u / u - AuditRound8.mubar2 a u * Real.sin a ^ 2 / AuditRound8.I2 a u
```

## AuditRound8.S_reduction

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (a b u : ℝ),
  LT.lt.{0} 0 a →
    LT.lt.{0} 0 u →
      LT.lt.{0} 0 b →
        Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
          Eq.{1} (AuditRound8.S a u)
            (HSub.hSub.{0, 0, 0}
              (HDiv.hDiv.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) (HMul.hMul.{0, 0, 0} 2 (HPow.hPow.{0, 0, 0} u 3)))
              (HDiv.hDiv.{0, 0, 0}
                (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 (HPow.hPow.{0, 0, 0} a 4)) (HPow.hPow.{0, 0, 0} b 2))
                (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} u 3)
                  (HAdd.hAdd.{0, 0, 0} (HAdd.hAdd.{0, 0, 0} 1 b)
                    (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))))
```

## AuditRound8.capGap

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ → ℝ
```

Actual body:

```lean
fun R w => Real.pi ^ 2 * R * (1 / (4 * w ^ 2) - 1)
```

## AuditRound8.cap_lt_of_gap_lt

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (R w : ℝ), LT.lt.{0} 0 R → LT.lt.{0} 0 w → LT.lt.{0} (AuditRound8.capGap R w) 25 → LT.lt.{0} (AuditRound8.wCap R) w
```

## AuditRound8.cap_square

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (R : ℝ),
  LT.lt.{0} 0 R →
    LT.lt.{0} 0 (AuditRound8.wCap R) ∧
      Eq.{1} (HPow.hPow.{0, 0, 0} (AuditRound8.wCap R) 2)
        (HDiv.hDiv.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) R)
          (HMul.hMul.{0, 0, 0} 4 (HAdd.hAdd.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) R) 25)))
```

## AuditRound8.coefficient_identity

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (a b u : ℝ),
  LT.lt.{0} 0 a →
    LT.lt.{0} 0 u →
      LT.lt.{0} u (1 / 2) →
        Eq.{1} b (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) u) →
          Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
            Eq.{1} (AuditRound8.C a b u)
              (HAdd.hAdd.{0, 0, 0}
                (HDiv.hDiv.{0, 0, 0}
                  (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 4 (AuditRound8.mubar1 u)) (AuditRound8.ell u))
                  (HMul.hMul.{0, 0, 0} 3 u))
                (HMul.hMul.{0, 0, 0} (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) 3) (AuditRound8.S a u)))
```

## AuditRound8.critical_rewrite

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (R : ℝ),
  LT.lt.{0} 0 R →
    Eq.{1} (AuditRound8.wCritical R) (HDiv.hDiv.{0, 0, 0} (√R) (HMul.hMul.{0, 0, 0} 2 (HAdd.hAdd.{0, 0, 0} (√R) 1)))
```

## AuditRound8.ell

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ
```

Actual body:

```lean
fun u => 1 / 2 - u
```

## AuditRound8.integral_reduction

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (a b u : ℝ),
  LT.lt.{0} 0 a →
    LT.lt.{0} 0 u →
      LT.lt.{0} 0 b →
        Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
          Eq.{1} (AuditRound8.I2 a u)
              (HDiv.hDiv.{0, 0, 0}
                (HMul.hMul.{0, 0, 0} u
                  (HAdd.hAdd.{0, 0, 0} (HAdd.hAdd.{0, 0, 0} 1 b)
                    (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))
                (HMul.hMul.{0, 0, 0} 2
                  (HAdd.hAdd.{0, 0, 0} 1 (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))) ∧
            LT.lt.{0} 0 (AuditRound8.I2 a u)
```

## AuditRound8.local_root

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
(∀ (lambda2 : ℝ),
    LE.le.{0} 0 lambda2 →
      LE.le.{0} lambda2 (HMul.hMul.{0, 0, 0} 4 (HPow.hPow.{0, 0, 0} Real.pi 2)) →
        LE.le.{0} 0 (AuditRound8.phase lambda2) ∧
          LE.le.{0} (AuditRound8.phase lambda2) (HDiv.hDiv.{0, 0, 0} Real.pi 20) ∧
            LT.lt.{0} (HDiv.hDiv.{0, 0, 0} Real.pi 20) (HDiv.hDiv.{0, 0, 0} Real.pi 2)) ∧
  (∀ (a b u : ℝ),
      LT.lt.{0} 0 a →
        LT.lt.{0} 0 u →
          LT.lt.{0} 0 b →
            Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
              Eq.{1} (AuditRound8.I2 a u)
                  (HDiv.hDiv.{0, 0, 0}
                    (HMul.hMul.{0, 0, 0} u
                      (HAdd.hAdd.{0, 0, 0} (HAdd.hAdd.{0, 0, 0} 1 b)
                        (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))
                    (HMul.hMul.{0, 0, 0} 2
                      (HAdd.hAdd.{0, 0, 0} 1
                        (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))) ∧
                LT.lt.{0} 0 (AuditRound8.I2 a u)) ∧
    (∀ (a b u : ℝ),
        LT.lt.{0} 0 a →
          LT.lt.{0} 0 u →
            LT.lt.{0} 0 b →
              Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
                Eq.{1} (AuditRound8.S a u)
                  (HSub.hSub.{0, 0, 0}
                    (HDiv.hDiv.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2)
                      (HMul.hMul.{0, 0, 0} 2 (HPow.hPow.{0, 0, 0} u 3)))
                    (HDiv.hDiv.{0, 0, 0}
                      (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 (HPow.hPow.{0, 0, 0} a 4)) (HPow.hPow.{0, 0, 0} b 2))
                      (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} u 3)
                        (HAdd.hAdd.{0, 0, 0} (HAdd.hAdd.{0, 0, 0} 1 b)
                          (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))))) ∧
      (∀ (a b u : ℝ),
          LT.lt.{0} 0 a →
            LT.lt.{0} 0 u →
              LT.lt.{0} u (1 / 2) →
                Eq.{1} b (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) u) →
                  Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a)))
                      0 →
                    Eq.{1} (AuditRound8.C a b u)
                      (HAdd.hAdd.{0, 0, 0}
                        (HDiv.hDiv.{0, 0, 0}
                          (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 4 (AuditRound8.mubar1 u)) (AuditRound8.ell u))
                          (HMul.hMul.{0, 0, 0} 3 u))
                        (HMul.hMul.{0, 0, 0} (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) 3) (AuditRound8.S a u)))) ∧
        (∀ (a b u : ℝ),
            LT.lt.{0} 0 a →
              LT.lt.{0} 0 u →
                LT.lt.{0} u (1 / 2) →
                  Eq.{1} b (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) u) →
                    Eq.{1}
                        (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a)))
                        0 →
                      Eq.{1} (AuditRound8.S a u) 0 →
                        Eq.{1} (AuditRound8.C a b u)
                            (HDiv.hDiv.{0, 0, 0}
                              (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) (AuditRound8.ell u))
                              (HMul.hMul.{0, 0, 0} 3 (HPow.hPow.{0, 0, 0} u 3))) ∧
                          LT.lt.{0} 0 (AuditRound8.C a b u)) ∧
          LT.lt.{0} AuditRound8.scalarRatio (8256 / 10000) ∧
            (LT.lt.{0} 1500 (3015 / 2) ∧
                LT.lt.{0} (3015 / 2) 1515 ∧
                  LT.lt.{0} (19 / 100) (48743 / 100000) ∧
                    LT.lt.{0} (48743 / 100000) (1 / 2) ∧
                      LT.lt.{0} (AuditRound8.wCritical 1500) (48743 / 100000) ∧
                        LT.lt.{0} (48743 / 100000) (AuditRound8.wCritical (3015 / 2))) ∧
              (LT.lt.{0} (AuditRound8.capGap (3015 / 2) (4995815 / 10000000)) 25 ∧
                  LT.lt.{0} 25 (AuditRound8.capGap 1515 (4995815 / 10000000))) ∧
                LT.lt.{0} 1500 (3015 / 2) ∧
                  LT.lt.{0} (3015 / 2) 1515 ∧
                    LT.lt.{0} 0 (4995815 / 10000000) ∧
                      LT.lt.{0} (4995815 / 10000000) (1 / 2) ∧
                        LT.lt.{0} (AuditRound8.wCap (3015 / 2)) (4995815 / 10000000) ∧
                          LT.lt.{0} (4995815 / 10000000) (AuditRound8.wCap 1515)
```

## AuditRound8.lt_cap_of_lt_gap

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (R w : ℝ), LT.lt.{0} 0 R → LT.lt.{0} 0 w → LT.lt.{0} 25 (AuditRound8.capGap R w) → LT.lt.{0} w (AuditRound8.wCap R)
```

## AuditRound8.mubar1

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ
```

Actual body:

```lean
fun u => Real.pi ^ 2 / (4 * u ^ 2)
```

## AuditRound8.mubar2

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ → ℝ
```

Actual body:

```lean
fun a u => a ^ 2 / u ^ 2
```

## AuditRound8.phase

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ
```

Actual body:

```lean
fun lambda2 => 1 / 1600 * √(1600 * lambda2)
```

## AuditRound8.phase_bound

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (lambda2 : ℝ),
  LE.le.{0} 0 lambda2 →
    LE.le.{0} lambda2 (HMul.hMul.{0, 0, 0} 4 (HPow.hPow.{0, 0, 0} Real.pi 2)) →
      LE.le.{0} 0 (AuditRound8.phase lambda2) ∧
        LE.le.{0} (AuditRound8.phase lambda2) (HDiv.hDiv.{0, 0, 0} Real.pi 20) ∧
          LT.lt.{0} (HDiv.hDiv.{0, 0, 0} Real.pi 20) (HDiv.hDiv.{0, 0, 0} Real.pi 2)
```

## AuditRound8.root_trig_reduction

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (a b : ℝ),
  Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
    Eq.{1} (HPow.hPow.{0, 0, 0} (Real.sin a) 2)
        (HDiv.hDiv.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))
          (HAdd.hAdd.{0, 0, 0} 1 (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2)))) ∧
      Eq.{1} (Real.sin (HMul.hMul.{0, 0, 0} 2 a))
        (HDiv.hDiv.{0, 0, 0} (Neg.neg.{0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 b) a))
          (HAdd.hAdd.{0, 0, 0} 1 (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} b 2) (HPow.hPow.{0, 0, 0} a 2))))
```

## AuditRound8.scalarRatio

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℚ
```

Actual body:

```lean
4 * (337 / 1000) * 9 * (100046 / 100000) / (3 * (333 / 106) * (156 / 100) * (99996 / 100000))
```

## AuditRound8.scalar_ratio_bound

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
LT.lt.{0} AuditRound8.scalarRatio (8256 / 10000)
```

## AuditRound8.stationary_coefficient

Kind: theorem; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (a b u : ℝ),
  LT.lt.{0} 0 a →
    LT.lt.{0} 0 u →
      LT.lt.{0} u (1 / 2) →
        Eq.{1} b (HDiv.hDiv.{0, 0, 0} (AuditRound8.ell u) u) →
          Eq.{1} (HAdd.hAdd.{0, 0, 0} (Real.sin a) (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} b a) (Real.cos a))) 0 →
            Eq.{1} (AuditRound8.S a u) 0 →
              Eq.{1} (AuditRound8.C a b u)
                  (HDiv.hDiv.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) (AuditRound8.ell u))
                    (HMul.hMul.{0, 0, 0} 3 (HPow.hPow.{0, 0, 0} u 3))) ∧
                LT.lt.{0} 0 (AuditRound8.C a b u)
```

## AuditRound8.wCap

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ
```

Actual body:

```lean
fun R => 1 / 2 / √(1 + 25 / (Real.pi ^ 2 * R))
```

## AuditRound8.wCritical

Kind: definition; origin: source; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
ℝ → ℝ
```

Actual body:

```lean
fun R => 1 / (2 * (1 + 1 / √R))
```

## AuditRound8.C._proof_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext'].

```lean
(HAdd.hAdd.{0, 0, 0} 2 1).AtLeastTwo
```

## AuditRound8.capGap.eq_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ (R w : ℝ),
  Eq.{1} (AuditRound8.capGap R w)
    (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HPow.hPow.{0, 0, 0} Real.pi 2) R)
      (HSub.hSub.{0, 0, 0} (HDiv.hDiv.{0, 0, 0} 1 (HMul.hMul.{0, 0, 0} 4 (HPow.hPow.{0, 0, 0} w 2))) 1))
```

## AuditRound8.ell._proof_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext'].

```lean
(HAdd.hAdd.{0, 0, 0} 1 1).AtLeastTwo
```

## AuditRound8.mubar1._proof_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext'].

```lean
(HAdd.hAdd.{0, 0, 0} 3 1).AtLeastTwo
```

## AuditRound8.phase._proof_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext'].

```lean
(HAdd.hAdd.{0, 0, 0} 1599 1).AtLeastTwo
```

## AuditRound8.root_trig_reduction._simp_1_1

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 2] [NeZero.{u_2} 2], Eq.{1} (Eq.{u_2 + 1} 2 0) False
```

## AuditRound8.root_trig_reduction._simp_1_2

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 3] [NeZero.{u_2} 3], Eq.{1} (Eq.{u_2 + 1} 3 0) False
```

## AuditRound8.root_trig_reduction._simp_1_3

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 4] [NeZero.{u_2} 4], Eq.{1} (Eq.{u_2 + 1} 4 0) False
```

## AuditRound8.root_trig_reduction._simp_1_4

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {M₀ : Type u_1} [inst : Mul.{u_1} M₀] [inst_1 : Zero.{u_1} M₀] [NoZeroDivisors.{u_1} M₀] {a b : M₀},
  Ne.{u_1 + 1} a 0 → Ne.{u_1 + 1} b 0 → Eq.{1} (Eq.{u_1 + 1} (HMul.hMul.{u_1, u_1, u_1} a b) 0) False
```

## AuditRound8.root_trig_reduction._simp_1_5

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {M₀ : Type u_1} [inst : MonoidWithZero.{u_1} M₀] {a : M₀} [IsReduced.{u_1} M₀] (n : ℕ),
  Ne.{u_1 + 1} a 0 → Eq.{1} (Eq.{u_1 + 1} (HPow.hPow.{u_1, 0, u_1} a n) 0) False
```

## AuditRound8.root_trig_reduction._simp_1_6

Kind: theorem; origin: compiler_generated; universes: ['u_3']; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ {G₀ : Type u_3} [inst : GroupWithZero.{u_3} G₀] {a : G₀} (n : ℤ),
  Ne.{u_3 + 1} a 0 → Eq.{1} (Eq.{u_3 + 1} (HPow.hPow.{u_3, 0, u_3} a n) 0) False
```

## AuditRound8.root_trig_reduction._simp_1_7

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {R : Type u_1} [inst : AddMonoidWithOne.{u_1} R] [CharZero.{u_1} R] (n : ℕ),
  Eq.{1} (Eq.{u_1 + 1} (HAdd.hAdd.{u_1, u_1, u_1} (↑n) 1) 0) False
```

## AuditRound8.scalarRatio.eq_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
Eq.{1} AuditRound8.scalarRatio
  (HDiv.hDiv.{0, 0, 0}
    (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 4 (337 / 1000)) 9) (100046 / 100000))
    (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 3 (333 / 106)) (156 / 100)) (99996 / 100000)))
```

## AuditRound8.stationary_coefficient._simp_1_1

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 2] [NeZero.{u_2} 2], Eq.{1} (Eq.{u_2 + 1} 2 0) False
```

## AuditRound8.stationary_coefficient._simp_1_2

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 3] [NeZero.{u_2} 3], Eq.{1} (Eq.{u_2 + 1} 3 0) False
```

## AuditRound8.stationary_coefficient._simp_1_3

Kind: theorem; origin: compiler_generated; universes: ['u_2']; transitive axioms: ['propext'].

```lean
∀ {α : Type u_2} [inst : Zero.{u_2} α] [inst_1 : OfNat.{u_2} α 4] [NeZero.{u_2} 4], Eq.{1} (Eq.{u_2 + 1} 4 0) False
```

## AuditRound8.stationary_coefficient._simp_1_4

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {M₀ : Type u_1} [inst : Mul.{u_1} M₀] [inst_1 : Zero.{u_1} M₀] [NoZeroDivisors.{u_1} M₀] {a b : M₀},
  Ne.{u_1 + 1} a 0 → Ne.{u_1 + 1} b 0 → Eq.{1} (Eq.{u_1 + 1} (HMul.hMul.{u_1, u_1, u_1} a b) 0) False
```

## AuditRound8.stationary_coefficient._simp_1_5

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {M₀ : Type u_1} [inst : MonoidWithZero.{u_1} M₀] {a : M₀} [IsReduced.{u_1} M₀] (n : ℕ),
  Ne.{u_1 + 1} a 0 → Eq.{1} (Eq.{u_1 + 1} (HPow.hPow.{u_1, 0, u_1} a n) 0) False
```

## AuditRound8.stationary_coefficient._simp_1_6

Kind: theorem; origin: compiler_generated; universes: ['u_3']; transitive axioms: ['propext', 'Classical.choice', 'Quot.sound'].

```lean
∀ {G₀ : Type u_3} [inst : GroupWithZero.{u_3} G₀] {a : G₀} (n : ℤ),
  Ne.{u_3 + 1} a 0 → Eq.{1} (Eq.{u_3 + 1} (HPow.hPow.{u_3, 0, u_3} a n) 0) False
```

## AuditRound8.stationary_coefficient._simp_1_7

Kind: theorem; origin: compiler_generated; universes: ['u_1']; transitive axioms: ['propext'].

```lean
∀ {R : Type u_1} [inst : AddMonoidWithOne.{u_1} R] [CharZero.{u_1} R] (n : ℕ),
  Eq.{1} (Eq.{u_1 + 1} (HAdd.hAdd.{u_1, u_1, u_1} (↑n) 1) 0) False
```

## AuditRound8.wCap._proof_1

Kind: theorem; origin: compiler_generated; universes: []; transitive axioms: ['propext'].

```lean
(HAdd.hAdd.{0, 0, 0} 24 1).AtLeastTwo
```
