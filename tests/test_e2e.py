"""
End-to-End tests containing:
- generate a key and a random message
- encrypt and decrypt the message
- compare a decrypted messages against original one.
"""
import numpy as np


def test_end2end():
    from Saber import Saber

    saber = Saber()

    total_attempts = 10
    successful_attempts = 0
    for _ in range(total_attempts):
        saber.set_key()
        msg = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
        encrypted_msg = saber.encrypt(msg)
        decrypted_msg = saber.decrypt(encrypted_msg)
        if decrypted_msg == msg:
            successful_attempts += 1
    print(f"Successful encryption-decryption attempts ratio: {successful_attempts}/{total_attempts} = "
          f"{successful_attempts/total_attempts:.2f}%.")
