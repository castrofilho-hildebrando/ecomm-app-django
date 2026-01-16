import json
import jwt
import bcrypt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.users.models import User


@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return JsonResponse(
                {'error': 'Nome, email e senha são obrigatórios'},
                status=400
            )
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'E-mail já registrado'}, status=409)
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User.objects.create(
            name=name,
            email=email,
            password=password_hash,
            role='user'
        )
        
        token = jwt.encode(
            {
                'user_id': str(user.id),
                'role': user.role
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return JsonResponse({
            'token': token,
            'user': {
                '_id': str(user.id),
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }, status=201)
        
    except Exception as e:
        print(f"Erro no registro de usuário: {e}")
        return JsonResponse({'error': 'Erro interno ao registrar usuário.'}, status=500)


@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return JsonResponse({'error': 'Credenciais inválidas'}, status=401)
        
        is_match = bcrypt.checkpw(
            password.encode('utf-8'),
            user.password.encode('utf-8')
        )
        
        if not is_match:
            return JsonResponse({'error': 'Credenciais inválidas'}, status=401)
        
        token = jwt.encode(
            {
                'user_id': str(user.id),
                'role': user.role
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        
        return JsonResponse({'token': token, 'role': user.role})
        
    except Exception as e:
        print(f"Erro no login: {e}")
        return JsonResponse({'error': 'Erro interno do servidor.'}, status=500)
