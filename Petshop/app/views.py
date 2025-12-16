from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy




class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        if request.user.is_authenticated and not request.user.is_staff:
            agendamentos = Agendamento.objects.filter(
                pet__cliente__email=request.user.email
            ).select_related('pet', 'servico', 'funcionario').order_by('data_agendamento', 'hora')
            context['agendamentos'] = agendamentos

        return render(request, 'index.html', context)
    def post(self, request):
        pass    


class PerfilView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        return render(request, 'perfil.html', {'user': request.user})




class RacaView(View):
    def get(self, request, *args, **kwargs):
        racas = Raca.objects.all()
        return render(request, 'raca/raca.html', {'racas': racas})


class EditarRacaView(View):
    template_name = 'raca/editar_raca.html'

    def get(self, request, id, *args, **kwargs):
        raca_instance = get_object_or_404(Raca, id_raca=id)
        form = RacaFormView(instance=raca_instance)
        return render(request, self.template_name, {
            'raca': raca_instance,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        raca_instance = get_object_or_404(Raca, id_raca=id)
        form = RacaFormView(request.POST, instance=raca_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Raça atualizada com sucesso.')
            return redirect('raca')

        return render(request, self.template_name, {
            'raca': raca_instance,
            'form': form
        })


class DeleteRacaView(View):
    def post(self, request, id, *args, **kwargs):
        raca = get_object_or_404(Raca, id_raca=id)
        raca.delete()
        messages.success(request, 'Raça deletada com sucesso.')
        return redirect('raca')
    
class CreateRacaView(View):
    template_name = 'raca/cadastrar_raca.html'

    def get(self, request, *args, **kwargs):
        form = RacaFormView()
        return render(request, self.template_name, {'form': form})


class AgendamentoView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            agendamentos = Agendamento.objects.all()
        else:
            agendamentos = Agendamento.objects.filter(pet__cliente__email=request.user.email)

        return render(request, 'agendamento/agendamento.html', {'agendamentos': agendamentos})


class AgendamentosHojeView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden()

        # Allow staff to select a date via ?date=YYYY-MM-DD; default to today
        date_str = request.GET.get('date')
        if date_str:
            selected_date = parse_date(date_str)
            if selected_date is None:
                selected_date = timezone.localdate()
        else:
            selected_date = timezone.localdate()

        agendamentos = Agendamento.objects.filter(data_agendamento=selected_date).select_related('pet', 'servico', 'funcionario').order_by('hora')
        return render(request, 'agendamento/hoje.html', {'agendamentos': agendamentos, 'selected_date': selected_date})


class CreateAgendamentoView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'agendamento/cadastrar_agendamento.html'

    def get(self, request, *args, **kwargs):
        form = AgendamentoFormView(user=request.user)
        if not request.user.is_staff:
            form.fields['pet'].queryset = Pet.objects.filter(cliente__email=request.user.email)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AgendamentoFormView(request.POST, user=request.user)
        if not request.user.is_staff:
            form.fields['pet'].queryset = Pet.objects.filter(cliente__email=request.user.email)

        if form.is_valid():
            ag = form.save(commit=False)
            # Atribuir automaticamente um funcionário qualificado e disponível
            servico = ag.servico
            d = ag.data_agendamento
            t = ag.hora
            funcionarios = Funcionario.objects.all()
            if servico:
                funcionarios = funcionarios.filter(funcao__icontains=servico.nome)
            if d and t:
                conflicted = Agendamento.objects.filter(data_agendamento=d, hora=t).values_list('funcionario_id', flat=True)
                funcionarios = funcionarios.exclude(id_funcionario__in=conflicted)
            funcionario_escolhido = funcionarios.order_by('nome').first()
            if not funcionario_escolhido:
                funcionario_escolhido = Funcionario.objects.order_by('nome').first()
            ag.funcionario = funcionario_escolhido
            ag.save()
            messages.success(request, 'Agendamento cadastrado com sucesso.')
            return redirect('agendamento')

        return render(request, self.template_name, {'form': form})


class EditarAgendamentoView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'agendamento/editar_agendamento.html'

    def get(self, request, id, *args, **kwargs):
        agendamento = get_object_or_404(Agendamento, id_agendamento=id)

        if not (request.user.is_staff or (agendamento.pet.cliente and agendamento.pet.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        form = AgendamentoFormView(instance=agendamento, user=request.user)
        if not request.user.is_staff:
            form.fields['pet'].queryset = Pet.objects.filter(cliente__email=request.user.email)
        return render(request, self.template_name, {
            'agendamento': agendamento,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        agendamento = get_object_or_404(Agendamento, id_agendamento=id)

        if not (request.user.is_staff or (agendamento.pet.cliente and agendamento.pet.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        form = AgendamentoFormView(request.POST, instance=agendamento, user=request.user)
        if not request.user.is_staff:
            form.fields['pet'].queryset = Pet.objects.filter(cliente__email=request.user.email)

        if form.is_valid():
            ag = form.save(commit=False)
            # Reatribuir funcionário se necessário (manter atual se disponível)
            d = ag.data_agendamento
            t = ag.hora
            servico = ag.servico
            conflicted_qs = Agendamento.objects.filter(data_agendamento=d, hora=t)
            if ag.id_agendamento:
                conflicted_qs = conflicted_qs.exclude(id_agendamento=ag.id_agendamento)
            conflicted_ids = conflicted_qs.values_list('funcionario_id', flat=True)

            # Se funcionário atual está livre, mantê-lo
            if ag.funcionario and ag.funcionario.id_funcionario not in conflicted_ids:
                pass
            else:
                funcionarios = Funcionario.objects.all()
                if servico:
                    funcionarios = funcionarios.filter(funcao__icontains=servico.nome)
                if d and t:
                    funcionarios = funcionarios.exclude(id_funcionario__in=conflicted_ids)
                funcionario_escolhido = funcionarios.order_by('nome').first()
                if not funcionario_escolhido:
                    funcionario_escolhido = Funcionario.objects.order_by('nome').first()
                ag.funcionario = funcionario_escolhido

            ag.save()
            messages.success(request, 'Agendamento atualizado com sucesso.')
            return redirect('agendamento')

        return render(request, self.template_name, {
            'agendamento': agendamento,
            'form': form
        })


class DeleteAgendamentoView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, id, *args, **kwargs):
        agendamento = get_object_or_404(Agendamento, id_agendamento=id)

        if not (request.user.is_staff or (agendamento.pet.cliente and agendamento.pet.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        agendamento.delete()
        messages.success(request, 'Agendamento deletado com sucesso.')
        return redirect('agendamento')


@login_required
@require_GET
def ajax_get_funcionarios(request):
    # endpoint removido: kept for compatibility but returns empty list
    return JsonResponse({'funcionarios': []})

    def post(self, request, *args, **kwargs):
        form = RacaFormView(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Raça cadastrada com sucesso.')
            return redirect('raca')

        return render(request, self.template_name, {'form': form})


class EspecieView(View):
    def get(self, request, *args, **kwargs):
        especies = Especie.objects.all()
        return render(request, 'especie/especie.html', {'especies': especies})


class EditarEspecieView(View):
    template_name = 'especie/editar_especie.html'

    def get(self, request, id, *args, **kwargs):
        especie_instance = get_object_or_404(Especie, id_especie=id)
        form = EspecieFormView(instance=especie_instance)
        return render(request, self.template_name, {
            'especie': especie_instance,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        especie_instance = get_object_or_404(Especie, id_especie=id)
        form = EspecieFormView(request.POST, instance=especie_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Espécie atualizada com sucesso.')
            return redirect('especie')

        return render(request, self.template_name, {
            'especie': especie_instance,
            'form': form
        })


class DeleteEspecieView(View):
    def post(self, request, id, *args, **kwargs):
        especie = get_object_or_404(Especie, id_especie=id)
        especie.delete()
        messages.success(request, 'Espécie deletada com sucesso.')
        return redirect('especie')
    
class CreateEspecieView(View):
    template_name = 'especie/cadastrar_especie.html'

    def get(self, request, *args, **kwargs):
        form = EspecieFormView()
        return render(request, self.template_name, {'form': form})


class ServicoView(View):
    def get(self, request, *args, **kwargs):
        servicos = Servico.objects.all()
        return render(request, 'servico/servico.html', {'servicos': servicos})


class EditarServicoView(View):
    template_name = 'servico/editar_servico.html'

    def get(self, request, id, *args, **kwargs):
        servico_instance = get_object_or_404(Servico, id_servico=id)
        form = ServicoFormView(instance=servico_instance)
        return render(request, self.template_name, {
            'servico': servico_instance,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        servico_instance = get_object_or_404(Servico, id_servico=id)
        form = ServicoFormView(request.POST, instance=servico_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso.')
            return redirect('servico')

        return render(request, self.template_name, {
            'servico': servico_instance,
            'form': form
        })


class DeleteServicoView(View):
    def post(self, request, id, *args, **kwargs):
        servico = get_object_or_404(Servico, id_servico=id)
        servico.delete()
        messages.success(request, 'Serviço deletado com sucesso.')
        return redirect('servico')
    
class CreateServicoView(View):
    template_name = 'servico/cadastrar_servico.html'

    def get(self, request, *args, **kwargs):
        form = ServicoFormView()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ServicoFormView(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso.')
            return redirect('servico')

        return render(request, self.template_name, {'form': form})


class FuncionarioView(View):
    def get(self, request, *args, **kwargs):
        funcionarios = Funcionario.objects.all()
        return render(request, 'funcionario/funcionario.html', {'funcionarios': funcionarios})


class EditarFuncionarioView(View):
    template_name = 'funcionario/editar_funcionario.html'

    def get(self, request, id, *args, **kwargs):
        funcionario_instance = get_object_or_404(Funcionario, id_funcionario=id)
        form = FuncionarioFormView(instance=funcionario_instance)
        return render(request, self.template_name, {
            'funcionario': funcionario_instance,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        funcionario_instance = get_object_or_404(Funcionario, id_funcionario=id)
        form = FuncionarioFormView(request.POST, instance=funcionario_instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso.')
            return redirect('funcionario')

        return render(request, self.template_name, {
            'funcionario': funcionario_instance,
            'form': form
        })


class DeleteFuncionarioView(View):
    def post(self, request, id, *args, **kwargs):
        funcionario = get_object_or_404(Funcionario, id_funcionario=id)
        funcionario.delete()
        messages.success(request, 'Funcionário deletado com sucesso.')
        return redirect('funcionario')
    
class CreateFuncionarioView(View):
    template_name = 'funcionario/cadastrar_funcionario.html'

    def get(self, request, *args, **kwargs):
        form = FuncionarioFormView()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FuncionarioFormView(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('funcionario')

        return render(request, self.template_name, {'form': form})


@login_required
def pagamento(request):
    """Lista agendamentos disponíveis para o usuário (ou todos se staff)
    e cria um registro em `Pagamento` ao confirmar método.
    """
    if request.method == 'POST':
        agendamento_id = request.POST.get('agendamento_id')
        metodo = request.POST.get('metodo', 'Não informado')

        if not agendamento_id:
            messages.error(request, 'Selecione um agendamento.')
            return redirect('pagamento')

        try:
            ag = Agendamento.objects.select_related('servico').get(id_agendamento=agendamento_id)
        except Agendamento.DoesNotExist:
            messages.error(request, 'Agendamento inválido.')
            return redirect('pagamento')

        valor = ag.servico.valor if ag.servico and hasattr(ag.servico, 'valor') else 0

        pagamento_obj = Pagamento(
            agendamento=ag,
            valor=valor,
            forma_pagamento=metodo,
            data_pagamento=timezone.now()
        )
        pagamento_obj.save()

        messages.success(request, f'Pagamento registrado (Agendamento #{ag.id_agendamento}) — {metodo} — R$ {valor}')
        return redirect('pagamento')

    # GET: listar agendamentos
    if request.user.is_staff:
        agendamentos = Agendamento.objects.select_related('pet', 'servico').order_by('data_agendamento', 'hora')
    else:
        agendamentos = Agendamento.objects.select_related('pet', 'servico').filter(pet__cliente__email=request.user.email).order_by('data_agendamento', 'hora')

    return render(request, 'pagamento/pagamento.html', {'agendamentos': agendamentos})


@login_required
def pagamentos(request):
    """Lista pagamentos: staff vê todos; usuário vê apenas os seus."""
    if request.user.is_staff:
        pagamentos_qs = Pagamento.objects.select_related('agendamento__pet', 'agendamento__servico').order_by('-data_pagamento')
    else:
        pagamentos_qs = Pagamento.objects.select_related('agendamento__pet', 'agendamento__servico').filter(agendamento__pet__cliente__email=request.user.email).order_by('-data_pagamento')

    return render(request, 'pagamento/pagamentos.html', {'pagamentos': pagamentos_qs})


class PetView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            pets = Pet.objects.select_related('raca', 'especie', 'cliente').all()
        else:
            pets = Pet.objects.select_related('raca', 'especie', 'cliente').filter(cliente__email=request.user.email)

        return render(request, 'pet/pet.html', {'pets': pets})


class CreatePetView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'pet/cadastrar_pet.html'

    def get(self, request, *args, **kwargs):
        form = PetFormView()
        if not request.user.is_staff:
            form.fields.pop('cliente', None)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PetFormView(request.POST)
        if not request.user.is_staff:
            form.fields.pop('cliente', None)

        if form.is_valid():
            pet_obj = form.save(commit=False)

            # Associate or create Cliente based on logged-in user
            if request.user.is_authenticated:
                cliente = Cliente.objects.filter(email=request.user.email).first()
                if not cliente:
                    nome = request.user.get_full_name() or request.user.username
                    cliente = Cliente.objects.create(nome=nome, email=request.user.email)

                pet_obj.cliente = cliente

            pet_obj.save()
            messages.success(request, 'Pet cadastrado com sucesso.')
            return redirect('pet')

        return render(request, self.template_name, {'form': form})


class EditarPetView(LoginRequiredMixin, View):
    login_url = 'login'
    template_name = 'pet/editar_pet.html'

    def get(self, request, id, *args, **kwargs):
        pet_instance = get_object_or_404(Pet, id_pet=id)

        if not (request.user.is_staff or (pet_instance.cliente and pet_instance.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        form = PetFormView(instance=pet_instance)
        if not request.user.is_staff:
            form.fields.pop('cliente', None)
        return render(request, self.template_name, {
            'pet': pet_instance,
            'form': form
        })

    def post(self, request, id, *args, **kwargs):
        pet_instance = get_object_or_404(Pet, id_pet=id)

        if not (request.user.is_staff or (pet_instance.cliente and pet_instance.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        form = PetFormView(request.POST, instance=pet_instance)
        if not request.user.is_staff:
            form.fields.pop('cliente', None)

        if form.is_valid():
            pet_obj = form.save(commit=False)

            # If non-staff editing, ensure cliente remains the same
            if not request.user.is_staff and pet_instance.cliente:
                pet_obj.cliente = pet_instance.cliente

            pet_obj.save()
            messages.success(request, 'Pet atualizado com sucesso.')
            return redirect('pet')

        return render(request, self.template_name, {
            'pet': pet_instance,
            'form': form
        })


class DeletePetView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, id, *args, **kwargs):
        pet = get_object_or_404(Pet, id_pet=id)

        if not (request.user.is_staff or (pet.cliente and pet.cliente.email == request.user.email)):
            return HttpResponseForbidden()

        pet.delete()
        messages.success(request, 'Pet deletado com sucesso.')
        return redirect('pet')

    def post(self, request, *args, **kwargs):
        form = FuncionarioFormView(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso.')
            return redirect('funcionario')

        return render(request, self.template_name, {'form': form})
    
