from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo_de_barras = models.CharField(max_length=20, unique=True)
    preco = models.FloatField()

    def __str__(self):
        return self.nome