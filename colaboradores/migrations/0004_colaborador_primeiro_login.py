# Generated by Django 4.2.2 on 2023-06-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0003_colaborador_situacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='primeiro_login',
            field=models.BooleanField(default=True),
        ),
    ]
