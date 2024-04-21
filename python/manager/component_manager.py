from logger import get_manual_logger
from pipeline import ComponentBase
from pathlib import Path
import inspect
import os
import importlib

logger = get_manual_logger()


def _get_module_name_by_path(path, base):
    return '.'.join(path.resolve().relative_to(base.resolve()).with_suffix('').parts)


PIPELINE_MODULE_PATH = os.path.dirname(importlib.import_module('pipeline').__file__)
MODULE_ROOT_PATH = Path(PIPELINE_MODULE_PATH).parent


class ComponentManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(ComponentManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self._component_name_to_class_dict = {}

        ...

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_component_class_by_name(self, component_name):
        return self._component_name_to_class_dict.get(component_name)

    def register_component(self):

        components_path = os.path.join(PIPELINE_MODULE_PATH, 'components')
        self.__register_component_from_dir(components_path)

    def __register_component_from_dir(self, components_path):
        pipeline_module_path_list = []
        component_class_list = []
        self._component_name_to_class_dict = {}

        # 导入components目录下的所有py文件
        for root, dirs, files in os.walk(components_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    pipeline_module_path_list.append(file_path)

        for pipeline_module_path in pipeline_module_path_list:
            logger.debug(f"Registering components from {pipeline_module_path}")
            module_name = _get_module_name_by_path(Path(pipeline_module_path), Path(MODULE_ROOT_PATH))
            logger.debug(module_name)
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, ComponentBase) and obj != ComponentBase:
                    component_class_list.append(obj)
                    self._component_name_to_class_dict[obj.get_component_name()] = obj

        logger.debug(f"component_name_to_class_dict: {self._component_name_to_class_dict}")



