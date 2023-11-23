import numpy as np





class ModuloBase:
    def __init__(self, f, q):
        self.q = q
        self.f = f % self.q

    def __eq__(self, other):
        return self.q == other.q and np.array_equal(self.f, other.f)

    def rebase(self, p):
        return ModuloBase(self.f, p)

    def round_mod(self, x):
        return accurate_round(x*(self.p/self.q)) % self.p
