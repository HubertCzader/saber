import unittest

import numpy as np

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial
from src.Saber import Saber


class TestSaberSanity(unittest.TestCase):

    def test_construct(self):
        Saber()

    def test_encrypt(self):
        saber = Saber()
        n = saber.n
        saber.set_key()
        m = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
        r = np.random.uniform(size=n).round().astype(int)
        print(saber.encrypt(m, r))

    def test_decrypt(self):
        # m = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
        m = np.array([1, 0]*128)  # n = m.size = 256
        n = m.size
        saber = Saber(n=n)
        saber.set_key()
        r = np.random.uniform(size=n).round().astype(int)
        cryptogram = saber.encrypt(m, r, verbose=True)
        print(cryptogram)
        print(saber.decrypt(cryptogram).coefficients)

    def test_generate_example(self):
        n = 4
        l = 2
        mi = 2
        r = 42
        eps_q = 4
        eps_p = 3
        eps_T = 2
        gen = np.random.default_rng(seed=r)
        s = np.array([gen.binomial(n=mi, p=0.5, size=n) for _ in range(l)])
        print(r)
        print(s)


if __name__ == '__main__':
    unittest.main()
