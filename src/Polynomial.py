"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Post-quantum Cryptography classes
AGH University of Cracow
"""
import numpy as np

class Polynomial:
    def __init__(self, coefficients, n: int):
        if isinstance(coefficients, list):
            coefficients = np.array(coefficients, dtype=int)
        assert (coefficients.dtype == int)
        self.f = np.array([1] + [0] * (n - 1) + [1], dtype=int)
        self.n = n
        self.coefficients = self.__mod(coefficients, self.f)
        self.coefficients = np.pad(self.coefficients, (n - self.coefficients.size, 0), constant_values=0)

    def __add__(self, other):
        assert isinstance(other, Polynomial) and self.n == other.n
        return Polynomial(self.coefficients + other.coefficients, self.n)

    def __neg__(self):
        return Polynomial(-self.coefficients, self.n)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            assert self.n == other.n
            return Polynomial(np.polymul(self.coefficients, other.coefficients).astype(int), self.n)
        elif isinstance(other, int):
            return Polynomial(self.coefficients * other, self.n)
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
            and self.n == other.n \
            and np.all(self.coefficients == other.coefficients)

    def __mod__(self, other):
        if isinstance(other, int):
            return Polynomial(self.coefficients % other, self.n)
        else:
            raise TypeError("Polynomial % () accepts only int types")

    def __rshift__(self, other):
        if isinstance(other, int):
            shifted = Polynomial(self.coefficients >> other, self.n)

            assert shifted.coefficients.size == self.coefficients.size
            return shifted
        else:
            raise TypeError("Polynomial >> () accepts only int types")
    @staticmethod
    def __mod(coefficients, f):
        return (np.polydiv(coefficients, f)[1]).astype(int)

    @staticmethod
    def init_many(multi_coefficients: np.ndarray, n: int):
        return np.apply_along_axis(lambda x: Polynomial(coefficients=x, n=n), -1, multi_coefficients)

    @staticmethod
    def zero(n: int):
        return Polynomial(np.array([0]), n)
