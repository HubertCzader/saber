import unittest

import numpy as np

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial
from src.Saber import Saber
from src.SaberConfiguration import SaberConfiguration


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
        config = SaberConfiguration(l=2, n=4, epsilon_q=4, epsilon_p=3, epsilon_T=2, mi=2)
        r = 42
        rp = 32
        m = np.array([0, 0, 1, 1], dtype=int)
        seed_A = np.array([1, 1, 1, 0, 1, 1, 1, 0], dtype=int)
        saber = Saber(config)
        s, (_, b, bq) = saber.generate_key(seed_A, r)
        cryptogram = saber.encrypt(m=m, seed_A=seed_A, b=b, rp=rp)
        mp = saber.decrypt(cryptogram, s)
        np.testing.assert_array_equal(m, mp.coefficients)

    def test_big_example(self):
        config = SaberConfiguration(l=2, n=16, epsilon_q=4, epsilon_p=3, epsilon_T=2, mi=6)
        r = 42
        rp = 32
        m = np.array([0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1], dtype=int)
        seed_A = np.array([1, 1, 1, 0, 1, 1, 1, 0], dtype=int)
        saber = Saber(config)
        s, (_, b) = saber.generate_key(seed_A, r)
        A = saber.gen_A(seed_A)
        cryptogram = saber.encrypt(m, seed_A, b, rp)
        mp = saber.decrypt(cryptogram, s)
        np.testing.assert_array_equal(m, mp.coefficients)


if __name__ == '__main__':
    unittest.main()
