from asyncio.windows_events import NULL
from contextlib import nullcontext
import json
import os

class Job():

    def __init__(self, dir: str):
        self.timeout = 10
        self._dir = dir
        self._data_dict = NULL

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

    def _build_percent_values_from_steps(self, steps) -> list:
        res = []
        if steps < 1:
            steps = 2
        step = 100 / (steps-1)
        i = 0 - step
        while i < 100:
            i += step
            res.append(round(i))
        return res

    def _build_filelist_sound(self):
        if 'number' not in self._data_dict:
            return False
        if 'name' not in self._data_dict:
            return False
        if 'sound' not in self._data_dict:
            return False

        po_name = f"PO-{self._data_dict['number']}-{self._data_dict['name']}"

        if not (isinstance(self._data_dict['sound'], list)):
            return

        for i in range(len(self._data_dict['sound'])):
            elem = self._data_dict['sound'][i]

            if 'button' not in elem:
                print('error: "button" missing in json sound section')
                raise

            if 'name' not in elem:
                print('error: "name" missing in json sound section')
                raise

            if 'a' not in elem:
                print('error: "a" missing in json sound section')
                raise

            if 'b' not in elem:
                print('error: "b" missing in json sound section')
                raise

            button = elem['button']
            name = elem['name']
            name = name.replace(' ', '_')
            a = elem['a']
            b = elem['b']

            base_file_name = f"{po_name}-sound-B{str(button).zfill(2)}-{name}"

            values_a=NULL
            values_b=NULL

            if a=="percent":
                #print("a is a percent value")
                if 'a_step_values' in elem:
                    values_a = elem['a_step_values']
                elif 'a_steps' in elem:
                    values_a = self._build_percent_values_from_steps(elem['a_steps'])
                else:
                    values_a = self._build_percent_values_from_steps(10)
            elif a=="notes":
                if 'notes' not in elem:
                    print('error: "a notes" missing in json sound section')
                    raise
                values_a = elem['notes']
            else:
                print(f'error: unsupported a value "{a}" in json sound section')
                raise

            if b=="percent":
                #print("b is a percent value")
                if 'b_step_values' in elem:
                    values_b = elem['b_step_values']
                elif 'b_steps' in elem:
                    values_b = self._build_percent_values_from_steps(elem['b_steps'])
                else:
                    values_b = self._build_percent_values_from_steps(10)
            else:
                print(f'error: unsupported b value "{b}" in json sound section')
                raise

            for a in values_a:
                for b in values_b:
                    file_name = f"{base_file_name}-{a}-{b}.wav"
                    print (file_name)




    def load(self, file_name) -> object:
        self._data_dict = NULL
        if not os.path.isfile(file_name):
            return self._data

        with open(file_name, 'r') as f:
            self._data_dict = json.load(f)
            #return self._dict2obj(self._data)
            return self._data_dict

    def build_filelist(self) -> bool:
        if 'number' not in self._data_dict:
            return False

        po_name = self._data_dict['number']
        po_name = f"PO-{po_name}"
        # po_dir =  os.path.join(self._dir, po_name)

        # try:
        #     os.makedirs(po_dir, exist_ok=True)
        # except BaseException as err:
        #     print(f"Error {err=}, {type(err)=}")
        #     return False

        sound_list = self._build_filelist_sound()

        return True