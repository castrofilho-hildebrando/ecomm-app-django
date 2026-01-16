from rest_framework.views import exception_handler
from rest_framework.response import Response
from domain.errors.domain_error import DomainError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, DomainError):
        return Response(
            {'error': exc.message, 'code': exc.code},
            status=400
        )
    
    return response