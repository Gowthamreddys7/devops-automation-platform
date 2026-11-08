
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


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Learn Jenkins CI/CD"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "Learn Jenkins CI/CD"


def test_get_tasks(client):
    client.post("/tasks", json={"title": "Learn Docker"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json) == 1


def test_update_task(client):
    client.post("/tasks", json={"title": "Learn AWS"})

    response = client.put(
        "/tasks/1",
        json={"completed": True}
    )

    assert response.status_code == 200
    assert response.json["completed"] is True


def test_delete_task(client):
    client.post("/tasks", json={"title": "Learn Kubernetes"})

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"


def test_create_task_without_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 400
