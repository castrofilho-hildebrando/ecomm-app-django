import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps


def authenticate(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return JsonResponse({'error': 'Token não fornecido'}, status=401)
        
        parts = auth_header.split(' ')
        
        if len(parts) != 2 or parts[0] != 'Bearer':
            return JsonResponse({'error': 'Formato de token inválido'}, status=401)
        
        token = parts[1]
        
        if not token:
            return JsonResponse({'error': 'Token inválido'}, status=401)
        
        try:
            decoded = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            if not isinstance(decoded, dict) or 'user_id' not in decoded or 'role' not in decoded:
                return JsonResponse({'error': 'Token inválido'}, status=401)
            
            if decoded['role'] not in ['user', 'admin']:
                return JsonResponse({'error': 'Token inválido'}, status=401)
            
            request.user_data = {
                'user_id': decoded['user_id'],
                'role': decoded['role']
            }
            
            return view_func(request, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expirado'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Token inválido'}, status=401)
    
    return wrapper


def is_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request, 'user_data'):
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
        
        if request.user_data['role'] != 'admin':
            return JsonResponse({'error': 'Acesso negado: apenas administradores'}, status=403)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper