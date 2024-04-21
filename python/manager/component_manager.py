from market_data.pipeline._base import *
from pathlib import Path
import inspect
import os
import importlib
import sys


def _get_module_name_by_path(path, base):
    return '.'.join(path.resolve().relative_to(base.resolve()).with_suffix('').parts)


class ComponentManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ComponentManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self._component_name_to_class_dict = None

        ...

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def register_component(self):

        PIPELINE_MODULE_PATH = os.path.dirname(importlib.import_module('market_data.pipeline').__file__)
        components_path = os.path.join(PIPELINE_MODULE_PATH, 'components')

        self.__register_component_from_dir(components_path)

    def __register_component_from_dir(self, components_path):
        pipeline_module_path_list = []
        component_class_list = []
        self._component_name_to_class_dict = {}

        # 遍历components目录下的所有py文件
        for root, dirs, files in os.walk(components_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    pipeline_module_path_list.append(file_path)

        for pipeline_module_path in pipeline_module_path_list:
            module_name = _get_module_name_by_path(Path(pipeline_module_path), Path(components_path))
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, ComponentBase):
                    component_class_list.append(obj)
                    self._component_name_to_class_dict[obj.get_component_name()] = obj

        print(self._component_name_to_class_dict)
