from asyncio import Future

from ..models.flow import Flow, Task, FlowExecutionResult
from .task import Process, Scheduler

class FlowProcessor:
    flow: Flow
    process_map: dict[str, Process]

    scheduler: Scheduler
    future_result: Future[FlowExecutionResult]

    def __init__(self, flow: Flow):
        self.flow = flow
        # Create a mapping from task name to the task process (containing the actual logic of the task)
        self.process_map = {task.name: Process(task) for task in flow.tasks}

        self.scheduler = Scheduler(self.__on_success, self.__on_failure, self.__end_flow)
        self.future_result = Future()

    def __on_success(self, task: Task):
        for condition in self.flow.conditions:
            if condition.source_task == task.name:
                next_task_name = condition.target_task_success
                if next_task_name in self.process_map:
                    return self.scheduler.schedule(self.process_map[next_task_name])
                else:
                    raise ValueError(f"Next task '{next_task_name}' not found in process map.")

        # If no conditions matched, we can consider the flow ended
        self.__end_flow()

    def __on_failure(self, task: Task):
        for condition in self.flow.conditions:
            if condition.source_task == task.name:
                next_task_name = condition.target_task_failure
                if next_task_name in self.process_map:
                    return self.scheduler.schedule(self.process_map[next_task_name])
                else:
                    raise ValueError(f"Next task '{next_task_name}' not found in process map.")

        # If no conditions matched, we can consider the flow ended
        self.__end_flow()

    def __end_flow(self):
        print(f"Flow {self.flow.name} (ID: {self.flow.id}) has ended.")
        if not self.future_result.done():
            result = FlowExecutionResult(
                flow_id=self.flow.id,
                status="completed",
                executions=self.scheduler.history
            )
            self.future_result.set_result(result)

    def execute_flow(self):
        """Executes the tasks defined in the flow, dynamically instantiating them and handling conditions."""
        print(f"Starting execution for flow: {self.flow.name} (ID: {self.flow.id})")

        start_task = self.flow.start_task
        self.scheduler.schedule(self.process_map[start_task])
