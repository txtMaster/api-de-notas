import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from src.config import Config

from src.db import mysql
from src.mail import mail

from src.routes.users import users_bp
from src.routes.pages import pages_bp
from src.routes.folders import folders_bp
from src.routes.notes import notes_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app,origins=[Config.FRONTEND_URL], supports_credentials=True)

app.register_blueprint(users_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(folders_bp)
app.register_blueprint(notes_bp)

@app.errorhandler(404)
def no_found(e):
   return "ruta no encontrada",404


mysql.init_app(app)
mail.init_app(app)
   


#@app.before_request
#def bef_request():
#   print("antes de la peticion")
#
#@app.after_request
#def aft_request(response):
#   print("despues de la peticion")
#   return response


#return redirect(url_for("index"))
#return render_template("error.html"),404