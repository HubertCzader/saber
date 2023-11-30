import numpy as np

from src.ModuloBase import ModuloBase
from src.Polynomial import Polynomial


class Poly17(Polynomial):
    def __init__(self, coefficients):
        super().__init__(coefficients, Poly17.get_base())

    @staticmethod
    def init_many(multi_coefficients, **kwargs):
        return Polynomial.init_many(multi_coefficients, Poly17.get_base())

    @staticmethod
    def zero(**kwargs):
        return Polynomial.zero(Poly17.get_base())

    @staticmethod
    def get_base():
        return ModuloBase(np.array([1, 0, 0, 0, 1], dtype=int), 17)
