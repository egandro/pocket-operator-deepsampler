from asyncio.windows_events import NULL
import json
import os

class Job():

    def __init__(self):
        self.timeout = 10

    def load(self, file_name) -> object:
        if not os.path.isfile(file_name):
            return NULL

        with open(file_name, 'r') as f:
            data = json.load(f)
            return data
