class AppException(Exception):
    """
    Base exception for application-level errors.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500
    ):
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class ResourceNotFoundException(AppException):
    """
    Raised when a requested resource does not exist.
    """

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=404
        )


class ForbiddenException(AppException):
    """
    Raised when a user is not allowed to access a resource.
    """

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=403
        )


class ConflictException(AppException):
    """
    Raised when a request conflicts with existing data.
    """

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=409
        )

class UnauthorizedException(AppException):
    """
    Raised when authentication credentials are invalid
    or the user is not authenticated.
    """

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=401
        )