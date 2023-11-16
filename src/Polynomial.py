import numpy as np
import math

class ModuloBase:
    def __init__(self, f, q):
        self.f = f % q
        self.q = q

    def __eq__(self, other):
        return self.q == other.q and np.array_equal(self.f, other.f)

class Polynomial:
    def __init__(self, coeffitients, base: ModuloBase):
        if isinstance(coeffitients, list):
            coeffitients = np.array(coeffitients, dtype=int)
        assert(coeffitients.dtype == int)
        self.coeffitients = self.__mod(coeffitients, base.f) % base.q
        self.base = base

    def initMany(multiCoeffitients, base: ModuloBase):
        return [Polynomial(coeffitients=coeffitients, base=base) for coeffitients in multiCoeffitients]
    
    def zero(base):
        return Polynomial([0], base)

    def __array__(self):
        return self.coeffitients
    
    def __add__(self, other):
        assert(isinstance(other, Polynomial))
        assert(self.base == other.base)
        newSize = max(self.coeffitients.shape[-1], other.coeffitients.shape[-1])
        coeff1 = np.pad(self, pad_width=(newSize - self.coeffitients.shape[-1], 0), mode='constant', constant_values=(0, 0))
        coeff2 = np.pad(other, pad_width=(newSize - other.coeffitients.shape[-1], 0), mode='constant', constant_values=(0, 0))
        return Polynomial(coeff1 + coeff2, self.base)
    
    def __sub__(self, other):
        assert(isinstance(other, Polynomial))
        assert(self.base == other.base)
        newSize = max(self.coeffitients.shape[-1], other.coeffitients.shape[-1])
        coeff1 = np.pad(self, pad_width=(newSize - self.coeffitients.shape[-1], 0), mode='constant', constant_values=(0, 0))
        coeff2 = np.pad(other, pad_width=(newSize - other.coeffitients.shape[-1], 0), mode='constant', constant_values=(0, 0))
        return Polynomial(coeff1 - coeff2, self.base)
    
    def __mul__(self, other):
        if isinstance(other, Polynomial):
            assert(self.base == other.base)
            return Polynomial(np.polymul(self, other).astype(int), self.base)
        elif isinstance(other, int):
            return Polynomial(self.coeffitients * other, self.base)
        else:
            raise TypeError("__mul__ accepts only Polynomial and int types")
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __repr__(self):
        if self.coeffitients.shape[-1] == 0:
            return "0"
        return ''.join([f"{int(coeff)}x^{self.coeffitients.shape[-1] - i - 1} + " for i, coeff in enumerate(self.coeffitients[:-1])]) + f"{int(self.coeffitients[-1])}"

    def __mod(self, coeffitients, f):
        return np.polydiv(coeffitients, f)[1].astype(int)