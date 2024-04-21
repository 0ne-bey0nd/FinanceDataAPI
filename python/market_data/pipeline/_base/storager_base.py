from . import ComponentBase
import pandas as pd
from manager.storage_engine_manager import StorageEngineManager
from logger import get_manual_logger

class StoragerBase(ComponentBase):

    def __init__(self, *args, **kwargs):
        super(StoragerBase, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.output_data = self.storage(self.input_data, *args, **kwargs)

    def storage(self, input_data: pd.DataFrame, *args, **kwargs) -> pd.DataFrame:
        raise NotImplementedError
