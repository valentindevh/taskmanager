import pytest
from httpx import AsyncClient

from app.schemas.task import TaskInDB

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    task_data = {"title": "Test Task", "description": "Test Description", "priority": 1}
    response = await client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 201
    task = response.json()
    assert task["title"] == task_data["title"]
    assert task["description"] == task_data["description"]
    assert task["priority"] == task_data["priority"]
    assert task["status"] == "pending"

@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):
    # First create a task
    task_data = {"title": "Test Get Task", "description": "Test", "priority": 1}
    create_response = await client.post("/api/v1/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Then get it
    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["id"] == task_id
    assert task["title"] == task_data["title"]

@pytest.mark.asyncio
async def test_get_tasks(client: AsyncClient):
    # Create some tasks first
    for i in range(3):
        await client.post("/api/v1/tasks/", json={"title": f"Task {i}", "priority": 1})

    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) >= 3

