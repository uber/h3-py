import doctest
import importlib

import pytest

import h3


@pytest.mark.parametrize('modname', ['h3.api.basic_str', 'h3._h3shape'])
def test_docstring_examples(modname):
    """
    The examples in the docstrings are written for the default (`str`) API.
    Make sure they keep matching what the functions actually return.
    """
    mod = importlib.import_module(modname)

    results = doctest.testmod(
        mod,
        extraglobs={'h3': h3},
        optionflags=doctest.NORMALIZE_WHITESPACE,
    )

    assert results.attempted > 0
    assert results.failed == 0
