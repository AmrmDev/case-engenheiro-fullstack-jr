def register_and_login(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "123456"
    })
    return response.json()["access_token"]

def test_start_game(client):
    token = register_and_login(client)
    response = client.post("/api/games/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert "id" in response.json()

def test_submit_attempt(client):
    token = register_and_login(client)
    game = client.post("/api/games/", headers={"Authorization": f"Bearer {token}"}).json()
    response = client.post(
        f"/api/games/{game['id']}/attempts",
        json={"guess": ["A", "B", "C", "D"]},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "exact_hits" in response.json()

def test_ranking(client):
    response = client.get("/api/games/ranking/top")
    assert response.status_code == 200
    assert isinstance(response.json(), list)