import numpy as np


def test_end2end():
    from Saber import Saber

    saber = Saber()

    for _ in range(10):
        saber.set_key()
        msg = np.array([1, 0, 0, 0, 1, 1, 0, 1], dtype=int)
        encrypted_msg = saber.encrypt(msg)
        decrypted_msg = saber.decrypt(encrypted_msg)
        print(encrypted_msg)
        print(decrypted_msg)
        assert decrypted_msg == msg