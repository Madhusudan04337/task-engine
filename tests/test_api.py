import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_registration_workflow(client: AsyncClient):
    """
    Test 1: Successful registration and subsequent login.
    """
    # 1. Register
    reg_data = {
        "email": "tester@example.com",
        "password": "testpassword",
        "role": "user"
    }
    response = await client.post("/api/v1/auth/register", json=reg_data)
    assert response.status_code == 201
    assert response.json()["email"] == reg_data["email"]

    # 2. Login
    login_data = {
        "username": reg_data["email"],
        "password": reg_data["password"]
    }
    login_res = await client.post("/api/v1/auth/login", data=login_data)
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()


@pytest.mark.asyncio
async def test_token_security_failures(client: AsyncClient):
    """
    Test 2: Accessing protected routes without valid credentials.
    """
    # No token
    res_no_token = await client.get("/api/v1/tasks/")
    assert res_no_token.status_code == 401
    assert res_no_token.json()["detail"] == "Not authenticated"

    # Invalid token
    res_bad_token = await client.get(
        "/api/v1/tasks/", 
        headers={"Authorization": "Bearer invalid_token_string"}
    )
    assert res_bad_token.status_code == 401
    assert "credentials" in res_bad_token.json()["detail"].lower()


@pytest.mark.asyncio
async def test_data_isolation_cross_tenant(client: AsyncClient):
    """
    Test 3: Ensure User A cannot see or modify User B's tasks.
    """
    # 1. Create User A and User B
    users = []
    for i in range(2):
        email = f"user{i}@example.com"
        await client.post("/api/v1/auth/register", json={
            "email": email, "password": "password", "role": "user"
        })
        login_res = await client.post("/api/v1/auth/login", data={
            "username": email, "password": "password"
        })
        users.append(login_res.json()["access_token"])
    
    token_a, token_b = users

    # 2. User A creates a task
    task_res = await client.post(
        "/api/v1/tasks/",
        json={"title": "Private Task A", "description": "Owner is User A"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    task_id = task_res.json()["id"]

    # 3. User B tries to fetch User A's task
    get_res = await client.get(
        f"/api/v1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert get_res.status_code == 403
    assert "permissions" in get_res.json()["detail"].lower()

    # 4. User B tries to list tasks and should NOT see User A's task
    list_res = await client.get(
        "/api/v1/tasks/",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert list_res.status_code == 200
    assert len(list_res.json()) == 0
