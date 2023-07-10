from django.db import models

class Produto(models.Model):

    CATEGORIA_CHOICES = (
        ('alimento', 'Alimento'),
        ('vestuario', 'Vestuário'),
        ('cinema', 'Ingresso'),
    )

    nome = models.CharField(max_length=100)
    codigo_de_barras = models.CharField(max_length=20, unique=True)
    preco = models.FloatField()
    situacao = models.BooleanField(default=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)


    def __str__(self):
        return self.nome