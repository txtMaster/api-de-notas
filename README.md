# API de almacenamiento de notas

## 📘 Descripción general
Esta API permite a los usuarios autenticarse, crear, leer, actualizar y eliminar notas personales en la nube.

Está desarrollada con Flask y MySQL.

## ⚙️ Tecnologías principales

- Python 3.11
- Flask 3
- Flask-JWT-Extended
- Flask-Mail
- Flask-MySQLdb
- itsdangerous
- bcrypt

## 🚀 Instalación y ejecución local
1. Crear entorno virtual
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```


2. Instalar dependencias
    ```bash
    pip install -r requirements.txt
    ```

3. Copiar el archivo .env.example y modificarlo con valores personales

    ```bash
    cp .env.example .env
    ```

    ```bash
    # .env

    APP_NAME="app name"
    IS_HTTPS=True
    # direccion del servidor
    SERVER_NAME="localhost:5000"
    # direccion frontend a donde se redirige al usuario al crear una cuenta
    LOGIN_URL="http://localhost:5000"

    FLASK_APP=app.py

    SECRET_KEY=my_super_secret_pass
    SALT=salt_by_register_process
    PASS_SALT=salt_by_recover_process

    DEBUG=True
    MYSQL_HOST = "localhost"
    MYSQL_USER = "user_db_name"
    MYSQL_PASSWORD = "user_pass"
    MYSQL_DB = "db_name"

    MAIL_USERNAME="user@mail.org"
    MAIL_PASSWORD="ur-fake-password"
    SMTP_SERVER ="smtp-fake.server.org"
    SMTP_PORT = 465
    SMTP_USE_SSL=True
    SMTP_USE_TLS=False

    ```

4. Ejecutar 
    ```bash
    python app.py
    ```


# Ejecutar servidor
flask run


Descripción general de la API (qué hace, para quién es)

Tecnologías usadas (Flask, SQLAlchemy, JWT, etc.)

Requisitos de instalación

Cómo ejecutar el servidor localmente

Ejemplos de uso (curl o Postman)

Estructura de carpetas