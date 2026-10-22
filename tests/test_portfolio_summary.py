from decimal import Decimal


def create_authenticated_user(client, name, email):
    response = client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "StrongPass123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_client(client, token, name, email):
    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": name,
            "email": email,
            "phone": "9000000000"
        }
    )

    assert response.status_code == 200

    return response.json()["id"]


def create_portfolio(client, token, client_id, name):
    response = client.post(
        "/portfolios",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "client_id": client_id,
            "name": name
        }
    )

    assert response.status_code == 200

    return response.json()["id"]


def test_portfolio_summary(client):

    token = create_authenticated_user(
        client,
        "Summary User",
        "summary@example.com"
    )

    client_id = create_client(
        client,
        token,
        "Summary Client",
        "summary_client@example.com"
    )

    portfolio_id = create_portfolio(
        client,
        token,
        client_id,
        "Summary Portfolio"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # BUY 10 INFY @ 1500
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 1500
        }
    )

    assert response.status_code == 200

    # BUY 5 TCS @ 3500
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

    # Get summary
    response = client.get(
        f"/portfolios/{portfolio_id}/summary",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    # 10 * 1500 = 15000
    # 5 * 3500 = 17500
    # Total = 32500
    assert data["portfolio_id"] == portfolio_id

    assert (
        Decimal(data["total_invested"])
        == Decimal("32500.00")
    )

    holdings = {
        item["asset_symbol"]: item
        for item in data["holdings"]
    }

    assert (
        Decimal(holdings["INFY"]["quantity"])
        == Decimal("10")
    )

    assert (
        Decimal(holdings["INFY"]["invested_amount"])
        == Decimal("15000.00")
    )

    assert (
        Decimal(holdings["TCS"]["quantity"])
        == Decimal("5")
    )

    assert (
        Decimal(holdings["TCS"]["invested_amount"])
        == Decimal("17500.00")
    )


def test_portfolio_summary_with_sell(client):

    token = create_authenticated_user(
        client,
        "Sell User",
        "sell_summary@example.com"
    )

    client_id = create_client(
        client,
        token,
        "Sell Client",
        "sell_client@example.com"
    )

    portfolio_id = create_portfolio(
        client,
        token,
        client_id,
        "Sell Portfolio"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # BUY 10 INFY @ 1500
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "BUY",
            "quantity": 10,
            "price": 1500
        }
    )

    assert response.status_code == 200

    # SELL 3 INFY @ 1600
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "portfolio_id": portfolio_id,
            "asset_symbol": "INFY",
            "transaction_type": "SELL",
            "quantity": 3,
            "price": 1600
        }
    )

    assert response.status_code == 200

    # Get summary
    response = client.get(
        f"/portfolios/{portfolio_id}/summary",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    # BUY value  = 10 * 1500 = 15000
    # SELL value =  3 * 1600 =  4800
    # Net        = 15000 - 4800 = 10200
    assert (
        Decimal(data["total_invested"])
        == Decimal("10200.00")
    )

    holdings = data["holdings"]

    assert len(holdings) == 1

    assert holdings[0]["asset_symbol"] == "INFY"

    assert (
        Decimal(holdings[0]["quantity"])
        == Decimal("7")
    )

    assert (
        Decimal(holdings[0]["invested_amount"])
        == Decimal("10200.00")
    )


def test_portfolio_summary_requires_authentication(client):

    response = client.get(
        "/portfolios/1/summary"
    )

    assert response.status_code == 401


def test_portfolio_summary_nonexistent_portfolio(client):

    token = create_authenticated_user(
        client,
        "Missing Summary User",
        "missing_summary@example.com"
    )

    response = client.get(
        "/portfolios/999999/summary",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["error"]["message"] == "Portfolio not found"

def test_portfolio_summary_other_users_portfolio(client):

    # User A
    token_a = create_authenticated_user(
        client,
        "Summary Advisor A",
        "summary_advisor_a@example.com"
    )

    client_a_id = create_client(
        client,
        token_a,
        "Summary Client A",
        "summary_client_a@example.com"
    )

    portfolio_a_id = create_portfolio(
        client,
        token_a,
        client_a_id,
        "Private Summary Portfolio"
    )

    # User B
    token_b = create_authenticated_user(
        client,
        "Summary Advisor B",
        "summary_advisor_b@example.com"
    )

    # User B tries to access User A's portfolio
    response = client.get(
        f"/portfolios/{portfolio_a_id}/summary",
        headers={
            "Authorization": f"Bearer {token_b}"
        }
    )

    assert response.status_code == 403

    data = response.json()

    assert data["error"]["message"] == (
    "You do not have access to this portfolio"
    )