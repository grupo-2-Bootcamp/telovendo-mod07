# Generated by Django 4.2.2 on 2023-06-29 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telovendo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='idEmpresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='telovendo.empresas'),
        ),
    ]