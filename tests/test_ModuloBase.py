from unittest import TestCase
import numpy as np
from src.ModuloBase import ModuloBase


class TestModuloBase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17, 11)

    def test_createModuloBase(self):
        ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17, 11)

    def test_equivalentModuloBasesAreEqual(self):
        base1 = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17, 11)
        base2 = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17, 11)
        self.assertEqual(base1, base2)

    def test_polynomialAsArrayElement(self):
        base = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17, 23)
        self.assertEqual(20, base.round_mod(15))
