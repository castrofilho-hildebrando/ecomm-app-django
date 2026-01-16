import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from infrastructure.middleware.auth_middleware import authenticate, is_admin
from .models import User


@require_http_methods(["GET"])
@authenticate
@is_admin
def get_all_users(request):
    try:
        users = User.objects.all().values('id', 'name', 'email', 'role', 'created_at')
        return JsonResponse(list(users), safe=False)
    except Exception:
        return JsonResponse({'error': 'Erro ao listar usuários'}, status=500)


@require_http_methods(["GET"])
@authenticate
@is_admin
def get_user_by_id(request, user_id):
    try:
        user = User.objects.filter(id=user_id).values('id', 'name', 'email', 'role', 'created_at').first()
        
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        
        return JsonResponse(user)
    except Exception:
        return JsonResponse({'error': 'Erro ao buscar usuário'}, status=500)


@require_http_methods(["PUT"])
@authenticate
@is_admin
def update_user(request, user_id):
    try:
        data = json.loads(request.body)
        
        user = User.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        
        user.save()
        
        user_data = {
            'id': str(user.id),
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at
        }
        
        return JsonResponse({
            'message': 'Usuário atualizado com sucesso!',
            'user': user_data
        })
    except Exception:
        return JsonResponse({'error': 'Erro ao atualizar usuário'}, status=500)


@require_http_methods(["DELETE"])
@authenticate
@is_admin
def delete_user(request, user_id):
    try:
        user = User.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
        
        user.delete()
        
        return JsonResponse({'message': 'Usuário removido com sucesso!'})
    except Exception:
        return JsonResponse({'error': 'Erro ao remover usuário'}, status=500)
