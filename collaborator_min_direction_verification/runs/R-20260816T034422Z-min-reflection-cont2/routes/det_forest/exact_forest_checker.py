"""Exact checks for the minimum dual determinant forest route.

This script is not a universal proof.  It verifies the polynomial identities
used in report.md at low symbolic dimensions and audits the exact reduced
n=3 obstruction witness over QQ.
"""

from itertools import combinations

import sympy as sp


def subsets(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def interval_components(n_vertices, kept_edges):
    """Components of a path with vertices 0,...,n_vertices-1.

    Edge j (1 <= j < n_vertices) joins j-1 to j.
    """
    kept = set(kept_edges)
    left = 0
    out = []
    for j in range(1, n_vertices):
        if j not in kept:
            out.append(tuple(range(left, j)))
            left = j
    out.append(tuple(range(left, n_vertices)))
    return out


def forest_identity(n_vertices):
    z = sp.symbols(f"z1:{n_vertices + 1}")
    # edge[j-1] is the conductance between vertices j-1 and j
    edge = sp.symbols(f"e1:{n_vertices}") if n_vertices > 1 else ()
    h = sp.zeros(n_vertices)
    for i in range(n_vertices):
        h[i, i] = z[i]
    for j in range(1, n_vertices):
        e = edge[j - 1]
        h[j - 1, j - 1] += e
        h[j, j] += e
        h[j - 1, j] = -e
        h[j, j - 1] = -e

    forest = 0
    for kept in subsets(range(1, n_vertices)):
        term = sp.prod(edge[j - 1] for j in kept)
        for component in interval_components(n_vertices, kept):
            term *= sum(z[i] for i in component)
        forest += term
    return sp.expand(h.det() - forest)


def alternating_w_identity(n_vertices):
    d = sp.symbols(f"d1:{n_vertices + 1}")
    edge = sp.symbols(f"t1:{n_vertices}") if n_vertices > 1 else ()
    w = sp.symbols(f"w1:{n_vertices + 1}")
    g = sp.diag(*d)
    for j in range(1, n_vertices):
        g[j - 1, j] = -edge[j - 1]
        g[j, j - 1] = -edge[j - 1]
    h = g - sp.diag(*w)
    expansion = 0
    all_indices = tuple(range(n_vertices))
    for selected in subsets(all_indices):
        selected_set = set(selected)
        complement = [i for i in all_indices if i not in selected_set]
        principal = sp.Integer(1) if not complement else g.extract(complement, complement).det()
        expansion += (-1) ** len(selected) * sp.prod(w[i] for i in selected) * principal
    return sp.expand(h.det() - expansion)


def scaled_charge_identity(n_vertices):
    d = sp.symbols(f"h1:{n_vertices + 1}")
    edge = sp.symbols(f"c1:{n_vertices}") if n_vertices > 1 else ()
    v = sp.symbols(f"v1:{n_vertices + 1}")
    h = sp.diag(*d)
    for j in range(1, n_vertices):
        h[j - 1, j] = -edge[j - 1]
        h[j, j - 1] = -edge[j - 1]
    vv = sp.diag(*v)
    scaled = vv * h * vv
    q = [sp.expand(v[i] * (h * sp.Matrix(v))[i]) for i in range(n_vertices)]
    laplace_plus_q = sp.diag(*q)
    for j in range(1, n_vertices):
        e = edge[j - 1] * v[j - 1] * v[j]
        laplace_plus_q[j - 1, j - 1] += e
        laplace_plus_q[j, j] += e
        laplace_plus_q[j - 1, j] = -e
        laplace_plus_q[j, j - 1] = -e
    matrix_residual = scaled - laplace_plus_q
    determinant_residual = sp.expand(scaled.det() - sp.prod(x * x for x in v) * h.det())
    return matrix_residual, determinant_residual


def reflection_covariance_identity(n_vertices):
    d = sp.symbols(f"u1:{n_vertices + 1}")
    edge = sp.symbols(f"r1:{n_vertices}") if n_vertices > 1 else ()
    v = sp.Matrix(sp.symbols(f"x1:{n_vertices + 1}"))
    p = sp.symbols("p", nonzero=True)
    h = sp.diag(*d)
    for j in range(1, n_vertices):
        h[j - 1, j] = -edge[j - 1]
        h[j, j - 1] = -edge[j - 1]
    reversal = sp.zeros(n_vertices)
    for i in range(n_vertices):
        reversal[i, n_vertices - 1 - i] = 1
    h_sharp = p**2 * reversal * h * reversal
    v_sharp = p ** (-2) * reversal * v
    q = sp.diag(*v) * h * v
    q_sharp = sp.diag(*v_sharp) * h_sharp * v_sharp
    assert sp.simplify(q_sharp - p ** (-2) * reversal * q) == sp.zeros(n_vertices, 1)
    assert sp.simplify(h_sharp.det() - p ** (2 * n_vertices) * h.det()) == 0

    if n_vertices > 1:
        e = sp.Matrix([edge[j - 1] * v[j - 1] * v[j] for j in range(1, n_vertices)])
        e_sharp = sp.Matrix(
            [
                (p**2 * edge[n_vertices - 2 - j])
                * v_sharp[j]
                * v_sharp[j + 1]
                for j in range(n_vertices - 1)
            ]
        )
        edge_reversal = sp.zeros(n_vertices - 1)
        for i in range(n_vertices - 1):
            edge_reversal[i, n_vertices - 2 - i] = 1
        assert sp.simplify(e_sharp - p ** (-2) * edge_reversal * e) == sp.zeros(
            n_vertices - 1, 1
        )


def exact_reduced_witness():
    q = sp.Rational
    p_inv = [
        sp.Matrix([[1, q(1, 2)], [q(1, 2), q(5, 4)]]),
        sp.Matrix([[q(103, 52), q(3, 2)], [q(3, 2), q(103, 52)]]),
        sp.Matrix([[q(5, 4), q(1, 2)], [q(1, 2), 1]]),
    ]
    w = q(71, 26)
    h = sp.Matrix(
        [
            [p_inv[0][1, 1] + p_inv[1][0, 0] - w, -p_inv[1][0, 1]],
            [-p_inv[1][0, 1], p_inv[1][1, 1] + p_inv[2][0, 0] - w],
        ]
    )
    assert h == sp.Matrix([[q(1, 2), q(-3, 2)], [q(-3, 2), q(1, 2)]])
    assert h.det() == -2
    z1 = h[0, 0] - q(3, 2)
    z2 = h[1, 1] - q(3, 2)
    assert (z1, z2) == (-1, -1)
    assert z1 * z2 + q(3, 2) * (z1 + z2) == -2

    a = [q(3, 4), q(1, 2), q(52, 181), q(52, 181), q(1, 2), q(3, 4)]
    k = [q(2), q(-71, 26), q(4525, 4056), q(-71, 26), q(2)]
    for j in range(3):
        c = 1 / k[2 * j]
        block = sp.Matrix([[a[2 * j] + c, -c], [-c, a[2 * j + 1] + c]])
        assert sp.simplify(block.inv() - p_inv[j]) == sp.zeros(2)

    # Exact time-translation forcing with the correct alternating phase law.
    incidence = sp.zeros(5, 6)
    for i in range(5):
        incidence[i, i] = 1
        incidence[i, i + 1] = -1
    m = sp.diag(*a) + incidence.T * sp.diag(*(1 / x for x in k)) * incidence
    gamma = sp.Matrix([q(28, 5), -1, q(45, 26), q(-45, 26), 1, q(-28, 5)])
    chi = [2, q(24, 5), q(11, 5), q(24, 5), 2]
    forcing = sp.Matrix(
        [
            q(19, 2) - chi[0],
            chi[0] - chi[1],
            chi[1] - chi[2],
            chi[2] - chi[3],
            chi[3] - chi[4],
            -q(19, 2) + chi[4],
        ]
    )
    assert m * gamma == forcing
    c_even = sp.Matrix(
        [
            [0, -1, 1, 0, 0, 0],
            [0, 0, 0, -1, 1, 0],
        ]
    )
    v = sp.diag(w, w).inv() * c_even * gamma
    assert v == sp.Matrix([1, 1])
    charge = sp.diag(*v) * h * v
    assert charge == sp.Matrix([-1, -1])
    assert sum(charge) == -2

    beta2 = q(17, 2)
    cosines = [q(13, 16), q(37, 192), q(63, 88), q(37, 192), q(13, 16)]
    for chi_i, cosine in zip(chi, cosines):
        assert sp.simplify(chi_i / beta2 - 1 / (1 + 4 * cosine)) == 0
    assert all(cosines[i] > q(1, 2) for i in (0, 2, 4))
    assert all(0 < cosines[i] < q(1, 2) for i in (1, 3))

    # The obstruction is not physical: two positive cells demand different
    # values of the one shared contrast (R-1)^2.
    def contrast_square(edge_index, cosine):
        q2 = (1 - cosine**2) * (1 + 4 * cosine) ** 2
        return sp.factor(
            k[edge_index] ** 2
            * a[edge_index]
            * a[edge_index + 1]
            * abs(gamma[edge_index] * gamma[edge_index + 1])
            / q2
        )

    contrast_first = contrast_square(0, cosines[0])
    contrast_middle = contrast_square(2, cosines[2])
    assert contrast_first == q(57344, 41905)
    assert contrast_middle == q(52707600, 1246373479)
    assert contrast_first != contrast_middle
    return h, contrast_first, contrast_middle


def main():
    for n_vertices in range(1, 5):
        assert forest_identity(n_vertices) == 0
    for n_vertices in range(1, 5):
        assert alternating_w_identity(n_vertices) == 0
    for n_vertices in range(1, 5):
        matrix_residual, determinant_residual = scaled_charge_identity(n_vertices)
        assert matrix_residual == sp.zeros(n_vertices)
        assert determinant_residual == 0
        reflection_covariance_identity(n_vertices)
    h, contrast_first, contrast_middle = exact_reduced_witness()
    print("FOREST_IDENTITY_N_1_TO_4=PASS")
    print("ALTERNATING_W_IDENTITY_N_1_TO_4=PASS")
    print("SCALED_CHARGE_IDENTITY_N_1_TO_4=PASS")
    print("REFLECTION_COVARIANCE_N_1_TO_4=PASS")
    print(f"REDUCED_WITNESS_H={h.tolist()}")
    print(f"REDUCED_WITNESS_DET={h.det()}")
    print(f"CONTRAST_SQUARE_FIRST={contrast_first}")
    print(f"CONTRAST_SQUARE_MIDDLE={contrast_middle}")
    print("SHARED_CONTRAST_MISMATCH=PASS")


if __name__ == "__main__":
    main()
