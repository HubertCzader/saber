from src.Polynomial import Polynomial
from src.ModuloBase import ModuloBase

import numpy as np


def decript(s, cryptogram, epsilon_q, epsilon_p, epsilon_t, n, f, p, q):
    c_m, b_prim = cryptogram
    assert isinstance(c_m, Polynomial) and isinstance(b_prim, Polynomial)
    single_coefficient = 2 ** (epsilon_p - 2) - 2 ** (epsilon_p - epsilon_t - 1) + 2 ** (epsilon_q - epsilon_t - 1)
    h2 = Polynomial(np.fill(n, single_coefficient), ModuloBase(f, q))
    v = (b_prim.T @ s)
    m_prim = (v - 2 ** (epsilon_p - epsilon_t) * c_m + h2).rebase(p)



if __name__== "__main__":
    pass
