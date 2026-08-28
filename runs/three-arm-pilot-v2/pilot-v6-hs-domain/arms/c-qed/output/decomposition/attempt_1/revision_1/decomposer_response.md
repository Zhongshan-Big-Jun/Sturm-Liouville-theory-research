metadata:
  problem_id: "problem.tex"
  mode: "CREATE"
  attempt: 1
  revision: 1
  timestamp: "2026-08-28T09:47:18.784211"

sources:
  - id: S1
    type: literature
    statement: |
      No external literature, repository result, prior answer, citation, or mathematical hint is available in this blind arm. Every theorem used must be proved self-containedly or identified as unverified.
    citation: |
      <cite>type=survey-status; label=Offline related-work status; title=Offline related-work status; authors=not supplied; source_url=related_info/related_work.md; verifier_locator=opening paragraph; statement_match=exact; statement=No external literature, repository result, prior answer, citation, or mathematical hint is available in this blind arm. Every theorem used must be proved self-containedly or identified as unverified.; usage=No external theorem is imported below; every mathematical step is to be proved self-containedly.</cite>

steps:
  - id: STEP1
    statement: |
      Put \(I=(-1,1)\), \(L=c-D^2\), and
      \[
        b_\pm(g):=g'(\pm1)-\frac{g(1)-g(-1)}2.
      \]
      Define, for \(u,v\in H^1(I)\),
      \[
        h(u):=\int_{-1}^1|u'|^2\,dx-\frac{|u(1)-u(-1)|^2}{2},
      \]
      \[
        \mathfrak a_c(u,v):=\int_{-1}^1u'\overline{v'}\,dx
          +c\int_{-1}^1u\overline v\,dx
          -\frac{(u(1)-u(-1))\overline{(v(1)-v(-1))}}2.
      \]
      Then
      \[
        h(u)=\int_{-1}^1\left|u'(x)-\frac{u(1)-u(-1)}2\right|^2dx\ge0,
      \]
      and there are constants \(0<A_c\le B_c<\infty\) such that
      \[
        A_c\|u\|_{H^1}^2\le\mathfrak a_c(u,u)
        \le B_c\|u\|_{H^1}^2\qquad(u\in H^1(I)).
      \]
      The positive self-adjoint realization in the problem satisfies
      \[
        D(K_c)=\{u\in H^2(I):b_+(u)=b_-(u)=0\},\qquad
        D(K_c^{1/2})=H^1(I),
      \]
      and
      \[
        \mathfrak a_c(u,v)=\langle K_cu,v\rangle_{L^2}
        \quad(u\in D(K_c),\ v\in H^1(I)).
      \]
      For every integer \(s\ge4\), write \(s=2m+\varepsilon\), where
      \(m=\lfloor s/2\rfloor\) and \(\varepsilon\in\{0,1\}\). Then
      \[
        D(K_c^{s/2})=
        \left\{f\in H^s(I):
        b_\pm(f^{(2\ell)})=0\text{ for }0\le\ell<m\right\}.
      \]
      Equivalently, for every \(0\le\ell<m\),
      \[
        f^{(2\ell+1)}(1)=f^{(2\ell+1)}(-1)
        =\frac{f^{(2\ell)}(1)-f^{(2\ell)}(-1)}2.
      \]
      Moreover, there are constants \(0<A_{s,c}\le B_{s,c}<\infty\) such that
      \[
        A_{s,c}\|f\|_{H^s}
        \le\|K_c^{s/2}f\|_{L^2}
        \le B_{s,c}\|f\|_{H^s}
        \qquad(f\in D(K_c^{s/2})).
      \]
    inputs: [S1]
    difficulty: medium
    is_key_step: false
    rationale: |
      This supplies the exact trace criterion and identifies the operator-domain topology. It also isolates the nonnegative boundary-corrected derivative energy used in the exclusion argument.
    strategy_hint: |
      Prove the form identity by writing \(d=(u(1)-u(-1))/2\) and expanding \(\int|u'-d|^2\). Establish the form realization by integration by parts. Obtain integer powers recursively from \(D(K_c^{j+1})=\{f\in D(K_c^j):K_c^jf\in D(K_c)\}\). For half-integer powers use the form characterization \(D(K_c^{j+1/2})=\{f\in D(K_c^j):K_c^jf\in H^1\}\). Since \(L^j\) is triangular in the even derivatives, the conditions \(b_\pm(L^jf)=0\) are equivalent to the displayed conditions on \(f^{(2\ell)}\). Prove the norm bounds by one-dimensional ODE estimates and induction, without citing an external elliptic-regularity theorem.

  - id: STEP2
    statement: |
      Let \(\mathcal P\) be the complex polynomial algebra and define
      \[
        \langle u,v\rangle_0:=\langle u,v\rangle_{L^2(I)},\qquad
        \langle u,v\rangle_1:=\mathfrak a_c(u,v).
      \]
      For \(\varepsilon\in\{0,1\}\), let \(R_n^{(\varepsilon)}\) be the unique
      monic polynomial of degree \(n\) orthogonal to all polynomials of degree
      less than \(n\) in \(\langle\cdot,\cdot\rangle_\varepsilon\).
      Thus \(R_n^{(0)}\) is the monic Legendre polynomial, while
      \(R_n^{(1)}\) is the monic polynomial for the form inner product.
      
      For \(s=2m+\varepsilon\), the polynomial left-definite inner product is
      \[
        [p,q]^{\mathrm{alg}}_s
        :=\langle L^mp,L^mq\rangle_\varepsilon .
      \]
      Its monic orthogonal polynomials satisfy
      \[
        L^mQ_n^{(s)}=c^mR_n^{(\varepsilon)}
      \]
      and hence
      \[
        Q_n^{(s)}
        =\left(1-\frac{D^2}{c}\right)^{-m}R_n^{(\varepsilon)}
        =\sum_{k=0}^{\lfloor n/2\rfloor}
          \binom{m+k-1}{k}c^{-k}
          \bigl(R_n^{(\varepsilon)}\bigr)^{(2k)}.
      \]
      In particular,
      \[
        \deg Q_n^{(s)}=n,\qquad
        \operatorname{span}\{Q_0^{(s)},\ldots,Q_N^{(s)}\}
        =\mathcal P_N
      \]
      for every \(N\ge0\).
    inputs: [S1, STEP1]
    difficulty: medium
    is_key_step: false
    rationale: |
      The finite inverse-series formula turns the abstract isometry construction into an explicit polynomial identity and makes both endpoint membership and completeness questions accessible.
    strategy_hint: |
      The map \(L^m:\mathcal P_N\to\mathcal P_N\) is triangular with nonzero diagonal \(c^m\), hence bijective. Transport orthogonality through this map. The inverse binomial series terminates because sufficiently high derivatives of a polynomial vanish.

  - id: STEP3
    statement: |
      For every \(n\ge0\),
      \[
        Q_n^{(s)}\in D(K_c^{s/2})
      \]
      if and only if, for all \(0\le\ell<m\),
      \[
        \bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(1)
        =\bigl(Q_n^{(s)}\bigr)^{(2\ell+1)}(-1)
        =\frac{
          \bigl(Q_n^{(s)}\bigr)^{(2\ell)}(1)
          -\bigl(Q_n^{(s)}\bigr)^{(2\ell)}(-1)}2.
      \]
      Define
      \[
        U_n^{(\varepsilon)}
        :=\left(1-\frac{D^2}{c}\right)^{-1}R_n^{(\varepsilon)}
        =\sum_{k=0}^{\lfloor n/2\rfloor}
          c^{-k}\bigl(R_n^{(\varepsilon)}\bigr)^{(2k)}.
      \]
      Then
      \[
        LU_n^{(\varepsilon)}=cR_n^{(\varepsilon)}
      \]
      algebraically, and
      \[
        Q_n^{(s)}\in D(K_c^{s/2})
        \quad\Longrightarrow\quad
        U_n^{(\varepsilon)}\in D(K_c).
      \]
    inputs: [STEP1, STEP2]
    difficulty: easy
    is_key_step: false
    rationale: |
      The first equivalence is the requested directly checkable condition. The final implication reduces every high-power membership question to a single Krein boundary condition.
    strategy_hint: |
      Algebraically,
      \(K_c^{m-1}Q_n^{(s)}=c^{m-1}U_n^{(\varepsilon)}\).
      For even \(s\), membership puts this function in \(D(K_c)\). For odd \(s\), it lies in \(D(K_c^{3/2})\subset D(K_c)\).

  - id: STEP4
    statement: |
      If \(\varepsilon=0\) and \(n\ge2\), then
      \[
        U_n^{(0)}\notin D(K_c).
      \]
      More precisely, if \(U:=U_n^{(0)}\) were in \(D(K_c)\) and
      \(R:=R_n^{(0)}\), then \(U-R\in\mathcal P_{n-2}\) and Legendre
      orthogonality would give
      \[
        \langle R,U-R\rangle_{L^2}=0.
      \]
      Using \(K_cU=cR\), one would obtain the exact identity
      \[
        0=h(U)+c\|U-R\|_{L^2}^2.
      \]
      Since both terms are nonnegative, this forces \(U=R\) and \(h(U)=0\).
      The identity in STEP1 then forces \(U\) to be affine, contradicting
      \(\deg U=n\ge2\).
    inputs: [STEP1, STEP2, STEP3]
    difficulty: hard
    is_key_step: true
    rationale: |
      This is the decisive obstruction for even \(s\): orthogonality turns the boundary-domain assumption into equality in a nonnegative energy inequality.
    strategy_hint: |
      Pair \(K_cU=cR\) with \(U\). Use
      \(\|U\|_2^2=\|R\|_2^2+\|U-R\|_2^2\) and
      \(\mathfrak a_c(U,U)=h(U)+c\|U\|_2^2\).
    hueristics: |
      The algebraic inverse differs from its forcing polynomial only by lower-degree terms. Base-space orthogonality therefore removes every cross term. The Krein boundary correction was chosen so that the remaining derivative contribution is exactly a square and can vanish only for affine functions.

  - id: STEP5
    statement: |
      If \(\varepsilon=1\) and \(n\ge2\), then
      \[
        U_n^{(1)}\notin D(K_c).
      \]
      Indeed, if \(U:=U_n^{(1)}\in D(K_c)\) and \(R:=R_n^{(1)}\), then
      \(U-R\in\mathcal P_{n-2}\), so form orthogonality gives
      \[
        \mathfrak a_c(R,U-R)=0.
      \]
      On the other hand, \(K_cU=cR\) and the form identity imply
      \[
        \mathfrak a_c(R,U)
        =\mathfrak a_c(U,R)
        =c\|R\|_{L^2}^2.
      \]
      Consequently,
      \[
        h(R)=\mathfrak a_c(R,R)-c\|R\|_{L^2}^2=0.
      \]
      Hence \(R\) is affine, contradicting \(\deg R=n\ge2\).
    inputs: [STEP1, STEP2, STEP3]
    difficulty: hard
    is_key_step: true
    rationale: |
      Odd orders use a different base inner product, so the even-order norm decomposition cannot be reused directly. This form-orthogonality identity supplies the corresponding obstruction.
    strategy_hint: |
      Use symmetry of \(\mathfrak a_c\), its association with \(K_c\), and orthogonality of \(R_n^{(1)}\) to every polynomial of degree below \(n\).
    hueristics: |
      The lower-degree correction \(U-R\) disappears in the form inner product. Domain membership then says that the form energy of \(R\) is only its \(cL^2\) part, forcing equality in the endpoint Cauchy-Schwarz inequality and therefore affine degree.

  - id: STEP6
    statement: |
      For every integer \(s\ge4\), every \(c>0\), and every \(n\ge0\),
      \[
        \boxed{\;
        Q_n^{(s)}\in D(K_c^{s/2})
        \quad\Longleftrightarrow\quad n\in\{0,1\}.
        \;}
      \]
      Specifically,
      \[
        R_0^{(\varepsilon)}=Q_0^{(s)}=1,\qquad
        R_1^{(\varepsilon)}=Q_1^{(s)}=x,
      \]
      and every affine polynomial satisfies the Krein condition and obeys
      \(K_c(a+bx)=c(a+bx)\). All \(n\ge2\) are excluded by STEP3 together
      with STEP4 or STEP5.
    inputs: [STEP3, STEP4, STEP5]
    difficulty: easy
    is_key_step: false
    rationale: |
      This converts the endpoint criterion into the complete degree spectrum, giving a concise necessary and sufficient answer to part 1.

  - id: STEP7
    statement: |
      Let \(\mathcal A_s\) be the Hilbert completion of
      \((\mathcal P,[\cdot,\cdot]^{\mathrm{alg}}_s)\). Define
      \[
        J_s p:=K_c^{-m}L^mp,\qquad p\in\mathcal P.
      \]
      Then \(J_sp\in D(K_c^{s/2})\) and
      \[
        \|J_sp\|_{D(K_c^{s/2})}^2
        :=\|K_c^{s/2}J_sp\|_2^2
        =[p,p]^{\mathrm{alg}}_s.
      \]
      The range \(J_s(\mathcal P)\) is dense in \(D(K_c^{s/2})\), so \(J_s\)
      extends uniquely to a unitary map
      \[
        \overline J_s:\mathcal A_s\longrightarrow D(K_c^{s/2}).
      \]
      Nevertheless, the two spaces are not equal under the identity
      realization as functions:
      \[
        x^2\in\mathcal P\subset\mathcal A_s,\qquad
        x^2\notin D(K_c^{s/2}),
      \]
      because \(b_+(x^2)=2\) and \(b_-(x^2)=-2\). In particular,
      \(J_sx^2\ne x^2\).
    inputs: [STEP1, STEP2, STEP6]
    difficulty: hard
    is_key_step: true
    rationale: |
      This distinguishes abstract unitary equivalence from equality under the identity map. The distinction is essential because completion uniqueness applies only after specifying how polynomials are embedded.
    strategy_hint: |
      For even \(s\), \(K_c^mJ_sp=L^mp\). For odd \(s\), use
      \(\|K_c^{m+1/2}J_sp\|_2^2=\mathfrak a_c(L^mp,L^mp)\).
      Since \(L^m\mathcal P=\mathcal P\), and polynomials are dense in
      \(L^2\) and in \(H^1\) with the form norm, the transported range is dense.
    hueristics: |
      The formal differential operator and the boundary-condition operator agree on compatible functions but have different inverses on arbitrary polynomials. Applying the genuine inverse after the formal differential expression is the natural nonidentity transport relating the two completions.

  - id: STEP8
    statement: |
      Put
      \[
        \mathcal C_s:=\mathcal P\cap D(K_c^{s/2}).
      \]
      Then
      \[
        \overline{\mathcal C_s}^{\,\|\cdot\|_{D(K_c^{s/2})}}
        =D(K_c^{s/2}).
      \]
      Quantitatively, define the continuous trace map
      \[
        T_s:H^s(I)\to\mathbb C^{2m},\qquad
        T_sf=(b_+(f^{(2\ell)}),b_-(f^{(2\ell)}))_{\ell=0}^{m-1}.
      \]
      There is a linear map
      \[
        R_s:\mathbb C^{2m}\to\mathcal P_{4m-1}
        \quad\text{with}\quad T_sR_s=I_{\mathbb C^{2m}}.
      \]
      If \(f\in D(K_c^{s/2})\) and \(p_j\to f\) in \(H^s(I)\), then
      \[
        q_j:=p_j-R_sT_sp_j\in\mathcal C_s
      \]
      and
      \[
        \|q_j-f\|_{H^s}
        \le\bigl(1+\|R_s\|\,\|T_s\|\bigr)\|p_j-f\|_{H^s}\to0.
      \]
      Hence graph-norm convergence follows from STEP1.

      In contrast,
      \[
        \operatorname{span}\{Q_n^{(s)}:n\ge0\}=\mathcal P
        \not\subset D(K_c^{s/2}),
      \]
      so the literal full span is not a dense linear subspace of the operator
      domain. Restricting to individually admissible basis vectors gives only
      \[
        \operatorname{span}\{Q_n^{(s)}:
        Q_n^{(s)}\in D(K_c^{s/2})\}
        =\operatorname{span}\{1,x\},
      \]
      which is not dense. Indeed, with
      \[
        F_m(x):=(1-x^2)^{2m},
      \]
      one has \(F_m\in\mathcal C_s\setminus\operatorname{span}\{1,x\}\) and
      \[
        \delta_{s,c}:=
        \inf_{a,b\in\mathbb C}
        \|K_c^{s/2}(F_m-a-bx)\|_{L^2}>0.
      \]
      However,
      \[
        \bigl(\operatorname{span}\{Q_n^{(s)}:n\ge0\}\bigr)
        \cap D(K_c^{s/2})
        =\mathcal C_s
      \]
      is dense in the operator domain.
    inputs: [STEP1, STEP2, STEP6, STEP7]
    difficulty: medium
    is_key_step: false
    rationale: |
      This resolves every natural interpretation of part 3: the full polynomial span is not contained in the domain, the span of individually admissible orthogonal polynomials is only two-dimensional, but boundary-compatible linear combinations form a graph core.
    strategy_hint: |
      Construct \(R_s\) by Hermite interpolation: prescribe all endpoint jets through order \(2m-1\), setting even jets to zero and odd jets to the desired trace coordinates. Polynomial density in \(H^s(I)\) can be proved by smooth approximation followed by uniform polynomial approximation of the highest derivative and repeated integration. The polynomial \(F_m\) has a zero of order \(2m\) at both endpoints, so all required traces vanish.

target:
  id: GOAL
  statement: |
    # Frozen main task: H^s operator-domain vs abstract completion

    Let `K_c = -d^2/dx^2 + c` on `[-1,1]` with Krein boundary condition
    `f'(±1) = (f(1)-f(-1))/2`, `c > 0`. Let `H^s`, `s >= 4`, be the left-definite
    space associated with `K_c`. Let `{Q_n^(s)}` be the SL_hs orthogonal polynomial
    system defined via the isometries `K_c^{-r}` on `L^2` or `H^1`.

    Prove or disprove, for integer `s >= 4`:

    1. Give a necessary and sufficient condition for `Q_n^(s) ∈ D(K_c^(s/2))`.
    2. Determine whether the operator-domain completion `D(K_c^(s/2))` equals the
       abstract completion obtained from the left-definite inner product on
       polynomials.
    3. Determine whether `span{Q_n^(s)}` is dense in `D(K_c^(s/2))` under the
       operator-domain reading.

    The complete polynomial degree spectrum is a bonus, not a completion gate.

    Rules: do not inspect repository history, current project files, known solution,
    or network. State all external theorems with hypotheses. Numerical evidence is
    not proof.
  inputs: [STEP6, STEP7, STEP8]

proof_order: [STEP1, STEP2, STEP3, STEP4, STEP5, STEP6, STEP7, STEP8, GOAL]

key_steps: [STEP4, STEP5, STEP7]

self_critique:
  plausibility_issues:
    - "STEP2 assumes that the stated SL_hs construction is precisely the pullback polynomial inner product through the formal expression L^m, with L^2 as the even base and the Krein form as the odd base. This is the natural meaning of the isometries named in the problem, but the prover must verify it directly from the supplied definitions."
    - "The word 'equals' in part 2 is interpretation-sensitive. STEP7 therefore proves both facts: there is a canonical nonidentity unitary transport, but there is no equality under the identity realization of polynomials as functions."
    - "Likewise, density of the full span is formally undefined because the span is not contained in the domain. STEP8 separately treats the literal span, the individually admissible subsystem, and the intersection with the domain."
    - "No external source theorem is available. The form realization, fractional-power domain identity, polynomial Sobolev density, and Hermite correction must therefore be proved in the final proof rather than cited."
  contradiction_checks:
    - "The plan is consistent with the survey's factual statement that no external result is available; S1 is only a status citation and no mathematical theorem is attributed to it."
    - "The classification n=0,1 does not imply that the only domain-compatible polynomials are affine. STEP8 explicitly allows cancellations among non-domain Q_n and constructs infinitely many compatible polynomials."
    - "The non-equality assertion in STEP7 does not contradict the unitary equivalence assertion: the unitary map J_s is not the identity on polynomials."
    - "The assumption c>0 is used essentially in positivity, injectivity, the inverse polynomial series, and the vanishing arguments; no claim is made for c=0."
  refinements_made:
    - "Replaced a merely formal endpoint criterion by the complete quantitative spectrum Q_n^(s) in the operator domain if and only if n is 0 or 1."
    - "Reduced all high-power boundary questions to the one-step polynomial U_n=(1-D^2/c)^(-1)R_n."
    - "Separated the even and odd base inner products, because their orthogonality identities require different nonnegative-energy arguments."
    - "Added the nonidentity unitary J_s to prevent conflating abstract completion equivalence with equality as function spaces."
    - "Added a Hermite trace-correction estimate showing that compatible polynomial combinations remain a graph core despite failure of individual basis membership."
  difficulty_assessment: |
    STEP4 and STEP5 are the genuinely novel algebraic-energy obstructions. Their
    conclusions depend on obtaining exactly the displayed zero-energy identities;
    a sign or boundary-form error would invalidate the spectrum. STEP7 is the main
    conceptual step because it must distinguish three different identifications of
    the same abstract Hilbert-scale data. STEP1 and STEP8 are substantial but
    standard one-dimensional arguments that can be proved directly. The steps
    chain completely: STEP1 and STEP2 identify the domains and polynomials,
    STEP3 reduces membership, STEP4–STEP6 classify it, STEP7 settles completion,
    and STEP8 settles every operator-domain density interpretation.