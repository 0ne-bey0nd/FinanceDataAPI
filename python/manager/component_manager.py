import sys
import pipeline
from pathlib import Path
import inspect
import os
import importlib
from utils.path_utils import get_module_name_by_path
from utils.log_utils import get_logger

logger = get_logger()

PIPELINE_MODULE_PATH = os.path.dirname(pipeline.__file__)
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
        return self._component_name_to_class_dict.get(component_name, None)

    def register_component(self):
        components_path = os.path.join(PIPELINE_MODULE_PATH, 'components')
        self.__register_component_from_dir(components_path)

    def import_and_flush_module(self, module_name):
        if module_name in sys.modules:
            # module = importlib.reload(sys.modules[module_name])
            del sys.modules[module_name]
        module = importlib.import_module(module_name)
        # 再import其实不会重载from xxx import 的组件
        return module

    def __register_component_from_dir(self, components_path):
        pipeline_module_path_list = []

        # 导入components目录下的所有py文件
        for root, dirs, files in os.walk(components_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    pipeline_module_path_list.append(file_path)

        for pipeline_module_path in pipeline_module_path_list:
            logger.info(f"Registering components from {pipeline_module_path}")
            module_name = get_module_name_by_path(Path(pipeline_module_path), Path(MODULE_ROOT_PATH))
            module = self.import_and_flush_module(module_name)

            for name, obj in inspect.getmembers(module):
                if self.check_component_class(obj):
                    if self._component_name_to_class_dict.get(obj.get_component_name(), None):
                        # 因为直接import component所在的module不会重载from xxx import 的组件，所以直接通过组件类对象重载
                        logger.info(f"component exists: {obj.get_component_name()}")
                        new_component_class_module = self.__flush_a_component_module(obj.get_component_name())
                        for new_name, new_obj in inspect.getmembers(new_component_class_module):
                            if self.check_component_class(new_obj):
                                new_obj.set_component_name(obj.get_component_name())
                                logger.info(f"Registering component: {new_obj.get_component_name()}")
                                self.update_component(new_obj.get_component_name(), new_obj)
                    else:
                        logger.info(f"Registering component: {obj.get_component_name()}")
                        self.update_component(obj.get_component_name(), obj)

        logger.info(f"component_name_to_class_dict: {self._component_name_to_class_dict}")

    def check_component_class(self, component_class):
        return inspect.isclass(component_class) and issubclass(component_class,
                                                               pipeline.ComponentBase) and component_class != pipeline.ComponentBase

    def update_component(self, component_name, component_class):  # todo: this is not thread safe !
        self._component_name_to_class_dict[component_name] = component_class

    def delete_component(self, component_name):  # todo: this is not thread safe !
        del self._component_name_to_class_dict[component_name]

    def flush_all_component_module(self):  # todo: this is not thread safe !
        for component_name, component_class in self._component_name_to_class_dict.items():
            try:
                module_name = component_class.__module__
                module = importlib.reload(sys.modules[module_name])
                logger.info(f"Flushed module: {module}")
            except Exception as e:
                logger.error(f"Error: {e}")
                self.delete_component(component_name)

    def __flush_a_component_module(self, component_name):
        try:
            component_class = self.get_component_class_by_name(component_name)
            if not component_class:
                return
            module_name = component_class.__module__
            # module = importlib.reload(sys.modules[module_name])

            del sys.modules[module_name]
            self.delete_component(component_name)
            module = importlib.import_module(module_name)

            logger.info(f"Flushed module: {module}")
            return module
        except Exception as e:
            logger.error(f"Error: {e}")
            self.delete_component(component_name)

if __name__ == '__main__':
    component_manager = ComponentManager.get_instance()
    component_manager.register_component()
    input()
    component_manager.register_component()
