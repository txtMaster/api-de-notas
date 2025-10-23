from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
class Config():
    DEBUG= os.getenv('DEBUG') == 'True'
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv("MYSQL_DB")
    SECRET_KEY = os.getenv("SECRET_KEY")

print(os.getenv("MYSQL_PASSWORD"))