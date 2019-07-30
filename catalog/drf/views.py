from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler

from drf.exceptions import APIBaseHttpException


def custom_exception_handler(exc, context):
    request = context['request']
    response = exception_handler(exc, context)

    if request.version == api_settings.DEFAULT_VERSION:

        if response is None and isinstance(exc, APIBaseHttpException):
            data = exc.get_detailed_info()

            return Response(
                data,
                status=exc.http_status_code,
                content_type='application/json'
            )

    return response
