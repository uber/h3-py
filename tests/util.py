import pytest


def same_set(a, b):
    """Test if two collections are the same if taken as sets"""
    set_a = set(a)
    set_b = set(b)

    assert len(a) == len(b) == len(set_a) == len(set_b)

    return set_a == set_b


def approx2(a, b):
    if len(a) != len(b):
        return False

    return all(
        x == pytest.approx(y)
        for x, y in zip(a, b)
    )
