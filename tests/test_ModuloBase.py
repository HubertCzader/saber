from unittest import TestCase
import numpy as np
from src.ModuloBase import ModuloBase


class TestModuloBase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17)

    def test_createModuloBase(self):
        ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17)

    def test_equivalentModuloBasesAreEqual(self):
        base1 = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17)
        base2 = ModuloBase(np.array([1, 0, 0, 1], dtype=int), 17)
        self.assertEqual(base1, base2)

