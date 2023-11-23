import numpy as np
from src.Polynomial import Polynomial


def encrypt(A: np.array, b: np.array, m: np.array, p: int):
    I = b.size
    poly_base = b[0].base
    poly_size = poly_base.coeficients.size - 1
    sp = np.random.randint(0, size=(I, poly_size))
    sp = Polynomial.init_many(sp, poly_base)
    bp = (A@sp).rebase(p)

