from abc import abstractmethod
from collections import Iterable
import tool


class Work:
    def __init__(self, **kwargs):
        self.__arguments = kwargs

    def __call__(self, **kwargs):
        self.__arguments = kwargs

    @abstractmethod
    def function(self):
        pass

    def arguments(self):
        return self.__arguments


class WorkFlow:
    def __init__(self, inertness=False):
        self.__input = None
        self.__output = None
        self.__work = None
        self.__inertness_input = None
        self.__arguments = None
        self.__ready = False
        self.__inertness = inertness
        self.__stack = []

    def input(self):
        return self.__input

    def output(self):
        return self.__output

    def work(self):
        return self.__work

    def inertness_input(self):
        return self.__inertness_input

    def __repr__(self):
        def _generate_io_string(thing):
            _string = ''
            if thing is not None:
                if isinstance(thing, str):
                    _string += ' >> \'{}\''.format(thing)
                else:
                    _string += ' >> {}'.format(thing)
            return _string

        def _generate_work_string(thing):
            _string = ''
            if thing is not None:
                arguments_string = ', '.join(str(k) + '=' + str(v) for k, v in thing.arguments().items())
                _string += ' >> {}({})'.format(thing.__class__.__name__, arguments_string)
            return _string
        string = 'WorkFlow'
        string += _generate_io_string(self.__input)
        string += _generate_work_string(self.__work)
        string += _generate_io_string(self.__output)
        for item in self.__stack:
            if isinstance(item, Work):
                string += _generate_work_string(item)
            else:
                string += _generate_io_string(item)
        return string

    def __str__(self):
        return self.__repr__()

    def __rshift__(self, other):
        if self.__ready:
            self.__stack.append(other)
        else:
            if isinstance(other, Work):
                self._set_work(other)
            elif isinstance(other, tuple):
                if self.__work is None:
                    self._set_input(other)
                else:
                    self._set_output(other)
                    self._check_run()
            elif isinstance(other, str):
                if self.__work is None:
                    self._set_input(other)
                else:
                    self._set_output(other)
                    self._check_run()
            elif isinstance(other, WorkFlow):
                if other.input() is not None:
                    self >> other.input()
                if other.work() is not None:
                    self >> other.work()
                if other.output() is not None:
                    self >> other.output()
            elif other is None:
                self._check_run(no_output=True)
        return self

    def __rrshift__(self, other: str):
        self.__inertness_input = other
        self.__inertness = True
        if self.__input is None:
            self._set_input(other)
        return self

    def __getitem__(self, item):
        new_workflow = WorkFlow()
        if isinstance(self.__input, str):
            new_workflow >> self.__input
        else:
            new_workflow >> self.__input[item]
        return new_workflow

    def _generate_input(self):
        input_list = []
        if self.__input is not None:
            _input = self.__input
            if not isinstance(_input, tuple):
                _input = [_input]
            for item in _input:
                if isinstance(item, WorkFlow):
                    item.passive_run()
                    workflow_input = item.input()
                    if isinstance(workflow_input, tuple):
                        input_list += [tool.path(t) for t in workflow_input]
                    else:
                        input_list.append(tool.path(workflow_input))
                else:
                    input_list.append(tool.path(item))
        return input_list

    def _generate_output(self):
        output_list = []
        if self.__output is not None:
            _output = self.__output
            if not isinstance(_output, tuple):
                _output = [_output]
            for item in _output:
                if isinstance(item, WorkFlow):
                    workflow_inertness_input = item.inertness_input()
                    if isinstance(workflow_inertness_input, tuple):
                        output_list += [tool.path(t) for t in workflow_inertness_input]
                    else:
                        output_list.append(tool.path(workflow_inertness_input))
                else:
                    output_list.append(tool.path(item))
        return output_list

    def _set_input(self, thing):
        self.__input = thing
        self._check_run()

    def _set_work(self, thing):
        self.__work = thing
        self._check_run()

    def _set_output(self, thing):
        self.__output = thing
        self._check_run()

    def _check_run(self, no_output=False):
        if self.__input is not None and self.__work is not None and (self.__output is not None or no_output):
            self.__arguments = self._generate_input() + self._generate_output()
            if self.__inertness:
                self.__ready = True
            else:
                self.run()

    def run(self):
        temp_output = self.__output
        self.__work.function()(*self.__arguments, **self.__work.arguments())
        self.__work = None
        self.__arguments = None
        self.__input = self.__output
        self.__output = None
        self.__inertness_input = None
        self.__ready = False
        if isinstance(temp_output, Iterable):
            for item in temp_output:
                if isinstance(item, WorkFlow):
                    item.active()
        temp_stack = self.__stack
        self.__stack = []
        for item in temp_stack:
            self >> item

    def passive_run(self):
        if self.__ready:
            self.run()

    def active(self):
        self.__inertness = False
        self.passive_run()
