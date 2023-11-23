from unittest import TestCase
import numpy as np

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial


class TestPolynomial(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17)

    def test_createPolynomial(self):
        Polynomial(np.array([23, 45, 2, 1, 42], dtype=int), self.base)

    def test_equivalentPolynomialsAreEqual(self):
        poly1 = Polynomial(np.array([23, 45, 2, 1, 42], dtype=int), self.base)
        poly2 = Polynomial(np.array([2, 12, 14], dtype=int), self.base)
        assert(poly1 == poly2)

    def test_polynomialAsArrayElement(self):
        poly_array1 = Polynomial.init_many(np.array([[1, 0, 0], [0, 0, 0]]), self.base)
        poly_array2 = Polynomial.init_many(np.array([[0, 1, 0], [2, 5, 4]]), self.base)
        poly = Polynomial([1], self.base)
        result = poly_array1 @ poly_array2.T - poly
        self.assertEqual(Polynomial.zero(self.base), result)

    def test_correctlyRebase(self):
        poly1 = Polynomial(np.array([23, 45, 2, 1, 42], dtype=int), self.base)
        poly2 = poly1.rebase(11)
        expected = Polynomial(np.array([1, 8, 9], dtype=int), self.base.rebase(11))
        self.assertEqual(poly2, expected)
