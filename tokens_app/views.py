from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Token, funcoes
import openpyxl as xl
from .atualiza_lista import atualiza_lista_tokens
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout

User = get_user_model()

def home(request):
    
    return render(request, 'home.html')

def lista_tokens(request):
    # print(request.user)
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        tokens = Token.objects.all()
        return render(request, 'lista_tokens.html', {'tokens': tokens})

def novo_token(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            nome_responsavel = request.POST.get('nome_responsavel')
            cpf_responsavel = request.POST.get('cpf_responsavel')
            funcao_responsavel = request.POST.get('funcao_responsavel')
            # setor_responsavel = request.POST.get('setor_responsavel')
            # telefone_responsavel = request.POST.get('telefone_responsavel')
            serial = request.POST.get('serial')
            data_solicitacao = request.POST.get('data_solicitacao') or None
            data_entrega = request.POST.get('data_entrega') or None
            observacao = request.POST.get('observacao')

            token = Token(
                nome_responsavel=nome_responsavel,
                cpf_responsavel=cpf_responsavel,
                funcao_responsavel=funcao_responsavel,
                # setor_responsavel=setor_responsavel,
                # telefone_responsavel=telefone_responsavel,
                serial=serial,
                data_solicitacao=data_solicitacao,
                data_entrega=data_entrega,
                observacao=observacao
            )
            try:
                Token.objects.get(nome_responsavel=nome_responsavel) or Token.objects.get(serial=serial) or Token.objects.get(cpf_responsavel=cpf_responsavel)
                return HttpResponse("Token já cadastrado com este nome, CPF ou serial.")
            except Token.DoesNotExist:
                token.save()
            return render(request, 'lista_tokens.html', {'tokens': Token.objects.all(), "sucesso": "Token cadastrado com sucesso!"})

        return render(request, 'novo_token.html', {"funcoes": funcoes})

def atualizar_token(request, token_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        # return HttpResponse("This view is not implemented yet.")
        token = Token.objects.get(id=token_id)
        if request.method == 'POST':
            token.nome_responsavel = request.POST.get('nome_responsavel')
            token.cpf_responsavel = request.POST.get('cpf_responsavel')
            token.funcao_responsavel = request.POST.get('funcao_responsavel')
            # token.setor_responsavel = request.POST.get('setor_responsavel')
            # token.telefone_responsavel = request.POST.get('telefone_responsavel')
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
            return render(request, 'lista_tokens.html', {'tokens': Token.objects.all(), "sucesso": "Token atualizado com sucesso!"})
        return render(request, 'token.html', {'token': token, "funcoes": funcoes})

def atualizar_lista(request):
    """
    View para atualizar a lista de tokens a partir de um arquivo Excel.
    """
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        novos_tokens = atualiza_lista_tokens()
        
        for token in novos_tokens.values():
            
            try:
                has_token, created = Token.objects.update_or_create(
                nome_responsavel=token['nome_responsavel'],
                defaults={
                    'cpf_responsavel': token['cpf_responsavel'],
                    'funcao_responsavel': token['funcao_responsavel'],
                    'serial': token['serial'],
                    'data_solicitacao': token['data_solicitacao'],
                    'data_entrega': token['data_entrega'],
                    'observacao': token['observacao']
                }
            )
                if created:
                    print(f"Token {has_token.nome_responsavel} criado com sucesso!")
                else:
                    print(f"Token {has_token.nome_responsavel} já existe. Atualizado!")
                # Se quiser atualizar o token existente, descomente as linhas abaixo
                # has_token = Token.objects.get(nome_responsavel=has_token['nome_responsavel'])
                # has_token.cpf_responsavel = token['cpf_responsavel']
                # has_token.funcao_responsavel = token['funcao_responsavel']
                # has_token.serial = token['serial']
                # has_token.data_solicitacao = token['data_solicitacao']
                # has_token.data_entrega = token['data_entrega']
                # has_token.observacao = token['observacao']
                # has_token.save()
                # Token.objects.aupdate_or_create()
                # print(f"Token {has_token.serial} já existe. Atualizado!.")

            except Token.MultipleObjectsReturned:
                print(f"Erro: Múltiplos tokens encontrados para {has_token.nome_responsavel}. Verifique os dados.")

            # except Token.DoesNotExist:
            #     new_token = Token(
            #         nome_responsavel=token['nome_responsavel'],
            #         cpf_responsavel=token['cpf_responsavel'],
            #         funcao_responsavel=token['funcao_responsavel'],
            #         # setor_responsavel=token['setor_responsavel'],
            #         # telefone_responsavel=token['telefone_responsavel'],
            #         serial=token['serial'],
            #         data_solicitacao=token['data_solicitacao'],
            #         data_entrega=token['data_entrega'],
            #         observacao=token['observacao']
            #     )
            #     new_token.save()
        
        return redirect('lista_tokens')

def admin(request):
    return redirect('/admin')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')