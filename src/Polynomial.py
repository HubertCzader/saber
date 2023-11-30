import numpy as np

from src.ModuloBase import ModuloBase, accurate_round


class Polynomial:
    def __init__(self, coefficients, base: ModuloBase):
        if isinstance(coefficients, list):
            coefficients = np.array(coefficients, dtype=int)
        assert (coefficients.dtype == int)
        self.coefficients = self.__mod(coefficients, base.f) % base.q
        self.base = base

    def rebase(self, p):
        rebased_coefficients = accurate_round(self.coefficients*(p/self.base.q))
        return Polynomial(rebased_coefficients, self.base.rebase(p))

    def __add__(self, other):
        assert isinstance(other, Polynomial) and self.base == other.base
        new_size = max(self.coefficients.shape[-1], other.coefficients.shape[-1])
        coeff1 = np.pad(self.coefficients, pad_width=(new_size - self.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        coeff2 = np.pad(other.coefficients, pad_width=(new_size - other.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        a = coeff1
        return Polynomial(coeff1 + coeff2, self.base)

    def __neg__(self):
        return Polynomial(-self.coefficients, self.base)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            assert self.base == other.base
            return Polynomial(np.polymul(self.coefficients, other.coefficients).astype(int), self.base)
        elif isinstance(other, int):
            return Polynomial(self.coefficients * other, self.base)
        else:
            raise TypeError("__mul__ accepts only Polynomial and int types")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        if self.coefficients.shape[-1] == 0:
            return "0"
        return ''.join([f"{int(coeff)}x^{self.coefficients.shape[-1] - i - 1}+" for i, coeff in
                        enumerate(self.coefficients[:-1])]) + f"{int(self.coefficients[-1])}"

    def __eq__(self, other):
        return isinstance(other, Polynomial) \
            and self.base == other.base \
            and np.all(self.coefficients == other.coefficients)

    def __mod__(self, other):
        if isinstance(other, int):
            return Polynomial(self.coefficients % other, self.base)
        else:
            raise TypeError("Polynomial % () accepts only int types")

    def __rshift__(self, other):
        if isinstance(other, int):
            return Polynomial(self.coefficients >> other, self.base)
        else:
            raise TypeError("Polynomial >> () accepts only int types")
    @staticmethod
    def __mod(coefficients, f):
        return np.polydiv(coefficients, f)[1].astype(int)

    @staticmethod
    def init_many(multi_coefficients: np.array, base: ModuloBase):
        return np.apply_along_axis(lambda x: Polynomial(coefficients=x, base=base), -1, multi_coefficients)

    @staticmethod
    def zero(base):
        return Polynomial(np.array([0]), base)
