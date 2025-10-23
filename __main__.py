from flask import Flask, jsonify, redirect, url_for
from flask import render_template,request
from flask_mysqldb import MySQL
from .src.db import mysql

from .src.models.User import User
from .src.config import Config

def queryinfo():
   print(request)
   print(request.args)
   print(request.args.get("name"))
   return "OK"

def create_app():
   app = Flask(__name__)

   from .src.routes.users import users_bp
   from .src.routes.pages import pages_bp
   from .src.routes.folders import folders_bp
   from .src.routes.notes import notes_bp

   app.add_url_rule("/queryinfo",view_func=queryinfo)
   app.register_blueprint(users_bp)
   app.register_blueprint(pages_bp)
   app.register_blueprint(folders_bp)
   app.register_blueprint(notes_bp)

   @app.errorhandler(404)
   def no_found(e):
      #return redirect(url_for("index"))
      #return render_template("error.html"),404
      return "ruta no encontrada",404

   app.config.from_object(Config)

   mysql.init_app(app)

   return app

#@app.before_request
#def bef_request():
#   print("antes de la peticion")
#
#@app.after_request
#def aft_request(response):
#   print("despues de la peticion")
#   return response

if __name__ == "__main__":
   create_app().run()