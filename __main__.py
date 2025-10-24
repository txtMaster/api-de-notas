from flask import Flask
from .src.db import mysql
from .src.mail import mail
from .src.config import Config

def create_app():
   app = Flask(__name__)

   app.config.from_object(Config)

   from .src.routes.users import users_bp
   from .src.routes.pages import pages_bp
   from .src.routes.folders import folders_bp
   from .src.routes.notes import notes_bp

   app.register_blueprint(users_bp)
   app.register_blueprint(pages_bp)
   app.register_blueprint(folders_bp)
   app.register_blueprint(notes_bp)

   @app.errorhandler(404)
   def no_found(e):
      return "ruta no encontrada",404


   mysql.init_app(app)
   mail.init_app(app)

   return app

if __name__ == "__main__":
   create_app().run()


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