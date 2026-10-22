from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY
)

from app.database.database import get_db
from app.models.user import User

from app.exceptions.exceptions import (
    ResourceNotFoundException,
    UnauthorizedException
)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedException(
                "Invalid authentication token"
            )

    except JWTError:
        raise UnauthorizedException(
            "Invalid authentication token"
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:
        raise ResourceNotFoundException(
            "User not found"
        )

    return user