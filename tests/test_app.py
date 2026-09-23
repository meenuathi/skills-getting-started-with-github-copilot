from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_rejects_duplicate_email():
    activity_name = "Chess Club"
    email = "duplicate.student@mergington.edu"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first.status_code == 200

    second = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second.status_code == 400
    assert second.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Tennis Club"
    email = "remove.me@mergington.edu"

    signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup.status_code == 200

    unregister = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert unregister.status_code == 200
    assert unregister.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities")
    assert email not in activities.json()[activity_name]["participants"]
