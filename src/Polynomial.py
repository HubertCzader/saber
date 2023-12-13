"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Post-quantum Cryptography classes
AGH University of Cracow
"""
import numpy as np

from src.ModuloBase import ModuloBase, accurate_round


class Polynomial:
    def __init__(self, coefficients, base: ModuloBase, n: int = None):
        if isinstance(coefficients, list):
            coefficients = np.array(coefficients, dtype=int)
        assert (coefficients.dtype == int)
        self.coefficients = self.__mod(coefficients, base.f) % base.q
        if n:
            self.coefficients = np.pad(self.coefficients, (n - self.coefficients.size, 0), constant_values=0)
        self.base = base

    def rebase(self, p: int, alter: bool = True, v: bool = False):
        rebased_coefficients = accurate_round(self.coefficients*(p/self.base.q))
        if v:
            print(f"Old base: {self.base.q}, new base: {p}")
            print(f"Coefficient size before: {self.coefficients.size}, after: {rebased_coefficients.size}")
            print(f"Coefficients before: {self.coefficients}")
            print(f"Rebased coefficients before round: \n{self.coefficients*(p/self.base.q)}")
            print(f"Rebased coefficients after round: \n{rebased_coefficients}")
        if alter:
            return Polynomial(rebased_coefficients, self.base.rebase(p), self.coefficients.size)
        else:
            return Polynomial(self.coefficients, self.base.rebase(p), self.coefficients.size)

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
        if np.all(self.coefficients == 0):
            return "0"

        n = self.coefficients.shape[-1]
        return ''.join([f'{"+" if coeff > 0 and i > 0 else ""}{coeff if coeff != 0 else ""}{"x^%d" % (n-i-1) if n-i-1 > 0 and coeff != 0 else ""}' for i, coeff
                        in enumerate(self.coefficients)])

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
            shifted = Polynomial(self.coefficients >> other, self.base, self.coefficients.size)
            # print(len(shifted.coefficients))
            # print(shifted.coefficients)
            # print(len(self.coefficients))
            # print(self.coefficients
            # print(shifted.coefficients.size)
            # print(self.coefficients.size)

            assert shifted.coefficients.size == self.coefficients.size
            return shifted
        else:
            raise TypeError("Polynomial >> () accepts only int types")
    @staticmethod
    def __mod(coefficients, f):
        return (np.polydiv(coefficients, f)[1]).astype(int)

    @staticmethod
    def init_many(multi_coefficients: np.ndarray, base: ModuloBase):
        return np.apply_along_axis(lambda x: Polynomial(coefficients=x, base=base), -1, multi_coefficients)

    @staticmethod
    def zero(base):
        return Polynomial(np.array([0]), base)
