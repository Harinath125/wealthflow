def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "pytest_user_001@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test User"
    assert data["email"] == "pytest_user_001@example.com"
    assert data["role"] == "advisor"


def test_register_duplicate_email(client):
    user_data = {
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "StrongPass123"
    }

    first_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert second_response.status_code == 409

    data = second_response.json()

    # AuthService still uses FastAPI HTTPException.
    assert data["error"]["message"] == (
    "Email already registered"
)


def test_login_success(client):
    user_data = {
        "name": "Login User",
        "email": "login@example.com",
        "password": "StrongPass123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_wrong_password(client):
    user_data = {
        "name": "Wrong Password User",
        "email": "wrongpassword@example.com",
        "password": "StrongPass123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": "WrongPassword123"
        }
    )

    assert login_response.status_code == 401

    data = login_response.json()

    # AuthService still uses FastAPI HTTPException.
    assert data["error"]["message"] == (
    "Invalid email or password"
)


def test_protected_endpoint_without_token(client):
    response = client.post(
        "/clients",
        json={
            "name": "Unauthorized Client",
            "email": "unauthorized@example.com",
            "phone": "9000000000"
        }
    )

    assert response.status_code == 401

    data = response.json()

    # HTTPBearer still uses FastAPI's default error format.
    assert data["detail"] == "Not authenticated"


def test_authenticated_client_creation(client):
    user_data = {
        "name": "Authenticated User",
        "email": "authenticated@example.com",
        "password": "StrongPass123"
    }

    register_response = client.post(
        "/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Authenticated Client",
            "email": "client@example.com",
            "phone": "9000000000"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Authenticated Client"
    assert data["email"] == "client@example.com"


def test_user_cannot_access_another_users_client(client):
    # Create User A
    user_a = {
        "name": "Advisor A",
        "email": "advisor_a@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_a
    )

    assert response.status_code == 201

    # Login User A
    response = client.post(
        "/auth/login",
        json={
            "email": user_a["email"],
            "password": user_a["password"]
        }
    )

    assert response.status_code == 200

    token_a = response.json()["access_token"]

    # User A creates a client
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "name": "Client A",
            "email": "client_a@example.com",
            "phone": "9000000001"
        }
    )

    assert response.status_code == 200

    client_a_id = response.json()["id"]

    # Create User B
    user_b = {
        "name": "Advisor B",
        "email": "advisor_b@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_b
    )

    assert response.status_code == 201

    # Login User B
    response = client.post(
        "/auth/login",
        json={
            "email": user_b["email"],
            "password": user_b["password"]
        }
    )

    assert response.status_code == 200

    token_b = response.json()["access_token"]

    # User B requests all clients
    response = client.get(
        "/clients",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 200

    clients = response.json()

    # User B must not see User A's client
    assert all(
        client_data["id"] != client_a_id
        for client_data in clients
    )


def test_user_cannot_access_another_users_portfolio(client):
    # -------------------------
    # Create User A
    # -------------------------
    user_a = {
        "name": "Portfolio Advisor A",
        "email": "portfolio_a@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_a
    )

    assert response.status_code == 201

    # Login User A
    response = client.post(
        "/auth/login",
        json={
            "email": user_a["email"],
            "password": user_a["password"]
        }
    )

    assert response.status_code == 200

    token_a = response.json()["access_token"]

    # -------------------------
    # User A creates a client
    # -------------------------
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "name": "Portfolio Client A",
            "email": "portfolio_client_a@example.com",
            "phone": "9000000001"
        }
    )

    assert response.status_code == 200

    client_a_id = response.json()["id"]

    # -------------------------
    # User A creates a portfolio
    # -------------------------
    response = client.post(
        "/portfolios",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "client_id": client_a_id,
            "name": "Private Portfolio A"
        }
    )

    assert response.status_code == 200

    portfolio_a_id = response.json()["id"]

    # -------------------------
    # Create User B
    # -------------------------
    user_b = {
        "name": "Portfolio Advisor B",
        "email": "portfolio_b@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_b
    )

    assert response.status_code == 201

    # Login User B
    response = client.post(
        "/auth/login",
        json={
            "email": user_b["email"],
            "password": user_b["password"]
        }
    )

    assert response.status_code == 200

    token_b = response.json()["access_token"]

    # -------------------------
    # User B tries to access
    # User A's portfolio
    # -------------------------
    response = client.get(
        f"/portfolios/{portfolio_a_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 403

    data = response.json()

    # PortfolioService now uses AppException.
    assert data["error"]["message"] == (
        "You do not have access to this portfolio"
    )


def test_user_cannot_create_transaction_for_another_users_portfolio(client):
    # -------------------------
    # Create User A
    # -------------------------
    user_a = {
        "name": "Transaction Advisor A",
        "email": "transaction_a@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_a
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": user_a["email"],
            "password": user_a["password"]
        }
    )

    assert response.status_code == 200

    token_a = response.json()["access_token"]

    # -------------------------
    # User A creates client
    # -------------------------
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "name": "Transaction Client A",
            "email": "transaction_client_a@example.com",
            "phone": "9000000001"
        }
    )

    assert response.status_code == 200

    client_a_id = response.json()["id"]

    # -------------------------
    # User A creates portfolio
    # -------------------------
    response = client.post(
        "/portfolios",
        headers={
            "Authorization": f"Bearer {token_a}"
        },
        json={
            "client_id": client_a_id,
            "name": "Transaction Portfolio A"
        }
    )

    assert response.status_code == 200

    portfolio_a_id = response.json()["id"]

    # -------------------------
    # Create User B
    # -------------------------
    user_b = {
        "name": "Transaction Advisor B",
        "email": "transaction_b@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_b
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": user_b["email"],
            "password": user_b["password"]
        }
    )

    assert response.status_code == 200

    token_b = response.json()["access_token"]

    # -------------------------
    # User B tries to create
    # transaction in User A's portfolio
    # -------------------------
    response = client.post(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
        json={
            "portfolio_id": portfolio_a_id,
            "asset_symbol": "RELIANCE",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 2800
        }
    )

    assert response.status_code == 403

    data = response.json()

    # TransactionService still uses HTTPException.
    assert data["error"]["message"] == (
    "You do not have access to this portfolio"
)


def test_user_can_create_transaction_for_own_portfolio(client):
    user = {
        "name": "Transaction Owner",
        "email": "transaction_owner@example.com",
        "password": "StrongPass123"
    }

    # Register
    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    # Create client
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Transaction Owner Client",
            "email": "transaction_owner_client@example.com",
            "phone": "9000000002"
        }
    )

    assert response.status_code == 200

    client_id = response.json()["id"]

    # Create portfolio
    response = client.post(
        "/portfolios",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "client_id": client_id,
            "name": "Transaction Owner Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Create transaction
    response = client.post(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 1500
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["portfolio_id"] == portfolio_id
    assert data["asset_symbol"] == "INFY"
    assert data["transaction_type"] == "BUY"


def test_user_can_get_own_transaction(client):
    user = {
        "name": "Transaction Reader",
        "email": "transaction_reader@example.com",
        "password": "StrongPass123"
    }

    # Register
    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create client
    response = client.post(
        "/clients",
        headers=headers,
        json={
            "name": "Transaction Reader Client",
            "email": "transaction_reader_client@example.com",
            "phone": "9000000003"
        }
    )

    assert response.status_code == 200

    client_id = response.json()["id"]

    # Create portfolio
    response = client.post(
        "/portfolios",
        headers=headers,
        json={
            "client_id": client_id,
            "name": "Transaction Reader Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Create transaction
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "TCS",
            "transaction_type": "BUY",
            "quantity": 5,
            "price": 3500
        }
    )

    assert response.status_code == 200

    transaction_id = response.json()["id"]

    # Retrieve transaction
    response = client.get(
        f"/transactions/{transaction_id}",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == transaction_id
    assert data["portfolio_id"] == portfolio_id
    assert data["asset_symbol"] == "TCS"
    assert data["transaction_type"] == "BUY"


def test_user_cannot_get_another_users_transaction(client):
    # -------------------------
    # User A
    # -------------------------
    user_a = {
        "name": "Transaction Reader A",
        "email": "transaction_reader_a@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_a
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": user_a["email"],
            "password": user_a["password"]
        }
    )

    assert response.status_code == 200

    token_a = response.json()["access_token"]

    headers_a = {
        "Authorization": f"Bearer {token_a}"
    }

    # User A creates client
    response = client.post(
        "/clients",
        headers=headers_a,
        json={
            "name": "Private Transaction Client",
            "email": "private_transaction_client@example.com",
            "phone": "9000000004"
        }
    )

    assert response.status_code == 200

    client_id = response.json()["id"]

    # User A creates portfolio
    response = client.post(
        "/portfolios",
        headers=headers_a,
        json={
            "client_id": client_id,
            "name": "Private Transaction Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # User A creates transaction
    response = client.post(
        "/transactions",
        headers=headers_a,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "HDFC",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 1600
        }
    )

    assert response.status_code == 200

    transaction_id = response.json()["id"]

    # -------------------------
    # User B
    # -------------------------
    user_b = {
        "name": "Transaction Reader B",
        "email": "transaction_reader_b@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user_b
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": user_b["email"],
            "password": user_b["password"]
        }
    )

    assert response.status_code == 200

    token_b = response.json()["access_token"]

    # User B tries to retrieve User A's transaction
    response = client.get(
        f"/transactions/{transaction_id}",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 403

    data = response.json()

    # TransactionService still uses HTTPException.
    assert data["error"]["message"] == (
    "You do not have access to this transaction"
)


def test_get_nonexistent_transaction(client):
    user = {
        "name": "Missing Transaction User",
        "email": "missing_transaction@example.com",
        "password": "StrongPass123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get(
        "/transactions/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    # TransactionService still uses HTTPException.
    assert data["error"]["message"] == "Transaction not found"