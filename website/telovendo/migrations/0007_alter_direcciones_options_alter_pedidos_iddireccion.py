# Generated by Django 4.2.2 on 2023-06-27 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telovendo', '0006_rename_run_empresas_rut_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direcciones',
            options={'verbose_name': 'Dirección', 'verbose_name_plural': 'Direcciones'},
        ),
        migrations.AlterField(
            model_name='pedidos',
            name='idDireccion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='telovendo.direcciones'),
        ),
    ]
