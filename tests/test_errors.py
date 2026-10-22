from fastapi import APIRouter

from main import app


error_router = APIRouter()


@error_router.get("/test-unexpected-error")
def trigger_unexpected_error():
    raise RuntimeError("This is a test failure")


app.include_router(error_router)


def test_unexpected_exception_returns_safe_response(client):
    response = client.get(
        "/test-unexpected-error"
    )

    assert response.status_code == 500

    data = response.json()

    assert data["error"]["message"] == (
        "Internal server error"
    )