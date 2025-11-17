import asyncio

from typing import Callable

from ..models.flow import Task

class Process:
    task: Task

    def __init__(self, task: Task):
        self.task = task

    async def execute(self):
        print(f"Executing task: {self.task.name}")
        # simulate some processing delay
        await asyncio.sleep(1)
        print(f"Executed task: {self.task.name}")
        # Simulate task execution success
        return True

class Scheduler:
    history: list[Task]
    on_failure: Callable[[Task], None]
    on_success: Callable[[Task], None]
    on_end: Callable[[], None]

    def __init__(self, on_success: Callable[[Task], None], on_failure: Callable[[Task], None], on_end: Callable[[], None]):
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.history = []

    def __task_done(self, task: Task, success: bool):
        if success:
            self.on_success(task)
        else:
            self.on_failure(task)

    def schedule(self, process: Process):
        self.history.append(process.task)
        if process.task.name == "end":
            self.on_end()
        else:
            asyncio.create_task(process.execute()).add_done_callback(
                lambda success: self.__task_done(process.task, success.result())
            )
