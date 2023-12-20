import numpy as np
from src.Saber import Saber
from src.SaberConfiguration import LIGHT_SABER, SABER, FIRE_SABER


m = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
# m = np.array([1, 0] * 128)  # n = m.size = 256
n = m.size
config = SABER
config.n = m.size
saber = Saber(saber_configuration=config)
s, (seed_A, b) = saber.generate_key()
print("Key set.")
# r = np.random.uniform(size=n).round().astype(int)
print("r seed set.")

cryptogram = saber.encrypt(m, seed_A, b)
print(f"Encrypted: {cryptogram}")

decrypted_m = saber.decrypt(cryptogram, s)
print(f"Decrypted: {decrypted_m.coefficients}")
print(f"Expected: {m}")
