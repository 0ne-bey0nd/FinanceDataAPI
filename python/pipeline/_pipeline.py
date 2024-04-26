import queue
from typing import Type
from pipeline import ComponentBase
from utils.log_utils import get_logger

logger = get_logger()

class Pipeline(object):
    def __init__(self, *args, **kwargs):
        self.component_name_to_class_dict = {}
        self.is_running = False
        self.input_data = None

        self._task_queue: queue.Queue[tuple[Type[ComponentBase], dict]] = queue.Queue()
        self._output_data = None

    def add_component(self, component_class: Type[ComponentBase], component_arguments: dict):
        self._task_queue.put((component_class, component_arguments))
        self.component_name_to_class_dict[component_class.get_component_name()] = component_class

    def run(self):  # todo: 暂时使用pipeline作为运行对象，后续考虑使用其他线程模型
        self.is_running = True
        pre_component_output = self.input_data
        while not self._task_queue.empty():
            component_class, component_arguments = self._task_queue.get()
            logger.info(f"begin to run component: {component_class.get_component_name()}")
            # logger.info(f"is subclass: {issubclass(component_class, ComponentBase)}")
            component_object = component_class()
            component_object.input_data = pre_component_output
            component_object.run(**component_arguments)
            pre_component_output = component_object.output_data
            logger.info(f"finish run component: {component_class.get_component_name()}")
        self.is_running = False
        self._output_data = pre_component_output

    @property
    def output_data(self):
        return self._output_data


if __name__ == '__main__':
    from pipeline import  Pipeline
    from manager.component_manager import ComponentManager

    component_manager = ComponentManager.get_instance()
    component_manager.register_component()  # 注册组件

    pipeline = Pipeline()
    pipeline.add_component(component_manager.get_component_class_by_name('BaoStockTradeDayProducer'),{})
    pipeline.add_component(component_manager.get_component_class_by_name('BaoStockTradeDayProcessor'),{})
    pipeline.add_component(component_manager.get_component_class_by_name('BaoStockTradeDayStorager'),{})

    print(pipeline.component_name_to_class_dict)
    pipeline.run()
    print(pipeline.output_data)