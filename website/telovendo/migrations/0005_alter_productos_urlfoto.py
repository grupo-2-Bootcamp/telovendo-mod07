# Generated by Django 4.2.2 on 2023-07-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telovendo', '0004_alter_detalles_pedido_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='urlfoto',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]
