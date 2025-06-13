from django.db import models
from django.core.validators import MinValueValidator
from django import forms
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils.translation import gettext_lazy as _ 


# Create your models here.
class Plataforma(models.Model):
    plataforma = models.CharField(max_length=250)
    
    def __str__(self):
        return self.plataforma

class VideoxogoPlataforma(models.Model):
    videoxogo = models.ForeignKey('Videoxogo', on_delete=models.CASCADE)
    plataforma = models.ForeignKey('Plataforma',on_delete=models.CASCADE)

    class Meta: 
        db_table = 'restApi_videoxogoPlataform_videoxogoPlataforma'
        unique_together = ('videoxogo','plataforma')

class Xenero(models.Model):
    xenero = models.CharField(max_length=250)

    def __str__(self):
        return self.xenero

class VideoxogoXenero(models.Model):
    videoxogo = models.ForeignKey('Videoxogo',on_delete=models.CASCADE)
    xenero = models.ForeignKey('Xenero',on_delete=models.CASCADE)

    class Meta: 
        db_table = 'restApi_videoxogoXenero_videoxogoXenero'
        unique_together = ('videoxogo','xenero')



class Videoxogo(models.Model):
    class AgeChoices(models.IntegerChoices):
        AGE_3 = 3, '3+'
        AGE_6 = 6, '6+'
        AGE_9 = 9, '9+'
        AGE_12 = 12, '12+'
        AGE_16 = 16, '16+'
        AGE_18 = 18, '18+'
    
    titulo = models.CharField(max_length=250)
    descricion = models.TextField(max_length=1000)
    prezo = models.DecimalField(editable=True,validators=[MinValueValidator(0,0)],max_digits=4,decimal_places=2)
    idade_recomendada = models.IntegerField(choices=AgeChoices.choices, default=AgeChoices.AGE_3)
    desarrolladora = models.CharField(max_length=250, null=True, blank=True)
    caratula = models.ImageField(upload_to="games/",null=True,blank=True)
    alt = models.CharField(max_length=250, null=True, blank=True, help_text="Descripción alternativa de la carátula para accesibilidad")
    xenero = models.ManyToManyField('Xenero',through='VideoxogoXenero',related_name='videoxogo_xenero')
    plataforma = models.ManyToManyField('Plataforma',through='VideoxogoPlataforma',related_name='videoxogos_plataforma')
    accesibilidades = models.ManyToManyField('Accesibilidade', through='VideoxogoAccesibilidade', related_name='videoxogos')
    
    def __str__(self):
        return self.titulo
    

# --- Define tu Custom User Manager ---
# Este manager es crucial. Sabe cómo crear instancias de tu modelo de usuario
# y cómo manejar contraseñas, staff, y superusuarios.
class UsuarioManager(BaseUserManager):
    def create_user(self, nome, email, password=None, **extra_fields):
        if not nome:
            raise ValueError('O campo nome de usuario é obrigatorio.')
        if not email:
            raise ValueError('O enderezo de correo electrónico é obrigatorio.')

        email = self.normalize_email(email)
        user = self.model(nome=nome, email=email, **extra_fields)
        user.set_password(password) # ¡Usa set_password para hashear la contraseña!
        user.save(using=self._db)
        return user

    def create_superuser(self, nome, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('admin', True) # Si tu campo 'admin' tiene un propósito específico

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe ter is_superuser=True.')

        return self.create_user(nome, email, password, **extra_fields)

# --- Tu Custom User Model Refactorizado ---
class Usuario(AbstractBaseUser, PermissionsMixin):
    # Campos existentes de tu modelo original:
    nome = models.CharField(max_length=100, unique=True, help_text="Nome de usuario único.")
    email = models.EmailField(max_length=250, unique=True, help_text="Enderezo de correo electrónico único.")
    
       # ¡ESTOS SON LOS CAMPOS QUE FALTAN Y DEBES AÑADIR!
    password = models.CharField(_("password"), max_length=128)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    
    imaxe_user = models.ImageField(upload_to="users/", null=True, blank=True, help_text="Imaxe de perfil do usuario.")
    admin = models.BooleanField(default=False, help_text="Indica se o usuario ten rol de administrador personalizado.")

    # Campos de relación ManyToMany:
    favoritos = models.ManyToManyField('Videoxogo', through='Favorito', related_name='usuarios_favoritos', blank=True)
    preferencias = models.ManyToManyField('Accesibilidade', through='PreferenciasAccesibilidade', related_name='usuario_preferencias', blank=True)

    # Campos requeridos por AbstractBaseUser para la integración con Django Admin y autenticación:
    is_active = models.BooleanField(default=True, help_text="Indica se o usuario está activo.")
    is_staff = models.BooleanField(default=False, help_text="Indica se o usuario pode acceder á área de administración.")
    date_joined = models.DateTimeField(auto_now_add=True) # Campo común para registrar la fecha de creación

    # Conexión al Manager personalizado:
    objects = UsuarioManager()

    # Define el campo que se usará como identificador único para el login:
    USERNAME_FIELD = 'nome' 
    
    # Campos adicionales que se pedirán al crear un superusuario (además de USERNAME_FIELD y la contraseña):
    REQUIRED_FIELDS = ['email'] # Si tu 'email' es un campo que debería ser solicitado al crear superuser

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        # Puedes añadir db_table = 'nome_da_táboa_usuario' si quieres que la tabla mantenga el nombre antiguo.

    def __str__(self):
        return self.nome

 
    # Métodos para PermissionsMixin (útiles para compatibilidad con el sistema de permisos de Django)
    def get_full_name(self):
        return self.nome

    def get_short_name(self):
        return self.nome


class Favorito(models.Model):
    usuario = models.ForeignKey('Usuario',on_delete=models.CASCADE)
    videoxogo = models.ForeignKey('Videoxogo',on_delete=models.CASCADE)
    
    class Meta: 
        unique_together = ('usuario','videoxogo')
    
class Comentario(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='comentarios')
    videoxogo = models.ForeignKey('Videoxogo' ,on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0,blank=True)
    dislikes = models.IntegerField(default=0,blank=True)
    
    
    
    class Meta: 
        ordering = ['-likes']
    
class VideoxogoAccesibilidade(models.Model):
    videoxogo = models.ForeignKey('Videoxogo',on_delete=models.CASCADE)
    accesibilidade = models.ForeignKey('Accesibilidade',on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.videoxogo} -- {self.accesibilidade}'
    
    class Meta: 
        unique_together = ('videoxogo','accesibilidade')
    
class Accesibilidade(models.Model):
    nome_accesibilidade = models.CharField(max_length=250)
    
    def __str__(self):
        return self.nome_accesibilidade
    

    
class PreferenciasAccesibilidade(models.Model):
    usuario = models.ForeignKey('Usuario',on_delete=models.CASCADE)
    accesibilidade = models.ForeignKey('Accesibilidade', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.usuario} -- {self.accesibilidade}'
    
    class Meta: 
        unique_together = ('usuario','accesibilidade')

class PropostaVideoxogo(models.Model):
   
    titulo = models.CharField(max_length=100)
    descricion = models.TextField()
    prezo = models.DecimalField(max_digits=10, decimal_places=2)
    idade_recomendada = models.IntegerField(choices=Videoxogo.AgeChoices.choices)
    usuario_id = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='propostas', null=True, blank=True)
    data_creacion = models.DateTimeField(auto_now_add=True)
    desarrolladora = models.CharField(max_length=250, null=True, blank=True)
    estado = models.CharField(max_length=10, default='PENDENTE')
    caratula = models.ImageField(upload_to="propostas", null=True, blank=True)
    alt = models.CharField(max_length=250, null=True, blank=True)
    xenero = models.ManyToManyField('Xenero', through='PropostaVideoxogoXenero', related_name='propostas_xenero',null=True,blank=True)
    plataforma = models.ManyToManyField('Plataforma', through='PropostaVideoxogoPlataforma', related_name='propostas_plataforma',null=True,blank=True)
    accesibilidades = models.ManyToManyField('Accesibilidade', through='PropostaVideoxogoAccesibilidade', related_name='propostas',null=True,blank=True)
  

    class Meta:
        db_table = 'proposta_videoxogo'

class PropostaVideoxogoXenero(models.Model):
    proposta = models.ForeignKey('PropostaVideoxogo', on_delete=models.CASCADE, null=True)
    xenero = models.ForeignKey('Xenero', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'proposta_videoxogo_xenero'
        unique_together = ('proposta', 'xenero')

class PropostaVideoxogoPlataforma(models.Model):
    proposta = models.ForeignKey('PropostaVideoxogo', on_delete=models.CASCADE, null=True)
    plataforma = models.ForeignKey('Plataforma', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'proposta_videoxogo_plataforma'
        unique_together = ('proposta', 'plataforma')

class PropostaVideoxogoAccesibilidade(models.Model):
    proposta = models.ForeignKey('PropostaVideoxogo', on_delete=models.CASCADE, null=True)
    accesibilidade = models.ForeignKey('Accesibilidade', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'proposta_videoxogo_accesibilidade'
        unique_together = ('proposta', 'accesibilidade')