import os
import csv
import time
import configure


def path(file_name):
    return os.path.join(configure.base_path, file_name)


class Reader:
    def __init__(self, file_path):
        self.__file_pointer = open(file_path, 'r', encoding='utf-8')
        self.__csv_reader = csv.reader(self.__file_pointer, delimiter=',')

    def __del__(self):
        try:
            self.__file_pointer.close()
        finally:
            pass

    def __iter__(self):
        return self.__csv_reader

    def read(self, numeric=False):
        data = []
        for row in self:
            if numeric:
                row = [int(d) if d.isdigit() else d for d in row]
            data.append(row)
        return data


class Writer:
    def __init__(self, file_path):
        self.__file_pointer = open(file_path, 'w', encoding='utf-8', newline='')
        self.__csv_writer = csv.writer(self.__file_pointer, delimiter=',')

    def __del__(self):
        try:
            self.__file_pointer.close()
        finally:
            pass

    def write_row(self, row):
        self.__csv_writer.writerow(row)

    def write(self, data):
        for row in data:
            self.write_row(row)


def state(function):
    def _state(*args, **kwargs):
            start_time = time.time()
            function_return = function(*args, **kwargs)
            end_time = time.time()
            pass_time = end_time - start_time
            output = '{}(): {}'.format(function.__name__, time.strftime('%H:%M:%S', time.gmtime(pass_time)))
            print(output)
            return function_return
    _state.__name__ = function.__name__
    return _state
