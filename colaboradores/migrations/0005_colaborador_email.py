# Generated by Django 4.2.2 on 2023-07-04 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0004_colaborador_primeiro_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='email',
            field=models.EmailField(max_length=100, null=True, unique=True),
        ),
    ]
