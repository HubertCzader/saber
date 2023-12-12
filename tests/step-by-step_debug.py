import numpy as np
from src.Saber import Saber


m = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
# m = np.array([1, 0] * 128)  # n = m.size = 256
n = m.size
saber = Saber(n=n, rebase_alter=False)
saber.set_key()
print("Key set.")
r = np.random.uniform(size=n).round().astype(int)
print("r seed set.")

cryptogram = saber.encrypt(m, r, verbose=True)
print(f"Encrypted: {cryptogram}")

decrypted_m = saber.decrypt(cryptogram)
print(f"Decrypted: {decrypted_m.coefficients}")
print(f"Expected: {m}")
