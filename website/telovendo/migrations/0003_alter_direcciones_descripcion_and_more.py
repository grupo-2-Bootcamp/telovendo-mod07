# Generated by Django 4.2.2 on 2023-06-29 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telovendo', '0002_alter_customuser_idempresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direcciones',
            name='descripcion',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='idEmpresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='telovendo.empresas'),
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='idUsuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
