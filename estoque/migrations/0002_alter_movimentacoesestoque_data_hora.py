# Generated by Django 4.2.2 on 2023-07-17 16:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesestoque',
            name='data_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]