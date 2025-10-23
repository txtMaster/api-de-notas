from flask import Blueprint, render_template

pages_bp = Blueprint("pages",__name__)

@pages_bp.route('/')
def index():
    cursos = ["PHP","JAVA","Python"]
    data = {
       "title":"Index",
       "welcome_message":"!HOLAA!",
       "cursos":cursos,
       "len_cursos":len(cursos)
    ,}
    return render_template("index.html",data=data)

@pages_bp.route("/contact/<name>/<int:age>")
def contact(name,age):
   data={
      "title": "Contacto",
      "name":name,
      "age":age
   }
   return render_template("contact.html",data=data)
