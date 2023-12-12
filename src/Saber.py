from typing import Tuple

import numpy as np
from Crypto.Hash import SHAKE128

from src.LogicalShift import shift_right
from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial


class Saber:
    def __init__(self, n: int = 256, l: int = 3, eps_p: int = 10, eps_q: int = 13, eps_T: int = 4, mi: int = 8):
        self.seed_A = None
        self.b = None
        self.s = None
        self.mi = mi
        self.n = n
        self.l = l

        assert eps_p < eps_q
        assert eps_T < eps_p
        self.eps_p = eps_p
        self.p = 2**eps_p
        self.eps_q = eps_q
        self.q = 2**eps_q
        self.eps_T = eps_T
        self.T = 2 ** eps_T

        poly_base = [1]+[0]*(n-1)+[1]
        self.p_base = ModuloBase(np.array(poly_base, dtype=int), self.p)
        self.q_base = ModuloBase(np.array(poly_base, dtype=int), self.q)

        self.h1 = Polynomial(np.full(n, 2**(eps_q-eps_p-1)), self.q_base)
        self.h = np.full(self.l, self.h1)
        h2_coefficient = 2 ** (self.eps_p - 2) - 2 ** (self.eps_p - self.eps_T - 1) + 2 ** (self.eps_q - self.eps_T - 1)
        self.h2 = Polynomial(np.full(n, h2_coefficient), self.q_base)

    def gen_A(self) -> np.ndarray:
        byte_seed = np.packbits(self.seed_A.reshape((-1, 8))).tobytes()
        shake = SHAKE128.new()
        shake.update(byte_seed)

        A_coefficient_len = self.eps_q
        shake_size = self.l * self.l * self.n * A_coefficient_len / 8
        raw = shake.read(int(shake_size))
        bytes_array = np.frombuffer(raw, dtype=np.uint8)
        nums = np.unpackbits(bytes_array)
        nums = nums.reshape(self.l, self.l, self.n, A_coefficient_len)

        A = np.ndarray((self.l, self.l), dtype=Polynomial)

        for A_row in range(nums.shape[0]):
            for A_col in range(nums.shape[1]):
                poly = nums[A_row][A_col]
                a = [coefficient.dot(2 ** np.arange(coefficient.size)[::-1]) for coefficient in poly]
                A[A_row][A_col] = Polynomial(a, self.q_base)
        return A

    def set_key(self):
        self.seed_A = np.random.uniform(size=self.n).round().astype(int)

        A = self.gen_A()

        r = np.random.uniform(size=self.n).round().astype(int)
        self.s = np.array([Polynomial(np.random.binomial(n=self.mi, p=r, size=self.n), self.q_base) for _ in range(self.l)])

        b = (np.matmul(A.transpose(), self.s) + self.h) >> (self.eps_q - self.eps_p)
        self.b = np.array([poly.rebase(self.p) for poly in b])

    def encrypt(self, m: np.ndarray, r: np.ndarray = None, verbose: bool = False) \
            -> Tuple[Polynomial, np.ndarray[Polynomial]]:
        if self.seed_A is None:
            raise AttributeError("Key was not set. Use the Saber.set_key() method before encryption.")

        if r is None:
            r = np.random.uniform(size=self.n).round().astype(int)

        sp = np.array([Polynomial(np.random.binomial(n=self.mi, p=r, size=self.n), self.p_base) for _ in range(self.l)])
        sq = [poly.rebase(self.q) for poly in sp]
        A = self.gen_A()
        bp = (A @ sq + self.h) >> (self.eps_q - self.eps_p)
        bp = np.array([x.rebase(self.p) for x in bp])
        vp = self.b.T @ sp
        m = Polynomial(m, self.p_base)
        if verbose:
            print(f"vp: {vp}")
            print(f"mmod: {(2 ** (self.eps_p - 1)) * m}")
            print(f"h1: {self.h1}")
            print(f"h1 in base p: {self.h1.rebase(self.p)}")

        cm: Polynomial = vp + self.h1.rebase(self.p) - (2 ** (self.eps_p - 1)) * m
        cm = cm >> (self.eps_p - self.eps_T)
        if verbose:
            print(f"Shifted: {cm}")
            print(self.T)
            print(cm.base.q)

        cm = cm.rebase(self.T, v=verbose)
        if verbose:
            print(f"Rebased: {cm}")
        return cm, bp

    @staticmethod
    def round_all_Polynomials(vector: np.ndarray, p: int) -> np.ndarray[Polynomial]:
        def round_binary(number: int):
            if abs(number - p // 2) <= p // 4:
                return 1
            return 0

        return np.array([Polynomial(np.array([round_binary(coefficient) for coefficient in polynomial.coefficients]),
                                    polynomial.base) for polynomial in vector])

    def decrypt(self, cryptogram: Tuple[Polynomial, np.ndarray[Polynomial]]):
        c_m, b_prim = cryptogram
        assert isinstance(c_m, Polynomial)
        assert isinstance(b_prim, np.ndarray) and b_prim.dtype == Polynomial

        s_p = np.array([poly.rebase(self.p) for poly in self.s])
        v = (b_prim.T @ s_p)
        # ToDo: Edytowac rebase
        m_prim = v - (2 ** (self.eps_p - self.eps_T) * c_m.rebase(self.p)) + self.h2.rebase(self.p)
        m_prim = (m_prim >> (self.eps_p - 1)).rebase(2)
        return m_prim
