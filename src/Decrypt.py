from src.Polynomial import Polynomial
from src.ModuloBase import ModuloBase
from src.LogicalShift import shift_right

import numpy as np


def round_all_Polynomials(vector: np.Array, p: int):
    def round_binary(number: int):
        if abs(number - p // 2) <= p // 4:
            return 1
        return 0

    return np.array([Polynomial(np.array([round_binary(coefficient) for coefficient in polynomial.coefficients]),
                                polynomial.base) for polynomial in vector])


def decrypt(s, cryptogram, epsilon_q, epsilon_p, epsilon_t, n, f, p, q):
    c_m, b_prim = cryptogram
    assert isinstance(c_m, Polynomial) and isinstance(b_prim, Polynomial)
    single_coefficient = 2 ** (epsilon_p - 2) - 2 ** (epsilon_p - epsilon_t - 1) + 2 ** (epsilon_q - epsilon_t - 1)
    h2 = Polynomial(np.fill(n, single_coefficient), ModuloBase(f, q))
    v = (b_prim.T @ s)
    #ToDo: Edytowac rebase
    m_prim = shift_right((v - 2 ** (epsilon_p - epsilon_t) * c_m + h2).rebase(p), 1)
    return round_all_Polynomials(m_prim, p)


if __name__ == "__main__":
    pass
