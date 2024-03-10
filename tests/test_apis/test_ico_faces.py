import h3


def test_icosahedron_faces():
    """
    get_icosahedron_faces is kind of a special case, because it always returns
    a list of integers no matter the API
    """
    answers = {
        '804dfffffffffff': [2, 3, 7, 8, 12],
        '80c1fffffffffff': [13],
        '80bbfffffffffff': [15, 16],
    }

    interfaces = [
        (h3.api.basic_str, lambda x: x),
        (h3.api.basic_int, h3.str_to_int),
        (h3.api.memview_int, h3.str_to_int),
        (h3.api.numpy_int, h3.str_to_int),
    ]

    for api, conv in interfaces:
        for h in answers:
            expected = answers[h]

            h = conv(h)  # convert to int or str, depending on API
            out = api.get_icosahedron_faces(h)

            assert isinstance(out, list)
            assert set(out) == set(expected)
