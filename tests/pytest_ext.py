import functools
from copy import deepcopy
from unittest import mock

import cloudpickle.cloudpickle_fast as pickle


def cache_mock_fixture(fixture):
    val = {}

    @functools.wraps(fixture)
    def reset_mock(*args, **kwargs):
        k = ",".join(f"{key}={id(value)}" for key, value in kwargs.items())

        if k in val:
            val[k].reset_mock()
            print(f"reset {fixture.__name__}({k}) = {id(val[k])}")
        else:
            val[k] = fixture(*args, **kwargs)
            print(f"create {fixture.__name__}({k}) = {id(val[k])}")
        return val[k]

    return reset_mock


def clone_on_request(serialize=False):
    def decorated_fixture(fixture):
        val = {}
        serial = {}

        @functools.wraps(fixture)
        def copy_fixture(*args, **kwargs):
            nonlocal val, serial
            k = ",".join(f"{key}={id(value)}" for key, value in kwargs.items())
            if k not in val:
                val[k] = fixture(*args, **kwargs)
                # print(f"create {fixture.__name__}({k}) = {id(val)}")
                if serialize:
                    val[k].__reduce__ = lambda self: (mock.MagicMock, ())
                    serial[k] = pickle.dumps(val[k])
            # print(f"clone {fixture.__name__}({k}) = {id(val)}")
            v = pickle.loads(serial[k]) if k in serial else deepcopy(val[k])
            print(v)
            return v

        return copy_fixture

    return decorated_fixture


def qualified_name(spec):
    return f"{spec.__module__}.{spec.__qualname__}"


class MockCache:
    def __init__(self):
        self.dictionary = {}

    def __getitem__(self, key):
        return deepcopy(self.dictionary[key])
        # val = self.dictionary[key]
        # val.reset_mock()
        # return val

    def __contains__(self, key):
        return key in self.dictionary

    def patch(self, spec, key=None):
        stub = mock.patch(spec, autospec=True).start()
        self.dictionary[key or spec] = stub
        # return stub
        return self.dictionary[key or spec]
