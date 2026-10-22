def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Validation User",
            "email": "short_password@example.com",
            "password": "short"
        }
    )

    assert response.status_code == 422


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Validation User",
            "email": "not-an-email",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 422


def test_register_short_name(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "A",
            "email": "short_name@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 422


def test_create_client_invalid_email(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Client Test User",
            "email": "client_validation_user@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "client_validation_user@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    # Invalid client email
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Invalid Email Client",
            "email": "invalid-email",
            "phone": "9000000000"
        }
    )

    assert response.status_code == 422


def test_create_transaction_negative_quantity(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Quantity Test User",
            "email": "quantity_validation@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "quantity_validation@example.com",
            "password": "StrongPass123"
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
            "name": "Quantity Client",
            "email": "quantity_client@example.com",
            "phone": "9000000001"
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
            "name": "Quantity Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Negative quantity
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": -10,
            "price": 1500
        }
    )

    assert response.status_code == 422


def test_create_transaction_zero_quantity(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Zero Quantity User",
            "email": "zero_quantity@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "zero_quantity@example.com",
            "password": "StrongPass123"
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
            "name": "Zero Quantity Client",
            "email": "zero_quantity_client@example.com",
            "phone": "9000000002"
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
            "name": "Zero Quantity Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Zero quantity
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 0,
            "price": 1500
        }
    )

    assert response.status_code == 422


def test_create_transaction_negative_price(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Price Test User",
            "email": "price_validation@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "price_validation@example.com",
            "password": "StrongPass123"
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
            "name": "Price Client",
            "email": "price_client@example.com",
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
            "name": "Price Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Negative price
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": -1500
        }
    )

    assert response.status_code == 422


def test_create_transaction_zero_price(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Zero Price User",
            "email": "zero_price@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "zero_price@example.com",
            "password": "StrongPass123"
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
            "name": "Zero Price Client",
            "email": "zero_price_client@example.com",
            "phone": "9000000004"
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
            "name": "Zero Price Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Zero price
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 0
        }
    )

    assert response.status_code == 422


def test_create_transaction_invalid_transaction_type(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Transaction Type User",
            "email": "transaction_type@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "transaction_type@example.com",
            "password": "StrongPass123"
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
            "name": "Transaction Type Client",
            "email": "transaction_type_client@example.com",
            "phone": "9000000005"
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
            "name": "Transaction Type Portfolio"
        }
    )

    assert response.status_code == 200

    portfolio_id = response.json()["id"]

    # Invalid transaction type
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "INVALID",
            "quantity": 10,
            "price": 1500
        }
    )

    assert response.status_code == 422


def test_create_portfolio_for_nonexistent_client(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Missing Client User",
            "email": "missing_client@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "missing_client@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    # Nonexistent client
    response = client.post(
        "/portfolios",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "client_id": 999999,
            "name": "Invalid Portfolio"
        }
    )

    assert response.status_code == 404

    data = response.json()

    # PortfolioService uses AppException.
    assert data["error"]["message"] == "Client not found"


def test_create_transaction_for_nonexistent_portfolio(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Missing Portfolio User",
            "email": "missing_portfolio@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "missing_portfolio@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    # Nonexistent portfolio
    response = client.post(
        "/transactions",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "portfolio_id": 999999,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 1500
        }
    )

    assert response.status_code == 404

    data = response.json()

    # TransactionService still uses HTTPException.
    assert data["error"]["message"] == "Portfolio not found"


def test_get_nonexistent_portfolio(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "name": "Missing Portfolio Reader",
            "email": "missing_portfolio_reader@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "missing_portfolio_reader@example.com",
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    response = client.get(
        "/portfolios/999999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    # PortfolioService uses AppException.
    assert data["error"]["message"] == "Portfolio not found"