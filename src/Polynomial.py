import numpy as np


class ModuloBase:
    def __init__(self, f, q):
        self.f = f % q
        self.q = q

    def __eq__(self, other):
        return self.q == other.q and np.array_equal(self.f, other.f)


class Polynomial:
    def __init__(self, coefficients, base: ModuloBase):
        if isinstance(coefficients, list):
            coefficients = np.array(coefficients, dtype=int)
        assert (coefficients.dtype == int)
        self.coefficients = self.__mod(coefficients, base.f) % base.q
        self.base = base

    # def __array__(self):
    #     return self.coefficients

    def __add__(self, other):
        assert isinstance(other, Polynomial) and self.base == other.base
        newSize = max(self.coefficients.shape[-1], other.coefficients.shape[-1])
        coeff1 = np.pad(self, pad_width=(newSize - self.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        coeff2 = np.pad(other, pad_width=(newSize - other.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        return Polynomial(coeff1 + coeff2, self.base)

    def __sub__(self, other):
        assert isinstance(other, Polynomial) and self.base == other.base
        newSize = max(self.coefficients.shape[-1], other.coefficients.shape[-1])
        coeff1 = np.pad(self, pad_width=(newSize - self.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        coeff2 = np.pad(other, pad_width=(newSize - other.coefficients.shape[-1], 0), mode='constant',
                        constant_values=(0, 0))
        return Polynomial(coeff1 - coeff2, self.base)

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
        return ''.join([f"{int(coeff)}x^{self.coefficients.shape[-1] - i - 1} + " for i, coeff in
                        enumerate(self.coefficients[:-1])]) + f"{int(self.coefficients[-1])}"

    def __mod(self, coefficients, f):
        return np.polydiv(coefficients, f)[1].astype(int)

    @staticmethod
    def initMany(multiCoefficients, base: ModuloBase):
        return [Polynomial(coefficients=coefficients, base=base) for coefficients in multiCoefficients]

    @staticmethod
    def zero(base):
        return Polynomial(np.array([0]), base)
