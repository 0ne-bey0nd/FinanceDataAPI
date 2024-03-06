from . import ComponentBase
import pandas as pd


class ProcessorBase(ComponentBase):
    def __init__(self, *args, **kwargs):
        super(ProcessorBase, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.output_data = self.process(self.input_data, *args, **kwargs)

    def process(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError
