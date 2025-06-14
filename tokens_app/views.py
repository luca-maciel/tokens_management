from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Token
# Create your views here.

def home(request):
    return render(request, 'home.html')

def lista_tokens(request):
    tokens = Token.objects.all()
    return render(request, 'lista_tokens.html', {'tokens': tokens})

def atualizar_token(request, token_id):
    return HttpResponse("This view is not implemented yet.")
    # token = Token.objects.get(id=token_id)
    # if request.method == 'POST':
    #     token.nome_responsavel = request.POST.get('nome_responsavel')
    #     token.cpf_responsavel = request.POST.get('cpf_responsavel')
    #     token.funcao_responsavel = request.POST.get('funcao_responsavel')
    #     token.setor_responsavel = request.POST.get('setor_responsavel')
    #     token.telefone_responsavel = request.POST.get('telefone_responsavel')
    #     token.serial = request.POST.get('serial')
    #     token.data_solicitacao = request.POST.get('data_solicitacao')
    #     token.data_entrega = request.POST.get('data_entrega')
    #     token.observacao = request.POST.get('observacao')
    #     token.save()
    #     return redirect('lista_tokens')
    # return render(request, 'atualizar_token.html', {'token': token})