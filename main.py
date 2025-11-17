import os
import json

from fastapi import FastAPI
from helpers.models import Flow
from services.flow import Flow as FlowService

app = FastAPI(
    title="Flow Manager API",
    description="API for managing flows",
    version="1.0.0",
    contact={
        "name": "Akash",
        "email": "akash@example.com",
    },
)

flows: list[Flow] = []

@app.post("/flows/")
async def create_flow(flow: Flow):

    flow_data = flow.model_dump()
    file_path = f"flows/{flow_data['id']}.json"
    with open(file_path, 'w') as f:
        json.dump(flow_data, f, indent=4)
    flows.append(Flow.model_validate(flow_data))
    return flow_data

@app.get("/flows/")
async def read_flows():
    return flows

@app.get("/flows/{flow_id}")
async def read_flow(flow_id: str):
    for flow in flows:
        if flow.id == flow_id:
            return flow
    return {"message": "Flow not found"}

@app.get("/flows/{flow_id}/execute")
async def execute_flow(flow_id: str):
    for flow in flows:
        if flow.id == flow_id:
            flow_service = FlowService(flow)
            flow_service.execute()
            return {"message": "Flow executed successfully"}
    return {"message": "Flow not found"}
