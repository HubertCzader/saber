"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Post-quantum Cryptography classes
AGH University of Cracow

End-to-End tests containing:
- generate a key and a random message
- encrypt and decrypt the message
- compare a decrypted messages against original one.
"""
import time

import numpy as np


def test_end2end():
    from Saber import Saber

    saber = Saber()

    total_attempts = 100_000
    successful_attempts = 0
    times = []

    for _ in range(total_attempts):
        start_time = time.time()
        s, (seed, b) = saber.generate_key()
        msg = np.random.randint(2, size=256)
        cryptogram = saber.encrypt(msg, seed, b)
        decrypted_msg = saber.decrypt(cryptogram, b)
        end_time = time.time()
        times.append(end_time-start_time)
        if np.array_equal(decrypted_msg, msg):
            successful_attempts += 1
    print(f"Successful encryption-decryption attempts ratio: {successful_attempts}/{total_attempts} = "
          f"{successful_attempts/total_attempts:.2f}%.")
    print(f"Average key generation-encryption-decryption time: {(sum(times) / total_attempts):2f} sec.")
