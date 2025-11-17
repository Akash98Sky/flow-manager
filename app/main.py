import os
import json

from .models.flow import Flow, FlowData
from .services.flow import FlowProcessor
from . import app

flows: list[FlowData] = []

def load_flows_at_startup():
    """Loads all flows from the 'flows' directory at startup."""
    flows_dir = "flows"
    if not os.path.exists(flows_dir):
        os.makedirs(flows_dir) # Ensure directory exists if it doesn't
        return

    for filename in os.listdir(flows_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(flows_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    flow_data = FlowData.model_validate_json(f.read())
                    flows.append(flow_data)
                    print(f"Loaded flow: {flow_data.flow.id} from {filename}") # Optional: for debugging
            except json.JSONDecodeError:
                print(f"Error decoding JSON from {filename}")
            except Exception as e:
                print(f"Error loading flow from {filename}: {e}")

# Load flows when the application starts
load_flows_at_startup()

@app.post("/flows/")
async def create_flow(flow_data: FlowData):
    file_path = f"flows/{flow_data.flow.id}.json"
    with open(file_path, 'w') as f:
        f.write(flow_data.model_dump_json(indent=4))
    flows.append(flow_data)
    return flow_data

@app.get("/flows/")
async def read_flows():
    return flows

@app.get("/flows/{flow_id}")
async def read_flow(flow_id: str):
    for flow_data in flows:
        if flow_data.flow.id == flow_id:
            return flow_data
    return {"message": "Flow not found"}

@app.get("/flows/{flow_id}/execute")
async def execute_flow(flow_id: str):
    for flow_data in flows:
        if flow_data.flow.id == flow_id:
            processor = FlowProcessor(flow_data.flow)
            processor.execute_flow()
            result = await processor.future_result
            return {
                "message": f"Flow {flow_id} executed successfully",
                "result": result
            }
    return {"message": "Flow not found"}
