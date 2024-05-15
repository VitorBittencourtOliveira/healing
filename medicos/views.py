from django.shortcuts import render, redirect
from medicos.models import Especialidades, DadosMedico, is_medico, DatasAbertas
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from pacientes.models import Consulta, Documento
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

@login_required
def CadastroMedico(request):
    if is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Você já é médico')
        return redirect('/medicos/abrir_horario')
    
    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'cadastro_medico.html', {'especialidades':especialidades, 'is_medico': is_medico(request.user)})
    
    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')
        
        if not crm or not nome or not cep or not cep or not rua or not bairro or not numero or not cim or not rg or not foto or not especialidade or not descricao or not valor_consulta:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect('/medicos/abrir_horario')
        
        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            especialidade_id=especialidade,
            descricao=descricao,
            valor_consulta=valor_consulta,
            user=request.user
        )
        dados_medico.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso!')
        return redirect('/medicos/abrir_horario')

@login_required
def AbrirHorario(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user, data__gt=timezone.now()).exclude(consulta__status='C').order_by("data")
        return render(request, 'abrir_horario.html', {'dados_medicos':dados_medicos, 'datas_abertas':datas_abertas, 'is_medico': is_medico(request.user)})
    
    elif request.method == "POST":
        data = request.POST.get('data')
        if not data:
            messages.add_message(request, constants.ERROR, "Por favor, informe uma data.")
            return redirect('/medicos/abrir_horario')
        data_formatada = datetime.strptime(data, '%Y-%m-%dT%H:%M')
        
        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data não pode ser anterior a data atual.')
            return redirect('/medicos/abrir_horario')
        
        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
        )
        horario_abrir.save()
        messages.add_message(request, constants.SUCCESS, 'Horario cadastrado com sucesso.')
        return redirect('/medicos/abrir_horario')

@login_required
def DelHorario(request, id_horario):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    data_aberta = DatasAbertas.objects.get(id=id_horario)
    if request.user != data_aberta.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua.')
        return redirect('/medicos/abrir_horario/')
    
    if data_aberta.agendado != False:
        messages.add_message(request, constants.ERROR, 'Essa consulta tem um agendamento.')
        return redirect('/medicos/abrir_horario/')
    
    horario = DatasAbertas.objects.get(id=id_horario)
    horario.delete()
    messages.add_message(request, constants.SUCCESS, 'Horário excluído com sucesso.')
    return redirect('/medicos/abrir_horario')
        
@login_required        
def ConsultasMedico(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    data = request.GET.get("data")
    paciente = request.GET.get("paciente")
        
    hoje = datetime.now().date()
    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id')).filter(data_aberta__user=request.user).order_by('-data_aberta__data')
    
    if data:
        data = datetime.strptime(data, '%Y-%m-%d').date()
        consultas_restantes = consultas_restantes.annotate(data_aberta_date=TruncDate('data_aberta__data')).filter(data_aberta_date=data)
    if paciente:
        consultas_hoje = consultas_hoje.filter(paciente__username__icontains=paciente)
        consultas_restantes = consultas_restantes.filter(paciente__username__icontains=paciente)
    
    return render(request, 'consultas_medico.html', {'consultas_hoje':consultas_hoje, 'consultas_restantes':consultas_restantes, 'is_medico': is_medico(request.user)})
    
@login_required
def ConsultaAreaMedico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    if request.method == 'GET':
        documentos = Documento.objects.filter(consulta=consulta)
        dados_medico = DadosMedico.objects.get(user=request.user)
        return render(request, 'consulta_area_medico.html', {'consulta':consulta, 'is_medico': is_medico(request.user), 'documentos':documentos, 'dados_medico':dados_medico})
    elif request.method == 'POST':
        link = request.POST.get('link')
        
        if consulta.status == 'C':
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi cancelada.')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        elif consulta.status == 'F':
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi finalizada.')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        
        consulta.link = link
        consulta.status = 'I'
        consulta.save()
        messages.add_message(request, constants.SUCCESS, 'Consulta inicializada!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

@login_required
def FinalizarConsulta(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')

    consulta = Consulta.objects.get(id=id_consulta)
    
    if request.user != consulta.data_aberta.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua.')
        return redirect('/medicos/abrir_horario/')
    
    consulta.status = 'F'
    consulta.save()
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

@login_required
def AddDocumento(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if request.user != consulta.data_aberta.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')
    
    if not titulo:
        messages.add_message(request, constants.ERROR, 'Preencha o campo título.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    if not documento:
        messages.add_message(request, constants.ERROR, 'Preencha o campo documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento
    )
    documento.save()
    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso.')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

@login_required
def DelDocumento(request, id_consulta, id_documento):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('usuarios/sair')
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if request.user != consulta.data_aberta.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    documento = Documento.objects.get(id=id_documento)
    
    if documento.consulta != consulta:
        messages.add_message(request, constants.ERROR, 'Esse documento não pertence a essa consulta.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    documento.delete()
    messages.add_message(request, constants.SUCCESS, 'Documento removido com sucesso.')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

@login_required
def Dashboard(request):
    if not is_medico(request.user):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar.')
        return redirect('/usuarios/logout')
    
    consultas = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__range=[datetime.now().date() - timedelta(days=7), datetime.now().date() + timedelta(days=1)]).annotate(data_truncada=TruncDate('data_aberta__data')).values('data_truncada').annotate(quantidade=Count('id'))
    
    datas = [i['data_truncada'].strftime("%d-%m-%Y") for i in consultas]
    quantidade = [i['quantidade'] for i in consultas]
    
    return render(request, 'dashboard.html', {'datas':datas, 'quantidade':quantidade, 'is_medico': is_medico(request.user)})