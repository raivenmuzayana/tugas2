from fastapi.testclient import TestClient
from main import app
from modules.users import utils

client = TestClient(app)

def setup_function():
    utils.fake_users_db.clear()
    utils.user_id_counter = 1

def test_create_user_success():
    response = client.post(
        "/users/",
        json={"username": "newuser", "email": "newuser@example.com", "password": "Password!123", "role": "staff"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert "password" not in data
    assert len(utils.fake_users_db) == 1

def test_create_user_invalid_password():
    response = client.post(
        "/users/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "weak", "role": "staff"}
    )
    assert response.status_code == 422

def test_read_users_as_admin():
    client.post("/users/", json={"username": "adminuser", "email": "user1@example.com", "password": "Password!123", "role": "staff"})
    response = client.get("/users/", headers={"X-User-Role": "admin"})
    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_read_own_user_data_as_staff():
    client.post("/users/", json={"username": "staffuser", "email": "staff@example.com", "password": "Password!123", "role": "staff"})
    response = client.get("/users/1", headers={"X-User-Role": "staff", "X-User-ID": "1"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_user_as_admin():
    client.post("/users/", json={"username": "todelete", "email": "del@example.com", "password": "Password!123", "role": "staff"})
    assert len(utils.fake_users_db) == 1
    response = client.delete("/users/1", headers={"X-User-Role": "admin"})
    assert response.status_code == 204
    assert len(utils.fake_users_db) == 0

def test_user_not_found():
    response = client.get("/users/999", headers={"X-User-Role": "admin"})
    assert response.status_code == 404