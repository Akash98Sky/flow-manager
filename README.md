# Flow Manager

This project implements a flow manager that allows defining and executing complex workflows. Flows are composed of tasks, and their execution is controlled by conditions that dictate the sequence based on task success or failure.

## Flow Design Explanation

The flow manager orchestrates a series of tasks, enabling sophisticated workflow automation.

### Task Dependencies

Tasks are linked together through a defined set of `conditions`. Each `condition` specifies:
- A `source_task`: The task whose completion triggers the evaluation of this condition.
- An `outcome`: The result of the `source_task` (e.g., 'success', 'failure').
- A `target_task_success`: The next task to execute if the `source_task` succeeds and the `outcome` matches.
- A `target_task_failure`: The next task to execute if the `source_task` fails and the `outcome` matches.

The `Flow` object defines the `start_task` and lists all available `tasks` and `conditions`. The `FlowProcessor` uses these definitions to determine the execution path. If a task completes and no matching condition is found for its outcome, the flow is considered ended.

### Task Success/Failure Evaluation

1.  **Individual Task Execution**: The `Process` class (within `app/services/task.py`) is responsible for executing a single task. Currently, task execution is simulated with a delay, and the `Process.execute()` method is designed to return a boolean indicating success (`True`) or failure (`False`). The actual logic for determining the success or failure of a task's operation would be implemented within this method.
2.  **Flow Progression Evaluation**: The `FlowProcessor` (within `app/services/flow.py`) evaluates the flow's progression. After a task completes, the `FlowProcessor` iterates through the defined `conditions` in the `Flow` object. It checks if any `condition`'s `source_task` matches the completed task and if the `outcome` specified in the `condition` aligns with the actual result of the task (success or failure).

### Task Outcome Handling

-   **Task Success**: If a task succeeds, the `FlowProcessor` looks for a `condition` where the `source_task` matches the completed task and the `outcome` is 'success'. If found, the `target_task_success` is scheduled for execution. If no such condition is found, the flow is terminated.
-   **Task Failure**: If a task fails, the `FlowProcessor` looks for a `condition` where the `source_task` matches the completed task and the `outcome` is 'failure'. If found, the `target_task_failure` is scheduled for execution. If no such condition is found, the flow is terminated.
-   **Flow Termination**: A flow can end in several ways:
    -   When a task named "end" is executed.
    -   When a task completes, and no matching `condition` is found for its outcome (success or failure).
    -   When the `FlowProcessor` explicitly calls `__end_flow()`.
    Upon termination, the `FlowExecutionResult` is populated with the flow's status and a history of executed tasks.

## Code Implementation

The flow manager is implemented using Python with FastAPI for the API.

### Core Components:

-   **`app/models/flow.py`**: Defines Pydantic models for `Task`, `Condition`, `Flow`, `FlowData`, and `FlowExecutionResult`, structuring the workflow definitions.
-   **`app/services/task.py`**:
    -   `Process`: Encapsulates the logic for executing a single task.
    -   `Scheduler`: Manages the asynchronous execution of tasks and handles callbacks for success, failure, and flow completion.
-   **`app/services/flow.py`**:
    -   `FlowProcessor`: Orchestrates the execution of a `Flow` by managing task scheduling, condition evaluation, and state transitions. It uses the `Scheduler` and `Process` classes.
-   **`app/main.py`**:
    -   The FastAPI application setup.
    -   Loads flow definitions from JSON files in the `flows/` directory on startup.
    -   Provides API endpoints for creating (`/flows/`), retrieving (`/flows/`, `/flows/{flow_id}`), and executing (`/flows/{flow_id}/execute`) flows.

### Example Task Definition (JSON):

Flows are defined in JSON files within the `flows/` directory.

```json
{
    "flow": {
        "id": "my-first-flow",
        "name": "My First Flow",
        "start_task": "task_a",
        "tasks": [
            {
                "name": "task_a",
                "description": "This is the first task."
            },
            {
                "name": "task_b",
                "description": "This is the second task."
            },
            {
                "name": "task_c",
                "description": "This is the third task."
            }
        ],
        "conditions": [
            {
                "name": "condition_a_success",
                "description": "If task_a succeeds, go to task_b",
                "source_task": "task_a",
                "outcome": "success",
                "target_task_success": "task_b",
                "target_task_failure": "task_c"
            },
            {
                "name": "condition_a_failure",
                "description": "If task_a fails, go to task_c",
                "source_task": "task_a",
                "outcome": "failure",
                "target_task_success": "task_b",
                "target_task_failure": "task_c"
            },
            {
                "name": "condition_b_success",
                "description": "If task_b succeeds, go to task_c",
                "source_task": "task_b",
                "outcome": "success",
                "target_task_success": "task_c",
                "target_task_failure": "end"
            },
            {
                "name": "condition_c_success",
                "description": "If task_c succeeds, go to end",
                "source_task": "task_c",
                "outcome": "success",
                "target_task_success": "end",
                "target_task_failure": "end"
            }
        ]
    }
}
