class ComponentBase(object):

    def __init__(self, *args, **kwargs):
        self._input_data = None
        self._output_data = None

        pass

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, data):
        self._input_data = data

    @property
    def output_data(self):
        return self._output_data

    @output_data.setter
    def output_data(self, data):
        self._output_data = data

    def run(self, *args, **kwargs):
        raise NotImplementedError
