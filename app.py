from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

#Configuracion MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'host'
app.config['MYSQL_PASSWORD']  = 'admin'
app.config['MYSQL_DB'] = 'basta&punto'

@app.route('/')
def index():
     data = {
          'titulo' : 'Inicio' 
     }
     return render_template('index.html', data = data)

@app.route('/cursos')
def cursos():
     data = {
          'titulo' : 'Cursos'
     }
     return render_template('cursos.html', data = data)

if __name__ == '__main__':
     app.run(debug=True)