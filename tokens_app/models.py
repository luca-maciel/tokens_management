from django.db import models

# Create your models here.

class Token(models.Model):
    nome_responsavel = models.CharField(max_length=125)
    cpf_responsavel = models.CharField(max_length=11)
    funcao_responsavel = models.CharField(max_length=125)
    setor_responsavel = models.CharField(max_length=125)
    telefone_responsavel = models.CharField(max_length=15)
    serial = models.CharField(max_length=14)
    data_solicitacao = models.DateField()
    data_entrega = models.DateField(blank=True, null=True)
    data_modificacao = models.DateField(auto_now=True)
    observacao = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.nome_responsavel}"
    
