from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Token
# Create your views here.

def home(request):
    return render(request, 'home.html')

def lista_tokens(request):
    tokens = Token.objects.all()
    # print(tokens)
    return render(request, 'lista_tokens.html', {'tokens': tokens})