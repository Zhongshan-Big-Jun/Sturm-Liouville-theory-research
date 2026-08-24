# B3 O3: exactly 2n simple zeros of G_{n,s} in (0, pi)

**Theorem.** For every integer n >= 1 and every real R > 1, the function
G_{n,s}(y) has exactly 2n zeros in the open interval (0, pi), and every
zero is simple. Here s = sqrt(R).

We also prove the requested polynomial formulation Q_{n,s}(x) is a genuine
even polynomial of exact degree 2n with exactly 2n simple zeros in (-1, 1).

---

## 1. Notation and a matrix factorization

Write

    c = cos y,   q = sin y,   s = sqrt(R) > 1,
    E = [[c,  q],
         [-q, c]],

    B_s = [[c,  s^(-1) q],
           [-s q, c]].

A direct multiplication gives

    B_s E = [[c^2 - s^(-1)q^2,  (1 + s^(-1)) cq],
             [-(1 + s)cq,        c^2 - s q^2]]
          = C_s(y).

Hence

    M_{n,s} = E C_s^n = E (B_s E)^n.

Also

    tr C_s = 2c^2 - (s + s^(-1))q^2 = 2T,
    det C_s = 1,

where we set

    T = T(y) = c^2 - (s + s^(-1))/2 * q^2.

---

## 2. Exact closed form for G

Let U_k be the Chebyshev polynomial of the second kind: U_0 = 1,
U_1 = 2T, and U_{k+1} = 2T U_k - U_{k-1}. We use the elementary
Cayley-Hamilton identity for the 2x2 matrix C_s:

    C_s^2 - 2T C_s + I = 0,

which implies for every k >= 1

    C_s^k = U_{k-1}(T) C_s - U_{k-2}(T) I,

with the convention U_{-1} = 0.

Therefore

    G_{n,s}(y) = (E C_s^n)_{12}
                = c (C_s^n)_{12} + q (C_s^n)_{22}
                = U_{n-1}(T) (c (C_s)_{12} + q (C_s)_{22}) - q U_{n-2}(T).

Now

    c (C_s)_{12} + q (C_s)_{22}
        = c * (1 + s^(-1)) c q + q * (c^2 - s q^2)
        = q [(2 + s^(-1)) c^2 - s q^2]
        = q (2T + s^(-1)).

Thus

    G_{n,s}(y) = q [ (2T + s^(-1)) U_{n-1}(T) - U_{n-2}(T) ].

Using the Chebyshev recurrence

    U_n(T) = 2T U_{n-1}(T) - U_{n-2}(T),

this simplifies to the central identity

    G_{n,s}(y) = sin(y) [ U_n(T(y)) + s^(-1) U_{n-1}(T(y)) ].   (1)

---

## 3. Root count for the trigonometric/Chebyshev factor

Define, for 0 < epsilon < 1,

    F_n(T) = U_n(T) + epsilon U_{n-1}(T).

**Lemma.** For every integer n >= 1 and every epsilon in (0,1), F_n has
exactly n zeros in the open interval (-1, 1), all simple, and since
deg F_n = n these are all of its zeros.

**Proof.** For T = cos theta with 0 < theta < pi, the standard Chebyshev
identity gives

    F_n(cos theta) = [ sin((n+1)theta) + epsilon sin(n theta) ] / sin theta.

Let epsilon + e^{i theta} = rho(theta) e^{i psi(theta)} with continuous
psi satisfying psi(0) = 0 and psi(pi) = pi. This is possible because
epsilon < 1. Then

    sin((n+1)theta) + epsilon sin(n theta)
        = Im( e^{i n theta} (epsilon + e^{i theta}) )
        = rho(theta) sin( n theta + psi(theta) ).

For 0 < theta < pi,

    psi'(theta) = (1 + epsilon cos theta) / (epsilon^2 + 2 epsilon cos theta + 1) > 0,

because epsilon < 1 implies 1 + epsilon cos theta > 1 - epsilon > 0 and the
denominator is positive. Hence

    Phi(theta) = n theta + psi(theta)

is strictly increasing and continuous on [0, pi], with

    Phi(0) = 0,   Phi(pi) = n pi + pi = (n+1) pi.

The equation F_n(cos theta) = 0 is equivalent to sin(Phi(theta)) = 0, i.e.
Phi(theta) = k pi for an integer k. In (0, pi) this happens exactly once
for each k = 1, ..., n. At those points Phi'(theta) > 0, so the zeros are
simple as zeros of the trigonometric numerator; equivalently they are
simple zeros of F_n in T. Since F_n is a polynomial of degree n, it has no
other zeros. QED.

For our problem epsilon = s^(-1), which lies in (0,1) because s > 1.
Consequently F_n(T) has exactly n simple zeros T_1, ..., T_n in (-1, 1),
and no zeros outside [-1, 1].

---

## 4. Passage from T to y

Set

    alpha = s + s^(-1),   beta = (alpha + 2)/2.

The identity  cos^2 y + sin^2 y = 1 gives

    T(y) = cos^2 y - alpha/2 sin^2 y
         = beta cos^2 y - alpha/2.

Thus T depends on y only through z = cos^2 y. On the interval z in (0, 1),
T(z) is an increasing affine bijection onto

    T(z) in (-alpha/2, 1).

Since alpha/2 = (s + s^(-1))/2 > 1, we have -alpha/2 < -1. Therefore the
whole interval (-1, 1) is contained in (-alpha/2, 1). For every T_j in
(-1, 1), the corresponding z_j = (T_j + alpha/2)/beta lies in (0, 1).

For each z_j in (0, 1) there are exactly two y in (0, pi) with
cos^2 y = z_j, namely

    y = arccos(sqrt(z_j)) and y = pi - arccos(sqrt(z_j)).

Hence, by (1) and the lemma, G_{n,s} has exactly 2n zeros in (0, pi).

Every such zero y_0 has z = cos^2 y_0 > 0, so cos y_0 != 0 and

    T'(y_0) = -2 beta sin y_0 cos y_0 != 0.

Moreover F_n'(T(y_0)) != 0 by the lemma. Differentiating (1) at a zero:

    G'(y_0) = sin(y_0) F_n'(T(y_0)) T'(y_0) != 0.

Thus all 2n zeros are simple. This proves the theorem.

---

## 5. The polynomial formulation Q_{n,s}

For x in (-1, 1), let y = arccos(x), so that sin y = sqrt(1 - x^2) > 0.
From (1),

    Q_{n,s}(x) = G_{n,s}(arccos x) / sqrt(1 - x^2)
               = F_n( beta x^2 - alpha/2 ),   epsilon = s^(-1).

Since F_n is a polynomial of exact degree n, Q_{n,s} is an even polynomial
of exact degree 2n. Its leading coefficient is

    2^n beta^n = 2^n ((alpha+2)/2)^n != 0,

so no cancellation lowers the degree.

The zeros of Q_{n,s} in (-1, 1) are the numbers x = +/- sqrt(z_j) for the
n values z_j from Section 4. Hence Q_{n,s} has exactly 2n simple zeros in
(-1, 1). Because deg Q_{n,s} = 2n, these are all of its zeros.

---

## 6. Audits

- **n = 1.** Then F_1(T) = 2T + s^(-1), whose only zero is
  T = -1/(2s), lying in (-1, 1). It gives exactly two y zeros in (0, pi).

- **y = 0 and y = pi.** These are zeros of G because sin y = 0, but they
  are endpoints and are not counted. The factor F_n(T(0)) = F_n(1) =
  (n+1) + n/s > 0, and similarly at y = pi.

- **y = pi/2.** Here sin y = 1 and T(pi/2) = -alpha/2 < -1. By the lemma,
  all zeros of F_n lie in (-1, 1), so F_n(-alpha/2) != 0. Thus G(pi/2) != 0.

- **Boundary R = 1.** This is outside the stated hypothesis R > 1, but the
  closed form extends: s = 1 gives B_s = E, C_s = E^2, and
  M_{n,1} = E C_1^n = E^{2n+1}, hence
  G_{n,1}(y) = sin((2n+1)y). Its zeros in (0, pi) are exactly
  y = k pi/(2n+1) for k = 1, ..., 2n, all simple. The theorem's 2n count
  therefore also holds at this boundary.

---

## 7. Statement of external facts used

1. **Cayley-Hamilton for a 2x2 matrix.** If A is a 2x2 matrix with trace
   t and determinant d, then A^2 - t A + d I = 0. Here d = det C_s = 1.
2. **Chebyshev second-kind polynomials.** U_n(cos theta) =
   sin((n+1)theta)/sin(theta) for theta in (0, pi); equivalently
   U_0 = 1, U_1 = 2T, U_{n+1} = 2T U_n - U_{n-1}. These are standard and
   are used only in this elementary form.
3. **The argument derivative formula** for z(theta) = epsilon + e^{i theta}
   is derived directly from d/d theta atan2(sin theta, epsilon + cos theta).

No numerical scan is used in the proof.
