"""

"""
from dataclasses import dataclass

import pytest

# tests ####################################################


def test_key_generation(light_saber_test_cases):
    from KeyGen import key_gen

    for kat_test_case_data in light_saber_test_cases:
        print(kat_test_case_data)

# dataclasses ##############################################


@dataclass()
class KatTestCaseData:
    count: int
    seed: str
    pk: str
    sk: str
    ct: str
    ss: str

# fixtures ##################################################


@pytest.fixture
def light_saber_test_cases():
    with open("kat_files/PQCkemKAT_1568.rsp", "r") as file:
        lines = file.read().splitlines()
    test_cases = []
    for i in range(2, len(lines), 7):
        tmp_kat = KatTestCaseData(
            count=int(lines[i].split(" = ")[1]),
            seed=lines[i+1].split(" = ")[1],
            pk=lines[i+2].split(" = ")[1],
            sk=lines[i+3].split(" = ")[1],
            ct=lines[i+4].split(" = ")[1],
            ss=lines[i+5].split(" = ")[1]
        )
        test_cases.append(tmp_kat)
    return test_cases
