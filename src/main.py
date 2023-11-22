from Polynomial import Polynomial
from src.ModuloBase import ModuloBase
import numpy as np

if __name__ == "__main__":
    base = ModuloBase(np.array([1, 0, 0, 1]), 17, 23)
    a = Polynomial(np.array([1, 1, 1, 1, 1]), base)
    tab = np.array([[a, a], [a, a]])
    print(tab)
    print(tab + tab)
