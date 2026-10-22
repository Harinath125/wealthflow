import logging
import sys

from app.core.request_context import get_request_id


class RequestIDFilter(logging.Filter):
    """
    Add the current request ID to every log record.
    """

    def filter(
        self,
        record: logging.LogRecord
    ) -> bool:
        record.request_id = get_request_id()
        return True


def configure_logging():
    """
    Configure application-wide logging.
    """

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "request_id=%(request_id)s | "
        "%(message)s"
    )

    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(formatter)

    handler.addFilter(
        RequestIDFilter()
    )

    root_logger = logging.getLogger()

    root_logger.setLevel(
        logging.INFO
    )

    root_logger.handlers.clear()

    root_logger.addHandler(
        handler
    )