from abc import abstractmethod
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
        self.__arguments = None
        self.__inertness = inertness

    def __repr__(self):
        string = 'WorkFlow'
        if self.__input is not None:
            if isinstance(self.__input, str):
                string += ' >> \'{}\''.format(self.__input)
            else:
                string += ' >> {}'.format(self.__input)
        if self.__work is not None:
            arguments_string = ', '.join(str(k) + '=' + str(v) for k, v in self.__work.arguments().items())
            string += ' >> {}({})'.format(self.__work.__class__.__name__, arguments_string)
        if self.__output is not None:
            if isinstance(self.__output, str):
                string += ' >> \'{}\''.format(self.__output)
            else:
                string += ' >> {}'.format(self.__output)
        return string

    def __str__(self):
        return self.__repr__()

    def __rshift__(self, other):
        if isinstance(other, Work):
            self.__work = other
        elif isinstance(other, list):
            if self.__work is None:
                self.__input = other
            else:
                self.__output = other
                if isinstance(self.__input, str):
                    self.__arguments = [tool.path(self.__input)] + [tool.path(item) for item in self.__output]
                else:
                    self.__arguments = [tool.path(item) for item in self.__input] + [tool.path(item) for item in self.__output]
                if self.__inertness:
                    self.__ready = True
                else:
                    self.run()
        elif isinstance(other, str):
            if self.__work is None:
                self.__input = other
            else:
                if self.__input is None:
                    self.__input = other
                else:
                    self.__output = other
                    if isinstance(self.__input, str):
                        self.__arguments = [tool.path(self.__input), tool.path(self.__output)]
                    else:
                        self.__arguments = [tool.path(item) for item in self.__input] + [tool.path(self.__output)]
                    if self.__inertness:
                        self.__ready = True
                    else:
                        self.run()
        elif other is None:
            if self.__input is not None and self.__work is not None:
                if isinstance(self.__input, str):
                    self.__arguments = [tool.path(self.__input)]
                else:
                    self.__arguments = [tool.path(item) for item in self.__input]
                if self.__inertness:
                    self.__ready = True
                else:
                    self.run()
        return self

    def __getitem__(self, item):
        new_workflow = WorkFlow()
        if isinstance(self.__input, str):
            new_workflow >> self.__input
        else:
            new_workflow >> self.__input[item]
        return new_workflow

    def run(self):
        self.__work.function()(*self.__arguments, **self.__work.arguments())
        self.__work = None
        self.__arguments = None
        self.__input = self.__output
        self.__output = None
