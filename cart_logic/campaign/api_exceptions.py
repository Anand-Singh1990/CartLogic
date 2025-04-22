from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        # You can customize the structure here
        response.data = {
            "success": False,
            "error": response.data,
            "message": "Something went wrong. Please check the details."
        }
    else:
        # Handle unexpected exceptions not caught by DRF
        logger.error("Unhandled exception", exc_info=exc)
        response = Response({
            "success": False,
            "error": str(exc),
            "message": "An internal server error occurred."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response