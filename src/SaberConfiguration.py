"""
Saber.PKE parameter sets.
Based on the official paper "SABER: Mod-LWR based KEM (Round 2 Submission)"
"""
from dataclasses import dataclass


@dataclass()
class SaberConfiguration:
    l: int
    n: int
    epsilon_q: int
    epsilon_p: int
    epsilon_T: int
    mi: int


LIGHT_SABER = SaberConfiguration(l=2, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=3, mi=10)
SABER = SaberConfiguration(l=3, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=4, mi=8)
FIRE_SABER = SaberConfiguration(l=4, n=256, epsilon_q=13, epsilon_p=10, epsilon_T=6, mi=6)
