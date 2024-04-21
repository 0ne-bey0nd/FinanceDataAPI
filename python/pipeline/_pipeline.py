import queue
from logger import get_manual_logger

logger = get_manual_logger()

class Pipeline(object):
    def __init__(self, *args, **kwargs):
        self.component_class_queue = queue.Queue()
        self.component_name_to_class_dict = {}
        self.is_running = False
        self.input_data = None
        self._output_data = None

    def add_component_class(self, component_class): # todo: 加入参数，可以设计为add task
        self.component_class_queue.put(component_class)
        self.component_name_to_class_dict[component_class.get_component_name()] = component_class

    def run(self):
        self.is_running = True
        pre_component_output = self.input_data
        while not self.component_class_queue.empty():
            component_class = self.component_class_queue.get()
            component_object = component_class()
            component_object.input_data = pre_component_output
            component_object.run()
            pre_component_output = component_object.output_data
        self.is_running = False
        self._output_data = pre_component_output

    @property
    def output_data(self):
        return self._output_data


if __name__ == '__main__':
    from pipeline import ComponentBase
    import inspect
    import os
    import importlib

    PIPELINE_MODULE_PATH = os.path.dirname(importlib.import_module('pipeline').__file__)
    components_path = os.path.join(PIPELINE_MODULE_PATH, 'components')

    pipeline_module_path_list = []
    component_class_list = []
    component_name_to_class_dict = {}

    # 遍历components目录下的所有py文件
    for root, dirs, files in os.walk(components_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                pipeline_module_path_list.append(file_path)

    from pathlib import Path


    def _get_module_name_by_path(path, base):
        return '.'.join(path.resolve().relative_to(base.resolve()).with_suffix('').parts)


    for pipeline_module_path in pipeline_module_path_list:
        module_name = _get_module_name_by_path(Path(pipeline_module_path), Path(PIPELINE_MODULE_PATH))
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, ComponentBase):
                component_class_list.append(obj)
                component_name_to_class_dict[obj.get_component_name()] = obj

    print(component_name_to_class_dict)

    pipeline = Pipeline()
    pipeline.add_component_class(component_name_to_class_dict['BaoStockTradeDayProducer'])
    pipeline.add_component_class(component_name_to_class_dict['BaoStockTradeDayProcessor'])
    pipeline.add_component_class(component_name_to_class_dict['BaoStockTradeDayStorager'])

    print(pipeline.component_name_to_class_dict)

    pipeline.run()

    print(pipeline.output_data)
