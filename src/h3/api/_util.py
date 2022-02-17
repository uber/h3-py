def _update_globals(klass, _globals):
    _methods = {
        name: getattr(klass, name)
        for name in dir(klass)
        if callable(getattr(klass, name)) and not name.startswith("_")
    }

    _globals.update(_methods)
