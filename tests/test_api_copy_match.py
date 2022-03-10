import inspect


def test_api_copy_match():
    import h3
    import h3.api.numpy_int

    apis = [
        h3.api.basic_int._copy_of_api,
        h3.api.basic_str._copy_of_api,
        h3.api.memview_int._copy_of_api,
        h3.api.numpy_int._copy_of_api,
    ]

    apis = map(inspect.getsource, apis)
    apis = set(apis)

    assert len(apis) == 1
