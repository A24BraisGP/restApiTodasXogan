from rest_framework import generics, status
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import  check_password
from django.http import Http404
from django.contrib.auth import authenticate 
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


@api_view(['GET'])
def api_home(request, format=None):
    return Response({
        'mensaje': 'Bienvenido a la API de TodasXogan'
    })

# Usuarios
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    parser_classes= (MultiPartParser,FormParser,)

    # --- THIS IS THE KEY CHANGE ---
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'POST':
            # Allow ANY user to create a new account (POST request)
            return [AllowAny()]
        # For other methods (GET, HEAD, OPTIONS), apply the default permission
        # which you likely want to be IsAuthenticatedOrReadOnly or IsAuthenticated
        return [IsAuthenticatedOrReadOnly()] # Or [IsAuthenticated()] if only logged-in users can list


class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Videoxogos
class VideoxogoListCreateView(generics.ListCreateAPIView):
    queryset = Videoxogo.objects.all()
    serializer_class = VideoxogoSerializer
    parser_classes= (MultiPartParser,FormParser,)

class VideoxogoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Videoxogo.objects.all()
    serializer_class = VideoxogoSerializer

# Xéneros
class XeneroListCreateView(generics.ListCreateAPIView):
    queryset = Xenero.objects.all()
    serializer_class = XeneroSerializer

class XeneroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Xenero.objects.all()
    serializer_class = XeneroSerializer

# Plataformas
class PlataformaListCreateView(generics.ListCreateAPIView):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer

class PlataformaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plataforma.objects.all()
    serializer_class = PlataformaSerializer

# Accesibilidades
class AccesibilidadeListCreateView(generics.ListCreateAPIView):
    queryset = Accesibilidade.objects.all()
    serializer_class = AccesibilidadeSerializer

class AccesibilidadeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accesibilidade.objects.all()
    serializer_class = AccesibilidadeSerializer

# Comentarios
class ComentarioListCreateView(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class ComentarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

# Favoritos
class FavoritoListCreateView(generics.ListCreateAPIView):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer

class FavoritoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer

class FavoritoDeleteView(generics.DestroyAPIView):
    serializer_class = FavoritoSerializer

    def get_object(self):
        usuario_id = self.request.query_params.get('usuario')
        videoxogo_id = self.request.query_params.get('videoxogo')
        
        if not usuario_id or not videoxogo_id:
            raise Http404("Faltan parámetros en favoritos")
            
        try:
            return Favorito.objects.get(usuario_id=usuario_id, videoxogo_id=videoxogo_id)
        except Favorito.DoesNotExist:
            raise Http404("Non se atopou o favorito")

# Registro de usuarios
class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class LoginView(APIView):
    # This view doesn't require authentication for users to log in
    permission_classes = [] 

    def post(self, request, *args, **kwargs):
        # 1. Get credentials from the request body.
        # Make sure field names ('nome', 'contrasinal') match what your frontend sends.
        nome = request.data.get('nome')         # Your username field
        password = request.data.get('password') # Your password field

        if not nome or not password:
            return Response(
                {'error': 'Faltan nome e contrasinal.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 2. Authenticate the user using Django's `authenticate` function.
        # This function handles:
        # - Looking up the user by `username` (which is 'nome' in your case, configured via USERNAME_FIELD in your custom model).
        # - Verifying the `password` against the stored hash.
        # - Checking if the user is active (`is_active = True`).
        # It returns the User object on success, or None on failure.
        user = authenticate(request, username=nome, password=password)

        if user is not None:
            # 3. If authentication is successful, generate JWT tokens.
            try:
                # Create a refresh token for the authenticated user
                refresh = RefreshToken.for_user(user)
                # Get the access token string from the refresh token
                access_token = str(refresh.access_token)
                # Get the refresh token string
                refresh_token = str(refresh)

            except Exception as e:
                # Catch potential errors during token generation (e.g., misconfiguration of simplejwt)
                return Response(
                    {'error': f'Erro interno ao xerar tokens de sesión: {str(e)}'}, # Using Galician as per "Faltan nome e contrasinal"
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 4. Serialize the user data to include in the response.
            serializer = UsuarioSerializer(user)
            parser_classes= (MultiPartParser,FormParser,)

            # 5. Return a successful 200 OK response with tokens and user data.
            return Response({
                'access': access_token,
                'refresh': refresh_token,
                'usuario': serializer.data,  # User data for the frontend
                'mensaje': 'Login exitoso'   # Success message
            }, status=status.HTTP_200_OK)
        else:
            # 6. If `authenticate` returns None, credentials are invalid.
            # Return a 401 Unauthorized response with a generic error message for security.
            return Response(
                {'error': 'Credenciais inválidas. Usuario ou contrasinal incorrectos.'}, # Using Galician
                status=status.HTTP_401_UNAUTHORIZED
            )

@api_view(['GET'])
def check_nome_usuario(request, nome):
    exists = Usuario.objects.filter(nome=nome).exists()
    return Response({'exists': exists})

# Propostas de Videoxogos
class PropostaVideoxogoListCreateView(generics.ListCreateAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer
    parser_classes= (MultiPartParser,FormParser,)

    
    def get_queryset(self):
        return PropostaVideoxogo.objects.all()

class PropostaVideoxogoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer
    parser_classes= (MultiPartParser,FormParser,)


    def get_queryset(self):
        return PropostaVideoxogo.objects.all()

class PropostaVideoxogoRevisionView(generics.UpdateAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer
    parser_classes= (MultiPartParser,FormParser,)


    def get_queryset(self):
        return PropostaVideoxogo.objects.filter(estado='PENDENTE')

class AccesibilidadeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorito.objects.all()
    serializer_class = AccesibilidadeSerializer
