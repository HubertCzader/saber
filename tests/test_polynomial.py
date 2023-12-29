from unittest import TestCase
import numpy as np

from src.Polynomial import Polynomial


class TestPolynomial(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.n = 3
        cls.p = 17

    def test_createPolynomial(self):
        Polynomial(np.array([23, 45, 2, 1, 42], dtype=int), self.n)

    def test_equivalentPolynomialsAreEqual(self):
        poly1 = Polynomial(np.array([23, 45, 2, 1, 42], dtype=int), self.n)
        poly2 = Polynomial(np.array([2, 12, 14], dtype=int), self.n)
        assert(poly1 == poly2)

    def test_polynomialAsArrayElement(self):
        poly_array1 = Polynomial.init_many(np.array([[1, 0, 0], [0, 0, 0]]), self.n)
        poly_array2 = Polynomial.init_many(np.array([[0, 1, 0], [2, 5, 4]]), self.n)
        poly = Polynomial([16], self.n)
        result = poly_array1 @ poly_array2.T - poly
        self.assertEqual(Polynomial.zero(self.n), result)
