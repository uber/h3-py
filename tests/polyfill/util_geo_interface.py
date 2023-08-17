class MockGeoInterface:
    def __init__(self, dictionary):
        assert isinstance(dictionary, dict)
        self.dictionary = dictionary

    @property
    def __geo_interface__(self):
        return self.dictionary
