def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_register_duplicate_email(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    response = client.post("/api/auth/register", json={
        "username": "testuser2",
        "email": "test@test.com",
        "password": "123456"
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123456"
    })
    response = client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "senhaerrada"
    })
    assert response.status_code == 401

def test_me_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401