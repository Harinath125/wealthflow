import logging
import uuid

from fastapi import Request

from app.core.request_context import (
    set_request_id,
    reset_request_id
)


logger = logging.getLogger(__name__)


async def request_id_middleware(
    request: Request,
    call_next
):
    request_id = request.headers.get(
        "X-Request-ID"
    )

    if not request_id:
        request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    context_token = set_request_id(
        request_id
    )

    logger.info(
        "Request started: method=%s path=%s",
        request.method,
        request.url.path
    )

    try:
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed: method=%s path=%s "
            "status_code=%s",
            request.method,
            request.url.path,
            response.status_code
        )

        return response

    except Exception:
        logger.exception(
            "Request failed: method=%s path=%s",
            request.method,
            request.url.path
        )

        raise

    finally:
        reset_request_id(context_token)