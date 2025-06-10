from rest_framework import generics, status
from .models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import  check_password
from django.http import Http404



@api_view(['GET'])
def api_home(request, format=None):
    return Response({
        'mensaje': 'Bienvenido a la API de TodasXogan'
    })

# Usuarios
class UsuarioListCreateView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# Videoxogos
class VideoxogoListCreateView(generics.ListCreateAPIView):
    queryset = Videoxogo.objects.all()
    serializer_class = VideoxogoSerializer

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
    def post(self, request):
        nome = request.data.get('nome')
        contrasinal = request.data.get('contrasinal')
        
        if not nome or not contrasinal:
            return Response({
                'error': 'Por favor, proporciona nombre de usuario y contraseña'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(nome=nome)
            if check_password(contrasinal, usuario.contrasinal):
                serializer = UsuarioSerializer(usuario)
                return Response({
                    'usuario': serializer.data,
                    'mensaje': 'Login exitoso'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Contraseña incorrecta'
                }, status=status.HTTP_401_UNAUTHORIZED)
        except Usuario.DoesNotExist:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': f'Error en el servidor: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def check_nome_usuario(request, nome):
    exists = Usuario.objects.filter(nome=nome).exists()
    return Response({'exists': exists})

# Propostas de Videoxogos
class PropostaVideoxogoListCreateView(generics.ListCreateAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer

    def get_queryset(self):
        return PropostaVideoxogo.objects.all()

class PropostaVideoxogoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer

    def get_queryset(self):
        return PropostaVideoxogo.objects.all()

class PropostaVideoxogoRevisionView(generics.UpdateAPIView):
    queryset = PropostaVideoxogo.objects.all()
    serializer_class = PropostaVideoxogoSerializer

    def get_queryset(self):
        return PropostaVideoxogo.objects.filter(estado='PENDENTE')

