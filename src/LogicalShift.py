from src.Polynomial import Polynomial
import numpy as np


# Test function
def shift_right(vector: np.Array, bits: int):
    return np.array([polynomial >> bits for polynomial in vector])

