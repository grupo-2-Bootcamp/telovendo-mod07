# Generated by Django 4.2.2 on 2023-07-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telovendo', '0005_alter_productos_urlfoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidos',
            name='total_pedido',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]