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

Para instalar el sistema primero cree un entorno virtual mediante el comando:

    python -m venv .venv

Después, active el entorno virtual y clone el proyecto usando git. Después de clonar el proyecto utilice el siguiente comando para instalar los requisitos de sistema:

    (.venv) píp install -r requeriments.txt

Finalmente cree un archivo .env en el directorio raíz del sistema:

    SECRET_KEY= 'Secret_key'     # secret_key de Django
    DB_ENGINE= 'django.db.backends.postgresql_psycopg2'
    DB_DATABASE= 'database'      # Nombre de la base de datos
    DB_USER= 'user'              # Usuario de la base de datos
    DB_PASSWORD= 'password'      # Contraseña del usuario 
    DB_HOST= 'host'              # Dirección del servidor PostgreSQL 
    DB_PORT= '5432'              # Puerto del servidor PostgreSQL, habitualmente 5432

## Estructura de directorios principales

Los directorios principales de Django son:

- website: Contiene las configuraciones principales, rutas, vistas
- mainsite: Contiene las paginas públicas del sitio web y sus archivos estáticos y plantillas
- telovendo: Contiene la aplicación interna para usuarios, modelos y relacionados

También existe una carpeta adicional **docs** que contiene otros archivos de documentación de la aplicación.