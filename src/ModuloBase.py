"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Post-quantum Cryptography classes
AGH University of Cracow
"""
import numpy as np


def accurate_round(x):
    return np.where(np.abs((x - x.astype(int))) < 0.5, x.astype(int), x.astype(int) + np.sign(x)).astype(int)


class ModuloBase:
    def __init__(self, f, q):
        self.q = q
        self.f = f % self.q

    def __eq__(self, other):
        return self.q == other.q and np.array_equal(self.f, other.f)

    def rebase(self, p):
        return ModuloBase(self.f, p)

    def round_mod(self, x, p):
        return accurate_round(x * (p / self.q)) % p
