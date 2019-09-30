import h3.api.memview_int as h3


def test1():
    assert h3.geo_to_h3(37.7752702151959, -122.418307270836, 9) == 617700169958293503
