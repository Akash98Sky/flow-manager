import asyncio
import time

from typing import Callable

from ..models.flow import Execution, Task

class Process:
    task: Task
    start_perf: float | None
    end_perf: float | None

    def __init__(self, task: Task):
        self.task = task
        self.start_perf = None
        self.end_perf = None

    def duration(self) -> float:
        print(self.start_perf, self.end_perf)
        return self.end_perf - self.start_perf if self.end_perf and self.start_perf else 0.0

    async def execute(self):
        try:
            self.start_perf = time.perf_counter()
            print(f"Executing task: {self.task.name}")
            # simulate some processing delay
            await asyncio.sleep(1)
            print(f"Executed task: {self.task.name}")
            # Simulate task execution success (true)
            return True
        except Exception as e:
            print(f"Error executing task {self.task.name}: {e}")
            # Simulate task execution failure (false)
            return False
        finally:
            self.end_perf = time.perf_counter()

class Scheduler:
    history: list[Execution]
    on_failure: Callable[[Task], None]
    on_success: Callable[[Task], None]
    on_end: Callable[[], None]

    def __init__(self, on_success: Callable[[Task], None], on_failure: Callable[[Task], None], on_end: Callable[[], None]):
        self.on_success = on_success
        self.on_failure = on_failure
        self.on_end = on_end
        self.history = []

    def __task_done(self, task: Task, success: bool, duration: float = 0.0):
        self.history.append(
            Execution(
                **task.model_dump(),
                success=success,
                duration=duration
            )
        )
        if success:
            self.on_success(task)
        else:
            self.on_failure(task)

    def schedule(self, process: Process):
        if process.task.name == "end":
            self.on_end()
        else:
            asyncio.create_task(process.execute()).add_done_callback(
                lambda success: self.__task_done(process.task, success.result(), process.duration())
            )
