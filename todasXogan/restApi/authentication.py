from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import User
from supabase import create_client, Client
import os
from jose import jwt, JWTError
import requests

def get_jwks():
    jwks_url = f"{os.getenv('SUPABASE_URL')}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

class SupabaseJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        jwks = get_jwks()

        try:
            # Verificar el token con las claves JWKS de Supabase
            decoded_token = jwt.decode(token, jwks, algorithms=['RS256'], audience='authenticated')
            user_id = decoded_token.get('sub')
            if not user_id:
                raise AuthenticationFailed('Invalid token payload')

            # Inicializar cliente de Supabase
            supabase: Client = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_ANON_KEY'))

            # Obtener datos del usuario desde Supabase
            response = supabase.table('auth.users').select('id, email, user_metadata').eq('id', user_id).execute()
            user_data = response.data[0] if response.data else None

            if not user_data:
                raise AuthenticationFailed('User not found in Supabase')

            # Crear o actualizar usuario en Django
            user, created = User.objects.get_or_create(
                username=user_id,
                defaults={
                    'email': user_data.get('email', ''),
                    'first_name': user_data.get('user_metadata', {}).get('first_name', ''),
                    'last_name': user_data.get('user_metadata', {}).get('last_name', ''),
                }
            )

            if not created:
                # Actualizar datos si el usuario ya existe
                user.email = user_data.get('email', user.email)
                user.first_name = user_data.get('user_metadata', {}).get('first_name', user.first_name)
                user.last_name = user_data.get('user_metadata', {}).get('last_name', user.last_name)
                user.save()

            return (user, token)

        except JWTError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication error: {str(e)}')