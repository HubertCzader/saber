import numpy as np


def accurate_round(x):
    if abs((x - int(x))) < 0.5:
        return int(x)
    return int(x) + int(np.sign(x))


class ModuloBase:
    def __init__(self, f, q, p):
        self.f = f % q
        self.q = q
        self.p = p

    def __eq__(self, other):
        return self.q == other.q and np.array_equal(self.f, other.f)

    def round_mod(self, x):
        return accurate_round(x*(self.p/self.q)) % self.p
