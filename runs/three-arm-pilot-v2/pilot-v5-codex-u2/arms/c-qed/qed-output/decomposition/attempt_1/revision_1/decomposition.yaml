metadata:
  problem_id: "problem.tex"
  mode: "CREATE"
  attempt: 1
  revision: 1
  timestamp: "2026-08-27T08:53:12.829520"

sources:
  - id: S0
    type: literature
    statement: |
      No external literature, citation, repository result, prior answer, or mathematical hint is available in this arm.
    citation: |
      <cite>type=survey_status; label=Offline literature status; title=Related work under the blind offline protocol; authors=QED benchmark; source_url=related_info/related_work.md; verifier_locator=opening paragraph; statement_match=exact; statement=No external literature, citation, repository result, prior answer, or mathematical hint is available in this arm.; usage=Consequently every random-walk and combinatorial estimate used below must be proved self-containedly rather than invoked externally.</cite>

  - id: S1
    type: literature
    statement: |
      From `(eta,z)`, independently resample the lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each, then independently resample the lamp at the arrival site from `Bernoulli(1/2)`.
    citation: |
      <cite>type=definition; label=Switch-walk-switch transition; title=Frozen task: U2 total-variation asymptotics; authors=QED benchmark problem setter; source_url=problem.tex; verifier_locator=transition-definition paragraph; statement_match=exact; statement=From `(eta,z)`, independently resample the lamp at `z` from `Bernoulli(1/2)`, move the base to `z+1` or `z-1` with probability `1/2` each, then independently resample the lamp at the arrival site from `Bernoulli(1/2)`.; usage=Used to derive the exact conditional lamp kernel from the base-walk range.</cite>

  - id: S2
    type: literature
    statement: |
      Total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1` distance on the countable state space.
    citation: |
      <cite>type=definition; label=Total variation convention; title=Frozen task: U2 total-variation asymptotics; authors=QED benchmark problem setter; source_url=problem.tex; verifier_locator=paragraph following the displayed conjecture; statement_match=exact; statement=Here total variation is `sup_A |P_t^x(A)-P_t^y(A)|`, equivalently one half of the `l^1` distance on the countable state space.; usage=Used for the kernel-contraction, projection, and exact overlap calculations.</cite>

steps:
  - id: STEP1
    statement: |
      Let `(W_s)_{0<=s<=t}` be simple symmetric random walk started at `a`, and put
      `L_t=min_{0<=s<=t} W_s`, `U_t=max_{0<=s<=t} W_s`, and
      `q_t^{(a)}(ell,u,z)=P_a(L_t=ell,U_t=u,W_t=z)`.
      For every integer `t>=1`, every finitely supported `eta:Z->Z_2`, and every `z in Z`,
      \[
      P_t^{(0,a)}(\eta,z)
      =\sum_{\ell,u\in\mathbb Z}
        q_t^{(a)}(\ell,u,z)\,
        2^{-(u-\ell+1)}
        {\bf1}_{\{\operatorname{supp}\eta\subseteq[\ell,u]\}} .
      \]
      Equivalently, conditional on `(L_t,U_t,W_t)=(ell,u,z)`, the lamps on
      `[ell,u]` are independent `Bernoulli(1/2)` variables and every lamp outside
      `[ell,u]` is zero.
    inputs: [S1]
    difficulty: easy
    is_key_step: false
    rationale: |
      This removes all lamp randomness from the comparison. Every visited site is resampled at
      least once: the initial site before the first move, intermediate sites upon arrival or
      departure, and the terminal site upon arrival. The last resampling variables at distinct
      visited sites are distinct independent fair bits. The initially zero lamps, including
      those at sites `0` and `2`, therefore leave no bias inside the visited interval.
    strategy_hint: |
      Condition first on the complete base path. Select the chronologically last resampling
      variable at each visited site, then average over all paths having the same range and
      endpoint.

  - id: STEP2
    statement: |
      Define the Markov kernel
      \[
      K((\ell,u,z),(\eta,w))
       ={\bf1}_{\{w=z\}}{\bf1}_{\{\operatorname{supp}\eta\subseteq[\ell,u]\}}
         2^{-(u-\ell+1)} .
      \]
      If `Q_t^{(a)}` denotes the law of `(L_t,U_t,W_t)` for a walk started at `a`,
      then for every `t>=1`,
      \[
      P_t^{(0,a)}=Q_t^{(a)}K,\qquad
      \|P_t^x-P_t^y\|_{\rm TV}\leq\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV},
      \]
      and translation invariance gives
      \[
      q_t^{(2)}(\ell,u,z)=q_t^{(0)}(\ell-2,u-2,z-2).
      \]
    inputs: [S2, STEP1]
    difficulty: easy
    is_key_step: false
    rationale: |
      The same conditional lamp kernel applies to both initial states, so total variation
      contracts under it. Translation is applied only to the base walk and its range; `(0,2)`
      is not interpreted as a lit lamp.
    strategy_hint: |
      Prove contraction directly by expanding the countable-state `l^1` norm and using
      `sum_s K(r,s)=1`.

  - id: STEP3
    statement: |
      For integers `d>=0` and `a,j in Z`, let `N_t(d,a,j)` be the number of
      nearest-neighbor paths `(v_0,...,v_t)` satisfying
      \[
      v_0=a,\quad v_t=j,\quad \min_s v_s=0,\quad\max_s v_s=d,
      \]
      and set `n_t(d,a,j)=2^{-t}N_t(d,a,j)`, with `n_t(d,a,j)=0` unless
      `0<=a,j<=d`. Then
      \[
      A_t:=\|Q_t^{(0)}-Q_t^{(2)}\|_{\rm TV}
      =\frac12\sum_{d=0}^{t}\sum_{j=0}^{d}\sum_{a=-2}^{d}
        |n_t(d,a,j)-n_t(d,a+2,j)|.
      \]
      Moreover,
      \[
      n_t(d,a,j)=0\quad\text{unless}\quad j-a\equiv t\pmod 2,
      \]
      and replacing `a` by `a+2` preserves this parity condition.
    inputs: [STEP2]
    difficulty: easy
    is_key_step: false
    rationale: |
      For a triple `(ell,u,z)`, use `d=u-ell`, `a=-ell`, and `j=z-ell`.
      Starting instead at `2` changes the relative starting coordinate from `a` to `a+2`
      while leaving `d` and `j` unchanged. This is the exact parity-preserving diagonal
      translation that must be estimated.
    strategy_hint: |
      Reindex the `l^1` formula from STEP2. The union of the supports in the `a` variable is
      exactly `-2<=a<=d`.

  - id: STEP4
    statement: |
      Let `h_t(d;a,j)` be `2^{-t}` times the number of length-`t` nearest-neighbor
      paths from `a` to `j` which remain in `[0,d]`; set it to zero if `d<0` or
      either endpoint is outside `[0,d]`. For all `d>=0` and all integers `a,j`,
      \[
      n_t(d,a,j)
       =h_t(d;a,j)-h_t(d-1;a-1,j-1)-h_t(d-1;a,j)
        +h_t(d-2;a-1,j-1).
      \]
      If
      \[
      p_t(k)=
      \begin{cases}
      2^{-t}\binom{t}{(t+k)/2},& |k|\le t\ \text{and }k\equiv t\pmod2,\\
      0,&\text{otherwise},
      \end{cases}
      \]
      then, for `0<=a,j<=d`,
      \[
      h_t(d;a,j)=\sum_{r\in\mathbb Z}
       \left[
       p_t(j-a+2r(d+2))
       -p_t(j+a+2+2r(d+2))
       \right].
      \]
      Both sums are finite because `p_t(k)=0` for `|k|>t`.
    inputs: [STEP3]
    difficulty: medium
    is_key_step: false
    rationale: |
      The first identity is inclusion-exclusion for attaining both endpoints of the range.
      The second is an exact two-barrier reflection formula. Together they expose the
      cancellation needed for the diagonal variation estimate.
    strategy_hint: |
      For inclusion-exclusion, subtract paths avoiding `0` and paths avoiding `d`, shifting
      an interval beginning at `1` down by one. Prove the image formula by reflecting at the
      first crossing of either absorbing barrier `-1` or `d+1`; no external reflection
      theorem is needed.

  - id: STEP5
    statement: |
      Put `m_t=max_k p_t(k)=2^{-t}\binom{t}{\lfloor t/2\rfloor}`. For every
      integer `t>=1`,
      \[
      \frac1{2\sqrt t}\le m_t\le\frac1{\sqrt t},
      \qquad
      \sum_{k\in\mathbb Z}|p_t(k)-p_t(k-2)|=2m_t.
      \]
      For every integer `t>=2` and every `k\equiv t (mod 2)`,
      \[
      |p_t(k+2)-2p_t(k)+p_t(k-2)|
      \le
      \frac{16}{t}\left(1+\frac{k^2}{t}\right)
      \sqrt{\frac2t}\exp\!\left(-\frac{k^2}{4t}\right).
      \]
    inputs: [STEP3]
    difficulty: medium
    is_key_step: false
    rationale: |
      These are the explicit binomial estimates required to control boundary terms and
      nonzero images in STEP6. The first-difference identity follows by telescoping along
      the unimodal parity lattice.
    strategy_hint: |
      Establish the central-binomial bounds by induction from the product formula for
      `binom(2n,n)/4^n`. For the second difference, use the exact ratios
      `p_t(k+2)/p_t(k)=(t-k)/(t+k+2)` and its reverse, treating
      `|k|<=t/2` and `|k|>t/2` separately; obtain the displayed Gaussian envelope from the
      product of these ratios.

  - id: STEP6
    statement: |
      For `A_t` defined in STEP3, every integer `t>=2` satisfies the explicit
      diagonal-variation estimate
      \[
      A_t\le
      16m_t+
      \frac{64}{t^{3/2}}\sum_{r=1}^{\infty}r e^{-r^2/t}
      +\frac{64}{t}\sum_{r=1}^{\infty}e^{-r^2/t}
      \le\frac{144}{\sqrt t}.
      \]
    inputs: [STEP4, STEP5]
    difficulty: hard
    is_key_step: true
    rationale: |
      This is the novel analytic core. It quantifies how little information the exact
      range-endpoint triple retains about a displacement of the starting point by two.
      The final inequality follows from
      `sum_{r>=1} r e^{-r^2/t}<=t`,
      `sum_{r>=1}e^{-r^2/t}<=sqrt(pi*t)/2`,
      `m_t<=t^{-1/2}`, and `80+32sqrt(pi)<144`.
    strategy_hint: |
      Substitute the four-term boundary-attainment formula of STEP4 into `A_t`, and then
      substitute the image formula for each killed kernel. Do not apply the triangle
      inequality to the four killed-kernel terms separately: that destroys the
      boundary-attainment cancellation. First pair the `a` and `a+2` expressions, group
      image indices `r` and `-r`, and perform discrete summation by parts in `d` and `j`.
      The zero-image boundary contributions reduce to at most eight parity-lattice first
      variations, giving `16m_t`. Each nonzero paired image contains a second difference
      of `p_t`; apply STEP5 and count image spacings `2r(d+2)`. Summing first in `d`
      yields respectively the two displayed Gaussian series. Check `d=0,1` separately
      under the zero-extension convention.
    hueristics: |
      Under diffusive scaling, `(minimum,maximum,endpoint)` has lattice mass of order
      `t^{-3/2}` over order `t^{3/2}` admissible triples. A translation by two creates
      a derivative of relative size `t^{-1/2}`, so total variation of order
      `t^{-1/2}` is the expected scale. The alternating four-term formula is essential:
      it records that both range boundaries were attained and converts dangerous
      first-image terms into summable second differences. The shift by two preserves
      parity, avoiding an order-one singular component.

  - id: STEP7
    statement: |
      For every integer `t>=2`,
      \[
      \|P_t^x-P_t^y\|_{\rm TV}
      \le A_t\le\frac{144}{\sqrt t}.
      \]
    inputs: [STEP2, STEP3, STEP6]
    difficulty: easy
    is_key_step: false
    rationale: |
      This is the upper bound obtained by applying the common lamp kernel after the
      quantitative range-endpoint estimate.
    strategy_hint: |
      Combine the contraction in STEP2 with STEP6 without introducing an additional
      coupling or conditioning argument.

  - id: STEP8
    statement: |
      For every integer `t>=1`,
      \[
      \|P_t^x-P_t^y\|_{\rm TV}
      \ge
      \|\mathcal L_0(W_t)-\mathcal L_2(W_t)\|_{\rm TV}
      =m_t
      \ge\frac1{2\sqrt t}.
      \]
    inputs: [S1, S2, STEP5]
    difficulty: easy
    is_key_step: false
    rationale: |
      The terminal base position is observable from the lamplighter state, so projection
      gives the first inequality. On the common parity lattice, the two endpoint laws are
      a one-place shift of the unimodal `Binomial(t,1/2)` mass sequence; its total
      variation under this shift is exactly its maximum mass.
    strategy_hint: |
      Sum the positive differences `p_t(k)-p_t(k-2)` up to the mode. Explicitly note that
      starts `0` and `2` have the same endpoint parity at time `t`.

  - id: STEP9
    statement: |
      At the omitted small time,
      \[
      \|P_0^x-P_0^y\|_{\rm TV}=1.
      \]
      At time one,
      \[
      \|P_1^x-P_1^y\|_{\rm TV}=\frac34.
      \]
      Indeed, each chain has eight equiprobable states of mass `1/8`; the only common
      endpoint is `1`, and exactly two states coincide there, namely those for which the
      noncommon lamps at `0` and `2` are both zero and the common lamp at `1` has either
      value.
    inputs: [S1, S2, STEP1]
    difficulty: easy
    is_key_step: false
    rationale: |
      This audits the small-time behavior and confirms that the final constants can use
      `t_0=1`. It also explicitly checks the effect of the initially zero lamps at the two
      different starting sites.
    strategy_hint: |
      Enumerate the two possible one-step base moves and the four equally likely lamp
      assignments on each two-point visited interval.

  - id: STEP10
    statement: |
      With the explicit choices
      \[
      c=\frac12,\qquad C=144,\qquad t_0=1,
      \]
      every integer `t>=t_0` satisfies
      \[
      \frac{c}{\sqrt t}
      \le\|P_t^x-P_t^y\|_{\rm TV}
      \le\frac{C}{\sqrt t}.
      \]
    inputs: [STEP7, STEP8, STEP9]
    difficulty: easy
    is_key_step: false
    rationale: |
      STEP7 and STEP8 cover `t>=2`; STEP9 supplies `t=1`. The constants satisfy
      `0<c<=C<infinity`.
    strategy_hint: |
      Separate `t=1` from `t>=2` and substitute the displayed constants.

target:
  id: GOAL
  statement: |
    Prove that there are explicit constants `0<c<=C<infinity` and an explicit integer `t_0` such that, for every integer `t>=t_0`,

    ```text
    c/sqrt(t) <= ||P_t^x-P_t^y||_TV <= C/sqrt(t).
    ```
  inputs: [STEP10]

proof_order: [STEP1, STEP2, STEP3, STEP4, STEP5, STEP6, STEP7, STEP8, STEP9, STEP10, GOAL]

key_steps: [STEP6]

self_critique:
  plausibility_issues:
    - "STEP6 is the genuine unresolved obligation. Its t^{-1/2} scale is strongly supported by the exact coordinate reduction and diffusive scaling, but the stated constants are valid only if the four boundary-attainment terms are retained through summation by parts. A termwise triangle inequality can produce a logarithmic loss or even an order-one bound."
    - "The proposed Gaussian-series bound in STEP6 must be checked at the degenerate widths d=0 and d=1 and at a=-2,-1,d-1,d. These terms are finite and covered by the 16m_t allowance, but omitting them would invalidate the estimate."
    - "The pointwise second-difference estimate in STEP5 is deliberately coarse. Its proof must separately audit the binomial support boundary because ratio formulas have vanishing denominators there."
  contradiction_checks:
    - "The supplied literature survey contains no mathematical theorem, so there is no external result with which the plan can conflict and no unlisted theorem is being assumed."
    - "The lower bound is compatible with the proposed upper bound because 1/2<144, and the exact t=1 value 3/4 satisfies both inequalities."
    - "Both starting positions are even, so their endpoints have the same parity at every time. The shift a->a+2 in STEP3 preserves the path parity condition and does not create disjoint supports."
    - "STEP1 uses the stated resampling convention exactly: the starting lamp is resampled before moving and the arrival lamp after moving. It does not replace resampling by toggling and does not treat `(0,2)` as a lit lamp."
  refinements_made:
    - "Reduced the lamplighter upper bound to an exact total-variation estimate for the base walk's minimum, maximum, and endpoint through a common conditional lamp kernel."
    - "Reindexed diagonal translation by the range width and the starting and ending coordinates relative to the minimum; this turns spatial translation by two into the precise finite difference n_t(d,a,j)-n_t(d,a+2,j)."
    - "Made the key cancellation explicit through inclusion-exclusion and the two-barrier image formula instead of invoking an unspecified local limit theorem."
    - "Avoided a reflection-coupling plan: deep pre-meeting excursions would require later covering a random interval and a naive truncation risks a logarithmic loss."
    - "Included exact parity, initial-lamp, and t=0,1 audits and selected t_0=1."
  difficulty_assessment: |
    STEP1 through STEP5 and STEP7 through STEP10 are self-contained routine-to-moderate
    calculations. STEP6 is hard and requires the original insight: a uniform l1 bound for a
    diagonal finite difference of the exact range-endpoint distribution. It is substantially
    narrower than the original conjecture because it contains no lamp variables, conditioning,
    or coupling, and it is reduced to a finite binomial-image calculation with an explicit
    target inequality. Nevertheless it is the point most likely to fail and should receive the
    prover's main attention. If STEP6 cannot be established with the displayed cancellation,
    the first unresolved obligation is precisely whether `A_t=O(t^{-1/2})` holds with an
    explicit constant via another self-contained range-path argument.