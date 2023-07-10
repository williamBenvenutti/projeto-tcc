from django.db import models
from produtos.models import Produto
class Estoque(models.Model):
    nome_produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome_produto.nome