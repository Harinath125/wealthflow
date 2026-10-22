from contextvars import ContextVar


request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-"
)


def set_request_id(request_id: str):
    """
    Store the request ID for the current execution context.
    """

    return request_id_context.set(request_id)


def get_request_id() -> str:
    """
    Get the request ID for the current execution context.
    """

    return request_id_context.get()


def reset_request_id(token):
    """
    Restore the previous request ID context.
    """

    request_id_context.reset(token)