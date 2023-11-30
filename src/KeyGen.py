from typing import Union, Tuple

from src.Polynomial import Polynomial
from src.ModuloBase import ModuloBase
from Crypto.Hash import SHAKE128
import numpy as np


def gen(seed: np.array, base: ModuloBase, n: int, _l: int, epsilon_q: int):
    # todo: check if seed is of length n, or trim/extend it to size
    byte_seed = np.packbits(seed.reshape((-1, 8))).tobytes()
    print(byte_seed)
    shake = SHAKE128.new()
    shake.update(byte_seed)

    A_len = epsilon_q
    raw = shake.read(int(_l*_l*n/8*A_len))
    bytes_array = np.frombuffer(raw, dtype=np.uint8)
    nums = np.unpackbits(bytes_array)
    nums = nums.reshape(_l, _l, n, A_len)
    A = np.ndarray((_l, _l), dtype=Polynomial)
    for A_row in range(nums.shape[0]):
        for A_col in range(nums.shape[1]):
                poly = nums[A_row][A_col]
                a = [coeff.dot(2**np.arange(coeff.size)[::-1]) for coeff in poly]
                A[A_row][A_col] = Polynomial(a, base)
    return A




# generate a public key
# default values conform to the Saber security level
def key_gen(n: int = 256, _l: int = 3, epsilon_p: int = 10, epsilon_q: int = 13,
            mi: int = 8) -> Tuple[np.array, np.array]:
    seed = np.random.uniform(size=n).round().astype(int)

    q = 2 ** epsilon_q

    base = ModuloBase(np.array(([1]+[0]*(n-1)+[1]), dtype=int), q)
    h1_elem = np.power(2, (epsilon_q-epsilon_p-1))
    h1 = Polynomial(np.array([h1_elem]*n), base)
    h = np.array([h1]*_l, dtype=Polynomial)

    A = gen(seed=seed, base=base, n=n, _l=_l, epsilon_q=epsilon_q)

    r = np.random.uniform(size=n).round().astype(int)
    s = np.array([Polynomial(np.random.binomial(n=mi, p=r, size=n), base) for _ in range(_l)])
    print(s.shape)

    b = (np.matmul(A.transpose(), h) % q) >> (epsilon_q-epsilon_p)
    print(b)

    return seed, b


if __name__ == "__main__":
    key_gen()
