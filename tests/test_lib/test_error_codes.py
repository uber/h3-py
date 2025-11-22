import pytest

import h3
from h3._cy import (
    error_code_to_exception,
    get_H3_ERROR_END,
)

# todo: maybe check the `check_for_error` function behavior directly?


h3_exceptions = {
    # h3.UnknownH3ErrorCode
    h3.H3BaseException: None,

    h3.H3GridNavigationError: None,
    h3.H3MemoryError: None,
    h3.H3ValueError: None,
}

for e in range(1, get_H3_ERROR_END()):
    ex = error_code_to_exception(e)
    h3_exceptions[ex] = e


def test_num_error_codes():
    assert get_H3_ERROR_END() >= 20
    assert error_code_to_exception(19) == h3.H3DeletedDigitError

    # H3_ERROR_END (and beyond) shouldn't be a valid error code
    code = get_H3_ERROR_END()
    assert isinstance(
        error_code_to_exception(code),
        h3.UnknownH3ErrorCode
    )

    code = get_H3_ERROR_END() + 1
    assert isinstance(
        error_code_to_exception(code),
        h3.UnknownH3ErrorCode
    )


def test_error_codes_match():
    """
    Should match the error codes given in `h3api.h.in` in the core C lib.
    """

    for err, code in h3_exceptions.items():
        assert err.h3_error_code == code


def test_unknown():
    weird_code = 1234

    with pytest.raises(h3.UnknownH3ErrorCode) as excinfo:
        raise h3.UnknownH3ErrorCode(weird_code)
    err = excinfo.value

    assert isinstance(err, h3.UnknownH3ErrorCode)
    assert err.args == (weird_code,)


def test_attributes():
    # errors always have an `h3_error_code` attribute
    for err in h3_exceptions:
        x = err.h3_error_code
        assert (x is None) or (x > 0)

    # UnknownH3ErrorCode is a bit of a special case
    weird_code = 1234
    with pytest.raises(h3.UnknownH3ErrorCode) as excinfo:
        raise h3.UnknownH3ErrorCode(weird_code)
    err = excinfo.value

    assert err.h3_error_code is None
    assert err.args == (weird_code,)
