# API de almacenamiento de notas

Esta API fue hecha con Flask y MySQL que permite a los usuarios registrarse, autenticarse, crear y organizar notas por carpetas. Todo ello guardado en una base de datos,

## 📘 Documentación de uso
- ["documentacion de rutas"](/doc/API_REFERENCES.md)
- ["diagramas de secuencias principales"](/doc/DIAGRAMS.md)

## ✅ Funcionalidades
- Registrar usuarios
- Verificar registros por correo
- recuperar contraseña por correo
- Login con JWT
- Eliminacion de cuentas
- obtener contenido de un folder
- crear y editar notas y folders de forma individualmente
- mover y eliminar varias notas y folders a la vez


</br>

**La API viene con 2 vistas simples, una para verificar una cuenta creada y otra para recuperar una contraseña**

<div align="center">
    <img src="./doc/preview_vistas.png" alt="preview de vistas" width="600">
</div>

## 📋 Funcionalidades pendientes
 - Opcion para cambiar el correo asociado a una cuenta
 - Opcion para guardar varias notas y folders a la vez
 - Registro con cuenta google
 - Registro de clave de Github o OpenIA para editar notas con IA
 - Registro de sesiones

## ⚙️ Tecnologías principales
- Python 3.11
- MySQL / MariaDB 10
- Flask 3
- PyJWT
- Flask-Mail
- Flask-MySQLdb
- itsdangerous
- bcrypt

## 🚀 **Instalación y ejecución local** *(Instrucciones hechas en Linux)*
1. Crear entorno virtual
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```


2. Instalar dependencias
    ```bash
    pip install -r requirements.txt
    ```

3. Configurar base de datos y usuario
    ```sql
    CREATE DATABASE IF NOT EXISTS test_db;
    CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
    GRANT ALL PRIVILEGES ON test_db.* TO 'your_user'@'localhost' WITH GRANT OPTION;
    ```
4. Importar configuracion de la base de datos
    ```bash
    mysql -u <your-db-user> -p <your-db-name> < build.sql 
    ```

5. Copiar el archivo .env.example y modificarlo con valores personales

    ```bash
    cp .env.example .env
    ```

    ```bash
    # .env

    #flask config
    FLASK_APP=app:app
    FLASK_DEBUG=1 # 1 = True | 0 = False
    SERVER_NAME="localhost:5000"
    SECRET_KEY=super_secret_password

    #flask mysqldb
    MYSQL_HOST="localhost"
    MYSQL_USER="your_username"
    MYSQL_PASSWORD="your_password"
    MYSQL_DB="db_name"

    #flask mail
    MAIL_USERNAME="user@domain.com"
    MAIL_PASSWORD="email_password"
    SMTP_SERVER ="smtp.domain.com"
    SMTP_PORT=465
    SMTP_USE_SSL=True
    SMTP_USE_TLS=False

    #app config
    APP_NAME="app_name"
    IS_HTTPS=True
    #url de redireccionamiento al finalizar registro de usuario
    LOGIN_URL="http://localhost:5000"
    SALT=email_salt_pe
    PASS_SALT=password-reset-salt
    ```

6. Ejecutar 
    ```bash
    flask run
    ```