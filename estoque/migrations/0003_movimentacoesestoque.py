# Generated by Django 4.2.2 on 2023-07-11 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_alter_estoque_nome_produto'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimentacoesEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('saida', 'Saida')], max_length=20)),
                ('nome_produto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='estoque.estoque')),
            ],
        ),
    ]