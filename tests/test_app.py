
import pytest
import app as task_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give each test its own temporary database.
    test_database = tmp_path / "test_tasks.db"
    monkeypatch.setattr(task_app, "DATABASE", str(test_database))

    task_app.init_db()

    with task_app.app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "My Task Management API is running!"
    }


def test_get_empty_tasks(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn pytest",
            "description": "Write automated tests"
        }
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "Learn pytest"
    assert data["description"] == "Write automated tests"
    assert data["status"] == "pending"
    assert "id" in data


def test_get_task_by_id(client):
    created = client.post(
        "/tasks",
        json={"title": "Learn Flask"}
    )

    task_id = created.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Learn Flask"


def test_update_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Original title"}
    )

    task_id = created.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "completed"}
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "completed"


def test_delete_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Delete me"}
    )

    task_id = created.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    missing = client.get(f"/tasks/{task_id}")
    assert missing.status_code == 404

def test_create_task_without_title(client):
    response = client.post(
        "/tasks",
        json={"description": "This task has no title"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "A non-empty title is required"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Task not found"


def test_update_task_with_invalid_status(client):
    created = client.post(
        "/tasks",
        json={"title": "Test task"}
    )

    task_id = created.get_json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "invalid_status"}
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid status"
