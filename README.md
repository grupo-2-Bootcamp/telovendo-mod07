# Telovendo Grupo 2 - Modulo 7
Repositorio principal proyecto TeLoVendo Grupo 2 - Modulo 7

## Requisitos

Los requisitos de la aplicación son:

- Django 4.2.2
- asgiref 3.7.2
- psycopg2 2.9.6
- python-dotenv 1.0.0
- setuptools 65.5.0
- sqlparse 0.4.4
- tzdata 2023.3

El programa está configurado para usar PostgreSQL como motor de base de datos

## Instalación

1.  Para instalar el sistema primero cree un entorno virtual mediante el comando

        python -m venv .venv

2.  Después, active el entorno virtual

        .venv\scripts\activate

3.  Clone el proyecto usando el archivo ZIP en

        https://github.com/grupo-2-Bootcamp/telovendo-mod07/archive/refs/heads/main.zip

    Y descomprima el archivo **en el mismo directorio** donde se encuentra el directorio .venv.
    También puede clonar el proyecto usando git, con las indicaciones señaladas anteriormente.

4.  y utilice el siguiente comando para instalar los requisitos de sistema:

        (.venv) píp install -r requeriments.txt

5.  Cree un archivo .env en el directorio raíz del sistema y proporcione los datos para acceder a una base de datos de PostgreSQL:

        SECRET_KEY= 'Secret_key'            # secret_key de Django
        DB_ENGINE= 'django.db.backends.postgresql_psycopg2'
        DB_DATABASE= 'database'             # Nombre de la base de datos
        DB_USER= 'user'                     # Usuario de la base de datos
        DB_PASSWORD= 'password'             # Contraseña del usuario 
        DB_HOST= 'host'                     # Dirección del servidor PostgreSQL 
        DB_PORT= '5432'                     # Puerto del servidor PostgreSQL, habitualmente 5432
        
        EMAIL_HOST = 'mailserver'           # Nombre del servidor SMTP
        EMAIL_PORT = 'hostport'             # Puerto del servidor
        EMAIL_USE_TLS = False               # Si el servidor usa TLS o no
        EMAIL_USE_SSL = False               # Si el servidor usa SSL o no
        EMAIL_HOST_USER = 'user'            # Usuario
        EMAIL_HOST_PASSWORD = 'password'    # Contraseña del usuario de correo

6.  Finalmente para ejecutar el proyecto utilice el comando
        (.venv) python manage.py runserver

## Estructura de directorios principales

Los directorios principales de Django son:

- website: Contiene las configuraciones principales, rutas, vistas
- mainsite: Contiene las paginas públicas del sitio web y sus archivos estáticos y plantillas
- telovendo: Contiene la aplicación interna para usuarios, modelos y relacionados

También existe una carpeta adicional **docs** que contiene otros archivos de documentación de la aplicación.

## Usuarios

Los usuarios se encuentran en el archivo usuarios.md