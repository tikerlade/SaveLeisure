import math


def inc(x):
    return x + 1


def test_answer():
    assert inc(4) == 5


def test_another():
    assert sorted([3, 1, 2]) == [1, 2, 3]


def test_sin():
    assert math.sin(0) == 0
