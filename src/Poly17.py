import numpy as np

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial


class Poly17(Polynomial):
    def __init__(self, coefficients):
        base = ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), 17, 23)
        super().__init__(coefficients, base)

    @staticmethod
    def init_many(multi_coefficients, **kwargs):
        base = ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), 17, 23)
        return Polynomial.init_many(multi_coefficients, base)

    @staticmethod
    def zero(**kwargs):
        base = ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), 17, 23)
        return Polynomial.zero(base)
