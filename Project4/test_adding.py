import mathfun as fun
from pytest import approx

def test_addints():
	assert fun.add(1, 1) == 2

def test_addfloats():
	assert fun.add(1.5, 1.7) == approx(3.1)
