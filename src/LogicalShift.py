import numpy as np


# Test function
def shift_right(vector: np.Array, bits: int):
    return np.array([np.right_shift(elem, bits) for elem in vector])

