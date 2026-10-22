from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse
)
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse
)
from app.schemas.auth import (
    RegisterRequest,
    UserResponse
)
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioSummaryResponse
)

from app.exceptions.exceptions import AppException
from app.exceptions.handlers import (
    app_exception_handler,
    unexpected_exception_handler
)

from app.services.auth_service import AuthService
from app.services.transaction_service import TransactionService
from app.services.portfolio_service import PortfolioService
from app.database.database import get_db
from app.schemas.client import ClientCreate, ClientResponse
from app.services.client_service import ClientService


from app.core.dependencies import get_current_user
from app.models.user import User

from app.exceptions.exceptions import (
    AppException,
    ResourceNotFoundException
)
from app.core.logging_config import configure_logging
from app.middleware.request_id import request_id_middleware

app = FastAPI(title="WealthFlow API")

configure_logging()
app.middleware("http")(request_id_middleware)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler
)
app.add_exception_handler(
    AppException,
    app_exception_handler
)

client_service = ClientService()


@app.get("/")
def home():
    return {"message": "Welcome to WealthFlow"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "wealthflow"
    }




@app.get(
    "/clients",
    response_model=list[ClientResponse]
)
def get_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return client_service.get_clients(
        db,
        current_user.id
    )


@app.post("/clients", response_model=ClientResponse)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return client_service.create_client(
        db,
        client,
        current_user
    )
#----------------------------------------------------------------
#               portfolio-services
#----------------------------------------------------------------
portfolio_service = PortfolioService()
@app.post(
    "/portfolios",
    response_model=PortfolioResponse
)
def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return portfolio_service.create_portfolio(
        db,
        portfolio,
        current_user
    )


@app.get(
    "/portfolios/{portfolio_id}",
    response_model=PortfolioResponse
)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return portfolio_service.get_portfolio(
        db,
        portfolio_id,
        current_user
    )

transaction_service = TransactionService()

@app.post(
    "/transactions",
    response_model=TransactionResponse
)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return transaction_service.create_transaction(
        db,
        transaction,
        current_user
    )


@app.get(
    "/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return transaction_service.get_transaction(
        db,
        transaction_id,
        current_user
    )

auth_service = AuthService()

@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: RegisterRequest,
    db: Session = Depends(get_db)
):
    return auth_service.register(
        db,
        user
    )


@app.post(
    "/auth/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return auth_service.login(
        db,
        login_data
    )


@app.get(
    "/portfolios/{portfolio_id}/summary",
    response_model=PortfolioSummaryResponse
)
def get_portfolio_summary(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return portfolio_service.get_summary(
        db,
        portfolio_id,
        current_user
    )