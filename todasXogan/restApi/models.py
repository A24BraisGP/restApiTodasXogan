from django.db import models
from django.core.validators import MinValueValidator
from django import forms
from django.contrib.auth.hashers import check_password as django_check_password, make_password

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
    

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=250, unique=True)
    contrasinal = models.CharField(max_length=128)
    imaxe_user = models.ImageField(upload_to="users/",null=True,blank=True)
    admin = models.BooleanField(default=False, null=False)
    favoritos = models.ManyToManyField('Videoxogo', through='Favorito', related_name='usuarios_favoritos')
    preferencias = models.ManyToManyField('Accesibilidade', through='PreferenciasAccesibilidade',related_name='usuario_preferencias')
    
    def __str__(self):
        return self.nome

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.contrasinal)

    def save(self, *args, **kwargs):
        if self.contrasinal and not self.contrasinal.startswith('pbkdf2_sha256$'):
            self.contrasinal = make_password(self.contrasinal)
        super().save(*args, **kwargs)

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