from dotenv import load_dotenv
import os

load_dotenv()
class Config():
    APP_NAME = os.getenv("APP_NAME")
    IS_HTTPS:bool = os.getenv("IS_HTTTPS") == "True"
    SERVER_NAME = os.getenv("SERVER_NAME")

    DEBUG:bool = os.getenv('DEBUG') == 'True'
    FLASK_APP= os.getenv("FLASK_APP")
    FLASK_DEBUG= os.getenv("FLASK_DEBUG")

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv("MYSQL_DB")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SALT = os.getenv("SALT")
    PASS_SALT = os.getenv("PASS_SALT")

    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_PORT = int(os.getenv("SMTP_PORT"))
    MAIL_USE_TLS:bool = os.getenv("SMTP_USE_TLS") == "True"
    MAIL_USE_SSL:bool = os.getenv("SMTP_USE_SSL") == "True"
    MAIL_SERVER = os.getenv("SMTP_SERVER")
    MAIL_DEFAULT_SENDER = (APP_NAME,MAIL_USERNAME)

    LOGIN_URL = os.getenv("LOGIN_URL")