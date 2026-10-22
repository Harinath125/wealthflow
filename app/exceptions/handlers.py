import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import AppException


logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message
            }
        }
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception: method=%s path=%s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error"
            }
        }
    )