"""
H. Czader, M. Szubert, J. Fortuna, A. Klekowski
Postquantum Cryptography classes
AGH University of Cracow

Saber.PKE parameter sets.
Based on the official paper "SABER: Mod-LWR based KEM (Round 3 Submission)"
"""
from dataclasses import dataclass


@dataclass()
class SaberConfiguration:
    # n, l: The degree n = 256 of the polynomial ring Z_q[X] / (X^n + 1) and the rank l of
    # the module which determine the dimension of the underlying lattice problem as l · n.
    # Increasing the dimension of the lattice problem increases the security, but reduces the correctness.
    l: int
    n: int
    # q, p, T: The moduli involved in the scheme are chosen to be powers of 2, in particular
    # q=2^epsilon_q, p=2^epsilon_p and T=2^epsilon_T with epsilon_q > epsilon_p > epsilon_T.
    # A higher choice for parameters p and T, will result in lower security, but higher correctness.
    epsilon_q: int
    epsilon_p: int
    epsilon_T: int
    # µ: The coefficients of the secret vectors s and s` are sampled according to a centered
    # binomial distribution β_µ with parameter µ, where µ < p. A higher value for µ
    # will result in a higher security, but a lower correctness of the scheme.
    mi: int


LIGHT_SABER = SaberConfiguration(l=2, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=3, mi=10)
SABER = SaberConfiguration(l=3, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=4, mi=8)
FIRE_SABER = SaberConfiguration(l=4, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=6, mi=6)
