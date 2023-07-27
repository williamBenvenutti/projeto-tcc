from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    login = models.CharField(max_length=20, unique=True)
    senha = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, null=True, unique=True)
    situacao = models.BooleanField(default=True)
    codigo_de_barras = models.CharField(max_length=20, default='1')
    primeiro_login = models.BooleanField(default=True)

    def __str__(self):
        return self.nome