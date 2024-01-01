import inspect


def test_api_copy_match():
    import h3

    apis = [
        h3.api.basic_int,
        h3.api.basic_str,
        h3.api.memview_int,
        h3.api.numpy_int,
    ]

    api_set = {inspect.getsource(api) for api in apis}
    assert len(api_set) == 1
