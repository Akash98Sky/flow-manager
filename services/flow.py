from services.tasks import FetchDataTask, ProcessDataTask, StoreDataTask

from ..helpers.models import Flow as FlowModel

class Flow:
    def __init__(self, flow_data: FlowModel):
        self.flow_data = flow_data

    def execute(self):
        tasks = []
        for task_data in self.flow_data.tasks:
            if task_data.name == 'task1':
                tasks.append(FetchDataTask())
            elif task_data.name == 'task2':
                tasks.append(ProcessDataTask())
            elif task_data.name == 'task3':
                tasks.append(StoreDataTask())

        for i, task in enumerate(tasks):
            task.execute()
            if i < len(tasks) - 1:
                # Evaluate conditions
                pass
