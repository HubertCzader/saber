from src.Polynomial import Polynomial
import numpy as np


# Test function
def shift_right(vector: np.Array, bits: int):
    return np.array([Polynomial(np.right_shift(polynomial.coefficients, bits), polynomial.base) for polynomial in vector])

