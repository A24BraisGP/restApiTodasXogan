from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'nome' 

    def validate(self, attrs):
        attrs['username'] = attrs.get(self.username_field)              
        data = super().validate(attrs)

        return data
class XeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xenero
        fields = '__all__'


class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'


class AccesibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accesibilidade
        fields = '__all__'


class VideoxogoSerializer(serializers.ModelSerializer):
    xenero = serializers.PrimaryKeyRelatedField(many=True, queryset=Xenero.objects.all(), required=False)
    plataforma = serializers.PrimaryKeyRelatedField(many=True, queryset=Plataforma.objects.all(), required=False)
    accesibilidades = serializers.PrimaryKeyRelatedField(many=True, queryset=Accesibilidade.objects.all(), required=False)
    class Meta:
        model = Videoxogo
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    favoritos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    preferencias = AccesibilidadeSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    

    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'password', 'imaxe_user', 'admin', 'favoritos', 'preferencias']
        extra_kwargs = {
            'email': {'write_only':True},
            'password': {'write_only': True},
            'admin': {'read_only' : True}
        }

    # El método create debe usar user.set_password() en el nuevo modelo.
    def create(self, validated_data):
        # Extrae la contraseña del diccionario validated_data
        password = validated_data.pop('password', None)
        
        # Crea la instancia del usuario SIN la contraseña encriptada aún
        # El campo 'admin' se puede asignar directamente
        usuario = Usuario.objects.create(**validated_data)
        
        # Usa el método set_password() del modelo (que viene de AbstractBaseUser)
        # para hashear y guardar la contraseña de forma segura.
        if password is not None:
            usuario.set_password(password)
            usuario.save() # Guarda los cambios después de establecer la contraseña
        
        return usuario

class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = '__all__'


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'


class VideoxogoAccesibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoxogoAccesibilidade
        fields = '__all__'


class PreferenciasAccesibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciasAccesibilidade
        fields = '__all__'


class PropostaVideoxogoSerializer(serializers.ModelSerializer):
    xenero = serializers.PrimaryKeyRelatedField(many=True, queryset=Xenero.objects.all(), required=False)
    plataforma = serializers.PrimaryKeyRelatedField(many=True, queryset=Plataforma.objects.all(), required=False)
    accesibilidades = serializers.PrimaryKeyRelatedField(many=True, queryset=Accesibilidade.objects.all(), required=False)
    usuario = UsuarioSerializer(read_only=True)
    admin_revisor = UsuarioSerializer(read_only=True)

    class Meta:
        model = PropostaVideoxogo
        fields = '__all__'
        read_only_fields = ('data_creacion', 'admin_revisor')

    def create(self, validated_data):
        xenero_data = validated_data.pop('xenero', [])
        plataforma_data = validated_data.pop('plataforma', [])
        accesibilidades_data = validated_data.pop('accesibilidades', [])
        
        proposta = PropostaVideoxogo.objects.create(**validated_data)
        
        for xenero in xenero_data:
            PropostaVideoxogoXenero.objects.create(proposta=proposta, xenero=xenero)
            
        for plataforma in plataforma_data:
            PropostaVideoxogoPlataforma.objects.create(proposta=proposta, plataforma=plataforma)
            
        for accesibilidade in accesibilidades_data:
            PropostaVideoxogoAccesibilidade.objects.create(proposta=proposta, accesibilidade=accesibilidade)
            
        return proposta

class PropostaVideoxogoXeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropostaVideoxogoXenero
        fields = '__all__'

class PropostaVideoxogoPlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropostaVideoxogoPlataforma
        fields = '__all__'

class PropostaVideoxogoAccesibilidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropostaVideoxogoAccesibilidade
        fields = '__all__' 