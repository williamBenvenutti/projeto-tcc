from django.db import models
from produtos.models import Produto
from django.utils import timezone

class Estoque(models.Model):
    nome_produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome_produto.nome

class MovimentacoesEstoque(models.Model):
    
    TIPOS_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saida'),
    )

    usuario = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)
    data_hora = models.DateTimeField(default=timezone.now)
    nome_produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
