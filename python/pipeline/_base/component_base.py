class ComponentBase(object):
    _component_name = None

    def __init__(self, *args, **kwargs):
        self._input_data = None
        self._output_data = None
        pass

    @classmethod
    def get_component_name(cls) -> str:
        return cls._component_name

    @classmethod
    def set_component_name(cls, name: str):
        cls._component_name = name

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
