from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest
)

from app.exceptions.exceptions import (
    ConflictException,
    UnauthorizedException
)


class AuthService:

    def __init__(self):
        self.repository = UserRepository()

    def register(
        self,
        db: Session,
        user_data: RegisterRequest
    ):
        existing_user = self.repository.get_by_email(
            db,
            user_data.email
        )

        if existing_user is not None:
            raise ConflictException(
                "Email already registered"
            )

        password_hash = hash_password(
            user_data.password
        )

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=password_hash,
            role="advisor"
        )

        return self.repository.create(
            db,
            new_user
        )

    def login(
        self,
        db: Session,
        login_data: LoginRequest
    ):
        user = self.repository.get_by_email(
            db,
            login_data.email
        )

        if user is None:
            raise UnauthorizedException(
                "Invalid email or password"
            )

        password_valid = verify_password(
            login_data.password,
            user.password_hash
        )

        if not password_valid:
            raise UnauthorizedException(
                "Invalid email or password"
            )

        access_token = create_access_token({
            "sub": str(user.id),
            "role": user.role
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }