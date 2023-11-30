import numpy as np


# Test function
def shift_right(vector: np.Array):
    return np.array([np.right_shift(elem, 1) for elem in vector])

