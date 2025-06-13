"""
URL configuration for todasXogan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views 
from .views import (
    check_nome_usuario,
    PropostaVideoxogoListCreateView,
    PropostaVideoxogoDetailView,
    PropostaVideoxogoRevisionView,
)

urlpatterns = [
    path('',views.api_home, name='api-home'),
    path('usuarios/login/', views.LoginView.as_view(), name='login'),
    path('usuarios/', views.UsuarioListCreateView.as_view()),
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view()),
    path('videoxogos/', views.VideoxogoListCreateView.as_view()),
    path('videoxogos/<int:pk>/', views.VideoxogoDetailView.as_view()),
    path('xeneros/',views.XeneroListCreateView.as_view()),
    path('xeneros/<int:pk>/',views.XeneroDetailView.as_view()),
    path('plataformas/',views.PlataformaListCreateView.as_view()),
    path('plataformas/<int:pk>',views.PlataformaDetailView.as_view()),
    path('favoritos/<int:pk>',views.FavoritoDetailView.as_view()),
    path('favoritos/',views.FavoritoListCreateView.as_view()),
    path('favoritos/delete/',views.FavoritoDeleteView.as_view()),
    path('accesibilidades/',views.AccesibilidadeListCreateView.as_view()),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('usuarios/check-nome/<str:nome>/', check_nome_usuario, name='check-nome-usuario'),
    path('propostas/', PropostaVideoxogoListCreateView.as_view(), name='proposta-list-create'),
    path('propostas/<int:pk>/', PropostaVideoxogoDetailView.as_view(), name='proposta-detail'),
    path('propostas/<int:pk>/revision/', PropostaVideoxogoRevisionView.as_view(), name='proposta-revision'),
]  
