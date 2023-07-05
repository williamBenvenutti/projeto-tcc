from django.db import models
from colaboradores.models import Colaborador
from produtos.models import Produto

class RegistroCompra(models.Model):
    colab_id = models.ForeignKey(Colaborador, on_delete=models.PROTECT)
    produtos = models.ManyToManyField(Produto, through='ItemCompra')
    data_compra = models.DateTimeField()

    def __str__(self):
        return self.colab_id.nome
    
class ItemCompra(models.Model):
    compra = models.ForeignKey(RegistroCompra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_individual = models.FloatField()

    def __str__(self):
        return self.produto.nome

