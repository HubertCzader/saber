"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Post-quantum Cryptography classes
AGH University of Cracow

Saber PKE implementation.
"""
from typing import Tuple
from dataclasses import dataclass

import numpy as np
from Crypto.Hash import SHAKE128

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial
from src.SaberConfiguration import SaberConfiguration, LIGHT_SABER


@dataclass
class Pk:
    seed_A: np.ndarray[int]
    b: np.ndarray[Polynomial]


@dataclass
class Cryptogram:
    C_m: Polynomial
    b_prim: np.ndarray[Polynomial]


class Saber:
    def __init__(self, saber_configuration: SaberConfiguration = LIGHT_SABER, rebase_alter: bool = False):
        self.mi = saber_configuration.mi
        self.n = saber_configuration.n
        self.l = saber_configuration.l

        self.eps_p = saber_configuration.epsilon_p
        self.p = 2 ** saber_configuration.epsilon_p
        self.eps_q = saber_configuration.epsilon_q
        self.q = 2 ** saber_configuration.epsilon_q
        self.eps_T = saber_configuration.epsilon_T
        self.T = 2 ** saber_configuration.epsilon_T

        poly_base = [1] + [0] * (saber_configuration.n - 1) + [1]
        self.p_base = ModuloBase(np.array(poly_base, dtype=int), self.p)
        self.q_base = ModuloBase(np.array(poly_base, dtype=int), self.q)

        self.h1 = Polynomial(np.full(saber_configuration.n,
                                     2 ** (saber_configuration.epsilon_q - saber_configuration.epsilon_p - 1)),
                             self.q_base)
        self.h = np.full(self.l, self.h1)
        h2_coefficient = 2 ** (self.eps_p - 2) - 2 ** (self.eps_p - self.eps_T - 1) + 2 ** (self.eps_q - self.eps_T - 1)
        self.h2 = Polynomial(np.full(saber_configuration.n, h2_coefficient), self.q_base)

        # debug parameters
        self.rebase_alter = rebase_alter

    def gen_A(self, seed_A) -> np.ndarray:
        byte_seed = np.packbits(seed_A.reshape((-1, 8))).tobytes()
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

    def __generate_s(self, base, r=None):
        if r is None:
            r = np.random.uniform(size=256).round().astype(int)

        generator = np.random.default_rng(r)
        s = np.array([Polynomial(generator.binomial(n=self.mi, p=0.5, size=self.n).round().astype(int), base)
                      - Polynomial(self.n * [self.mi / 2], base)
                      for _ in range(self.l)])

        return s

    def generate_key(self, seed_A=None, r=None):
        if seed_A is None:
            seed_A = np.random.uniform(size=self.n).round().astype(int)

        s = self.__generate_s(r, self.q_base)

        A = self.gen_A(seed_A)
        b = (np.matmul(A.transpose(), s) + self.h) >> (self.eps_q - self.eps_p)
        b = np.array([poly.rebase(self.p, self.rebase_alter) for poly in b])
        return s, (seed_A, b)

    def encrypt(self, m: np.ndarray[int], seed_A, b, rp: np.ndarray[int] = None, verbose: bool = False) \
            -> Tuple[Polynomial, np.ndarray[Polynomial]]:

        sp = self.__generate_s(self.p_base, rp)
        sq = [poly.rebase(self.q, self.rebase_alter) for poly in sp]

        A = self.gen_A(seed_A)
        bp = (A @ sq + self.h) >> (self.eps_q - self.eps_p)
        bp = np.array([x.rebase(self.p, self.rebase_alter) for x in bp])
        vp = b.T @ sp

        m = Polynomial(m, self.p_base)

        if verbose:
            print(f"vp: {vp}")
            print(f"mmod: {(2 ** (self.eps_p - 1)) * m}")
            print(f"h1: {self.h1}")
            print(f"h1 in base p: {self.h1.rebase(self.p, self.rebase_alter)}")

        cm: Polynomial = vp + self.h1.rebase(self.p, self.rebase_alter) - (2 ** (self.eps_p - 1)) * m
        cm = cm >> (self.eps_p - self.eps_T)
        if verbose:
            print(f"Shifted: {cm}")
            print(self.T)
            print(cm.base.q)

        cm = cm.rebase(self.T, self.rebase_alter, v=verbose)
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

    def decrypt(self, cryptogram: Tuple[Polynomial, np.ndarray[Polynomial]], s):
        c_m, b_prim = cryptogram
        assert isinstance(c_m, Polynomial)
        assert isinstance(b_prim, np.ndarray) and b_prim.dtype == Polynomial

        s_p = np.array([poly.rebase(self.p, self.rebase_alter) for poly in s])
        v = (b_prim.T @ s_p)

        # ToDo: Edytowac rebase
        m_prim = v - (2 ** (self.eps_p - self.eps_T) * c_m.rebase(self.p, self.rebase_alter)) + self.h2.rebase(self.p,
                                                                                                               self.rebase_alter)
        m_prim = (m_prim >> (self.eps_p - 1)).rebase(2, self.rebase_alter)
        return m_prim
