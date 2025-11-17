from pydantic import BaseModel

class Task(BaseModel):
    name: str
    description: str

class Condition(BaseModel):
    name: str
    description: str
    source_task: str
    outcome: str
    target_task_success: str
    target_task_failure: str

class Flow(BaseModel):
    id: str
    name: str
    start_task: str
    tasks: list[Task]
    conditions: list[Condition]
