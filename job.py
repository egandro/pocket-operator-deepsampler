from asyncio.windows_events import NULL
import json
import os

class Job():

    def __init__(self):
        self.timeout = 10

    def _dict2obj(self, d):
        # https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
        if isinstance(d, list):
            d = [self._dict2obj(x) for x in d]
        if not isinstance(d, dict):
            return d
        class C(object):
            pass
        o = C()
        for k in d:
            o.__dict__[k] = self._dict2obj(d[k])
        return o

    def load(self, file_name) -> object:
        if not os.path.isfile(file_name):
            return NULL

        with open(file_name, 'r') as f:
            data = json.load(f)
            return self._dict2obj(data)
