from . import ComponentBase
import pandas as pd


class ProducerBase(ComponentBase):
    def __init__(self, *args, **kwargs):
        super(ProducerBase, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.output_data = self.produce(*args, **kwargs)

    def produce(self, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError
