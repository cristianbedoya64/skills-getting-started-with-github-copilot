import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data

def test_signup_and_unregister():
    activity = "Tennis Club"
    email = "testuser@example.com"
    # Signup
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200
    assert f"Signed up {email}" in signup.json()["message"]
    # Duplicate signup
    duplicate = client.post(f"/activities/{activity}/signup?email={email}")
    assert duplicate.status_code == 400
    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister.status_code == 200
    assert f"Removed {email}" in unregister.json()["message"]
    # Unregister again
    unregister_again = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_again.status_code == 400
