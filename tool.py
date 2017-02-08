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


class Writer:
    def __init__(self, file_path):
        self.__file_pointer = open(file_path, 'w', encoding='utf-8', newline='')
        self.__csv_writer = csv.writer(self.__file_pointer, delimiter=',')

    def __del__(self):
        try:
            self.__file_pointer.close()
        finally:
            pass

    def write(self, row):
        self.__csv_writer.writerow(row)


def state(function):
    def _state(*args, **kwargs):
            start_time = time.time()
            function_return = function(*args, **kwargs)
            end_time = time.time()
            pass_time = end_time - start_time
            output = '{}(): {:.2f}s'.format(function.__name__, pass_time)
            print(output)
            return function_return
    return _state
