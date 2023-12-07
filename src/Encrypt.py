import numpy as np

from src.LogicalShift import shift_right
from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial
from src.KeyGen import gen


def encrypt(seed_A: np.ndarray, b: np.ndarray, m: np.ndarray, q: int, p: int, n: int, l: int, mi, r: np.ndarray, h, h1, eps_q, eps_p, eps_T):
    p_base = ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), p)
    q_base = ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), q)
    A = gen(seed_A, q_base, n, l, eps_q)
    sp = np.array([Polynomial(np.random.binomial(n=mi, p=r, size=n), p_base) for _ in range(l)])
    sq = np.array([Polynomial(np.random.binomial(n=mi, p=r, size=n), q_base) for _ in range(l)])
    bp = shift_right(A@sq + h, eps_q - eps_p).rebase(p) # Error: rebase on np.array
    vp = b.T@sp
    m = Polynomial(m, p_base)
    cm = vp + h1.rebase(p) - 2**(eps_p - 1) * m
    cm = shift_right(cm, eps_p - eps_T).rebase(2**eps_T)
    return cm, bp
