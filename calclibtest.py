import pytest
import calclib as cl

@pytest.fixture()
def test_decompose():
    string = 'x+4'
    list = ['x+4']
    test = cl.decompose(string)
    assert test == list