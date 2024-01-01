import inspect


def test_api_copy_match():
    import h3
    import h3.api.numpy_int

    apis = [
        h3.api.basic_int._api_template,
        h3.api.basic_str._api_template,
        h3.api.memview_int._api_template,
        h3.api.numpy_int._api_template,
    ]

    api_set = {inspect.getsource(api) for api in apis}
    assert len(api_set) == 1
