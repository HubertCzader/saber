import unittest

import numpy as np

from src.KeyGen import key_gen
from src.Saber import Saber


class TestSaberSanity(unittest.TestCase):
    def test_construct(self):
        Saber()

    def test_encrypt(self):
        n = 256
        saber = Saber(n=n)
        _, key = key_gen()
        saber.set_key(*key)
        m = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
        r = np.random.uniform(size=n).round().astype(int)
        saber.encrypt(m, r)


if __name__ == '__main__':
    unittest.main()
