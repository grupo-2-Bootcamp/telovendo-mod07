# Generated by Django 4.2.2 on 2023-06-26 22:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.CharField(max_length=10)),
                ('nombre_empresa', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estado_Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
                ('stock', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('urlfoto', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=30)),
                ('group', models.CharField(max_length=45, null=True)),
                ('idEmpresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telovendo.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(default=django.utils.timezone.now)),
                ('idDireccion', models.IntegerField()),
                ('total_pedido', models.IntegerField()),
                ('idEmpresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telovendo.empresas')),
                ('idEstado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telovendo.estado_pedido')),
                ('idMetodoPago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telovendo.metodopago')),
                ('idUsuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telovendo.users')),
            ],
        ),
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=45)),
                ('numero', models.IntegerField()),
                ('Comuna', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45, null=True)),
                ('idEmpresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telovendo.empresas')),
            ],
        ),
        migrations.CreateModel(
            name='Detalles_Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('precio', models.IntegerField()),
                ('idPedidos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telovendo.pedidos')),
                ('idProductos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telovendo.productos')),
            ],
        ),
    ]
