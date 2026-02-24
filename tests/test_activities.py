from urllib.parse import quote


def _signup(client, activity, email):
    path = f"/activities/{quote(activity, safe='')}/signup"
    return client.post(path, params={"email": email})


def _unregister(client, activity, email):
    path = f"/activities/{quote(activity, safe='')}/unregister"
    return client.delete(path, params={"email": email})


def test_get_activities_returns_all(client):
    # Arrange / Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    # Arrange
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act
    resp = _signup(client, activity, email)

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_activity_not_found_returns_404(client):
    # Arrange
    activity = "No Such Club"
    email = "x@mergington.edu"

    # Act
    resp = _signup(client, activity, email)

    # Assert
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"


def test_signup_already_signed_up_returns_400(client):
    # Arrange (seed data has michael@mergington.edu in Chess Club)
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    resp = _signup(client, activity, email)

    # Assert
    assert resp.status_code == 400


def test_unregister_success_removes_participant(client):
    # Arrange: sign up then remove
    activity = "Tennis Club"
    email = "alice@mergington.edu"
    r1 = _signup(client, activity, email)
    assert r1.status_code == 200

    # Act
    r2 = _unregister(client, activity, email)

    # Assert
    assert r2.status_code == 200
    assert r2.json() == {"message": f"Unregistered {email} from {activity}"}
    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_unregister_not_signed_up_returns_404(client):
    # Arrange
    activity = "Drama Club"
    email = "nobody@mergington.edu"

    # Act
    r = _unregister(client, activity, email)

    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == f"Student {email} is not signed up for {activity}"
