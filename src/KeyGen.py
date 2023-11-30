from typing import Union

from src.Polynomial import Polynomial
from src.ModuloBase import ModuloBase
from Crypto.Hash import SHAKE128
import numpy as np


def gen(seed: np.array, base: ModuloBase, n: int, _l: int):
    # todo: check if seed is of length n, or trim/extend it to size
    Amax = base.q
    byte_seed = np.packbits(seed.reshape((-1, 8))).tobytes()
    print(byte_seed)
    shake = SHAKE128.new()
    shake.update(byte_seed)
    raw = shake.read(int(_l*_l*n/8*Amax))
    nums = np.frombuffer(raw, dtype=np.uint8)
    print(nums.size)


# generate a public key
# default values conform to the Saber security level
def key_gen(seed: Union[np.array, list], n: int = 256, _l: int = 3, epsilon_p: int = 10, epsilon_q: int = 13, epsilon_t: int = 4, mi: int = 8):
    # todo: if seed is a list, make it into np.array
    p = 2 ** epsilon_p
    q = 2 ** epsilon_q

    base = ModuloBase(np.array(([1]+[0]*(n-1)+[1]), dtype=int), q)
    h1_elem = np.power(2, (epsilon_q-epsilon_p-1))
    h1 = Polynomial(np.array([h1_elem]*n), base)
    h = np.array([h1]*_l, dtype=Polynomial)

    A = gen(seed, base, n, _l)


if __name__ == "__main__":
    seed = np.random.uniform(size=n).round().astype(int)
    key_gen(seed)
