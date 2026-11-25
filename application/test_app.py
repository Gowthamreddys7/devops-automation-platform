
import pytest
import app as app_module


@pytest.fixture
def client():
    app_module.app.config["TESTING"] = True

    # Reset application data before each test
    app_module.tasks.clear()
    app_module.task_id_counter = 1

    with app_module.app.test_client() as client:
        yield client


# 1. Test homepage
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert response.json["application"] == "DevOps Automation Platform"


# 2. Test health endpoint
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


# 3. Test creating a task
def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Learn Jenkins CI/CD"}
    )

    assert response.status_code == 201
    assert response.json["id"] == 1
    assert response.json["title"] == "Learn Jenkins CI/CD"
    assert response.json["completed"] is False


# 4. Test retrieving all tasks
def test_get_tasks(client):
    client.post("/tasks", json={"title": "Learn Docker"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == "Learn Docker"


# 5. Test updating task completion
def test_update_task(client):
    client.post("/tasks", json={"title": "Learn AWS"})

    response = client.put(
        "/tasks/1",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json["completed"] is True


# 6. Test deleting a task
def test_delete_task(client):
    client.post("/tasks", json={"title": "Learn Kubernetes"})

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

    # Verify task was deleted
    get_response = client.get("/tasks")
    assert len(get_response.json) == 0


# 7. Test creating a task without title
def test_create_task_without_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.json["error"] == "Valid task title is required"


# 8. Test creating a task with empty title
def test_create_task_with_empty_title(client):
    response = client.post(
        "/tasks",
        json={"title": "   "}
    )

    assert response.status_code == 400


# 9. Test updating a nonexistent task
def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/999",
        json={"completed": True}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Task not found"


# 10. Test deleting a nonexistent task
def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json["error"] == "Task not found"


# 11. Test updating task title
def test_update_task_title(client):
    client.post("/tasks", json={"title": "Learn Docker"})

    response = client.put(
        "/tasks/1",
        json={"title": "Learn Kubernetes"}
    )

    assert response.status_code == 200
    assert response.json["title"] == "Learn Kubernetes"


# 12. Test updating task with invalid completed value
def test_update_task_invalid_completed_value(client):
    client.post("/tasks", json={"title": "Learn AWS"})

    response = client.put(
        "/tasks/1",
        json={"completed": "yes"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "completed must be a boolean"

