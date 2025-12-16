"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.views.generic import TemplateView
from django.urls import include
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', include('accounts.urls')),
    

    path('', IndexView.as_view(), name='index'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('pagamento/', pagamento, name='pagamento'),
    path('pagamentos/', pagamentos, name='pagamentos'),

    
    
    path('raca/', RacaView.as_view(), name='raca'),
    path('raca/cadastrar/', CreateRacaView.as_view(), name='cadastrar_raca'),
    path('raca/editar/<int:id>/', EditarRacaView.as_view(), name='editar_raca'),
    path('raca/deletar/<int:id>/', DeleteRacaView.as_view(), name='deletar_raca'),
    
    path('especie/', EspecieView.as_view(), name='especie'),
    path('especie/cadastrar/', CreateEspecieView.as_view(), name='cadastrar_especie'),
    path('especie/editar/<int:id>/', EditarEspecieView.as_view(), name='editar_especie'),
    path('especie/deletar/<int:id>/', DeleteEspecieView.as_view(), name='deletar_especie'),
    
    path('funcionario/', FuncionarioView.as_view(), name='funcionario'),
    path('funcionario/cadastrar/', CreateFuncionarioView.as_view(), name='cadastrar_funcionario'),
    path('funcionario/editar/<int:id>/', EditarFuncionarioView.as_view(), name='editar_funcionario'),
    path('funcionario/deletar/<int:id>/', DeleteFuncionarioView.as_view(), name='deletar_funcionario'),
    
    path('servico/', ServicoView.as_view(), name='servico'),
    path('servico/cadastrar/', CreateServicoView.as_view(), name='cadastrar_servico'),
    path('servico/editar/<int:id>/', EditarServicoView.as_view(), name='editar_servico'),
    path('servico/deletar/<int:id>/', DeleteServicoView.as_view(), name='deletar_servico'),
    
    path('pet/', PetView.as_view(), name='pet'),
    path('pet/cadastrar/', CreatePetView.as_view(), name='cadastrar_pet'),
    path('pet/editar/<int:id>/', EditarPetView.as_view(), name='editar_pet'),
    path('pet/deletar/<int:id>/', DeletePetView.as_view(), name='deletar_pet'),
    
    path('agendamento/', AgendamentoView.as_view(), name='agendamento'),
    path('agendamento/hoje/', AgendamentosHojeView.as_view(), name='agendamento_hoje'),
    path('agendamento/cadastrar/', CreateAgendamentoView.as_view(), name='cadastrar_agendamento'),
    path('agendamento/editar/<int:id>/', EditarAgendamentoView.as_view(), name='editar_agendamento'),
    path('agendamento/deletar/<int:id>/', DeleteAgendamentoView.as_view(), name='deletar_agendamento'),
]