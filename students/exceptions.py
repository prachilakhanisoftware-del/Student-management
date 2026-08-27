import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "error": response.data,
        }
        return response

    logger.exception(
        "Unhandled exception occurred",
        exc_info=exc
    )

    return Response(
        {
            "success": False,
            "error": "Internal server error",
            "detail": "Something went wrong. Please try again later."
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
