import numpy as np

from src.KeyGen import gen
from src.LogicalShift import shift_right
from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial


class Saber:
    def __init__(self, n: int = 256, l: int = 3, eps_p: int = 10, eps_q: int = 13, eps_T: int = 4, mi: int = 8):
        self.A = None
        self.b = None
        self.mi = mi
        self.n = n
        self.l = l
        assert(eps_p < eps_q)
        assert(eps_T < eps_p)
        self.eps_p = eps_p
        self.eps_q = eps_q
        self.eps_T = eps_T
        self.p = 2**eps_p
        self.q = 2**eps_q
        self.T = 2 ** eps_T
        poly_base = [1]+[0]*(n-1)+[1]
        self.p_base = ModuloBase(np.array(poly_base, dtype=int), self.p)
        self.q_base = ModuloBase(np.array(poly_base, dtype=int), self.q)
        self.h1 = Polynomial(2**(eps_q-eps_p-1)*np.ones(n, dtype=int), self.q_base)
        self.h = np.array([self.h1]*self.l, dtype=Polynomial)

    def set_key(self, seed_A: np.ndarray, b: np.ndarray):
        self.b = b
        self.A = gen(seed_A, self.q_base, self.n, self.l, self.eps_q)

    def encrypt(self, m: np.ndarray, r: np.ndarray):
        sp = np.array([Polynomial(np.random.binomial(n=self.mi, p=r, size=self.n), self.p_base) for _ in range(self.l)])
        sq = np.array([Polynomial(np.random.binomial(n=self.mi, p=r, size=self.n), self.q_base) for _ in range(self.l)])
        bp = shift_right(self.A @ sq + self.h, self.eps_q - self.eps_p)
        bp = np.array([x.rebase(self.p) for x in bp])
        vp = self.b.T @ sp
        m = Polynomial(m, self.p_base)
        cm = vp + self.h1.rebase(self.p) - 2 ** (self.eps_p - 1) * m
        cm = (cm >> (self.eps_p - self.eps_T)).rebase(self.T)
        return cm, bp

    def decrypt(self):
        pass
