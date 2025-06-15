from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Token, funcoes, setores
import openpyxl as xl
from .atualiza_lista import atualiza_lista_tokens
# Create your views here.

def home(request):
    return render(request, 'home.html')

def lista_tokens(request):
    tokens = Token.objects.all()
    return render(request, 'lista_tokens.html', {'tokens': tokens})

def atualizar_token(request, token_id):
    # return HttpResponse("This view is not implemented yet.")
    token = Token.objects.get(id=token_id)
    if request.method == 'POST':
        token.nome_responsavel = request.POST.get('nome_responsavel')
        token.cpf_responsavel = request.POST.get('cpf_responsavel')
        token.funcao_responsavel = request.POST.get('funcao_responsavel')
        token.setor_responsavel = request.POST.get('setor_responsavel')
        token.telefone_responsavel = request.POST.get('telefone_responsavel')
        token.serial = request.POST.get('serial')
        if request.POST.get('data_solicitacao'):
            token.data_solicitacao = request.POST.get('data_solicitacao')
        else:
            token.data_solicitacao = None
        if request.POST.get('data_entrega'):
            token.data_entrega = request.POST.get('data_entrega')
        else:
            token.data_entrega = None
        token.observacao = request.POST.get('observacao')
        token.save()
        return redirect('lista_tokens') 
    return render(request, 'token.html', {'token': token, "funcoes": funcoes, "setores": setores})

def atualizar_lista(request):
    """
    View para atualizar a lista de tokens a partir de um arquivo Excel.
    """
    novos_tokens = atualiza_lista_tokens()
    
    for token in novos_tokens.values():
        try:
            token = Token.objects.get(serial=token['nome_responsavel'])
            print(f"Token {token.serial} já existe, não será atualizado.")
        except Token.DoesNotExist:
            new_token = Token(
                nome_responsavel=token['nome_responsavel'],
                cpf_responsavel=token['cpf_responsavel'],
                funcao_responsavel=token['funcao_responsavel'],
                setor_responsavel=token['setor_responsavel'],
                telefone_responsavel=token['telefone_responsavel'],
                serial=token['serial'],
                data_solicitacao=token['data_solicitacao'],
                data_entrega=token['data_entrega'],
                observacao=token['observacao']
            )
            new_token.save()
    
    return redirect('lista_tokens')