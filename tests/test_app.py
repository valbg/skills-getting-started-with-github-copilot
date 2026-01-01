import os
import sys
from urllib.parse import quote

from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Basic known activity
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "tester@example.com"

    # Ensure clean start: the in-memory DB may persist across test runs in the same process
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email not in data[activity]["participants"]

    # Sign up
    res = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Confirm participant added
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email in data[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Confirm participant removed
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email not in data[activity]["participants"]
