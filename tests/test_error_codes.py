import pytest

import h3

# todo: maybe check the `check_for_error` function behavior directly?


h3_exceptions = {
    # h3.UnknownH3ErrorCode
    h3.H3BaseException: None,

    h3.H3GridNavigationError: None,
    h3.H3MemoryError: None,
    h3.H3ValueError: None,

    h3.H3FailedError: 1,
    h3.H3DomainError: 2,
    h3.H3LatLngDomainError: 3,
    h3.H3ResDomainError: 4,
    h3.H3CellInvalidError: 5,
    h3.H3DirEdgeInvalidError: 6,
    h3.H3UndirEdgeInvalidError: 7,
    h3.H3VertexInvalidError: 8,
    h3.H3PentagonError: 9,
    h3.H3DuplicateInputError: 10,
    h3.H3NotNeighborsError: 11,
    h3.H3ResMismatchError: 12,
    h3.H3MemoryAllocError: 13,
    h3.H3MemoryBoundsError: 14,
    h3.H3OptionInvalidError: 15,
}


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
