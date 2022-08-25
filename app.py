import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app = Flask(__name__)
app.secret_key="MisionTIC"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='sql651.main-hosting.eu'
app.config['MYSQL_DATABASE_USER']='u986885080_otravexxx'
app.config['MYSQL_DATABASE_PASSWORD']='GVfC7N^q6XKN'
app.config['MYSQL_DATABASE_DB']='u986885080_otravex'
mysql.init_app(app)
 

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/img/'),imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/css/'),archivocss)

@app.route('/libros')
def libros():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    return render_template('libros.html', libros=libros)

@app.route('/admin/crearcliente')
def crearcliente():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`")
    cliente=cursor.fetchall()
    conexion.commit()
    return render_template('admin/crearcliente.html', cliente=cliente)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login',methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']

    if _usuario=="admin" and _password=="123":
        session['login']=True
        session['usuario']="Administrador"
        return redirect('/admin')
    return render_template('admin/login.html',mensaje="Aqui no entran feas")

@app.route('/admin/cerrar')
def admin_login_clear():
    session.clear()
    return redirect('/')

@app.route('/admin/libros')
def admin_libros():

    if not 'login' in session:
        return redirect("/admin/login")

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    libros=cursor.fetchall()
    conexion.commit()
    return render_template('admin/libros.html',libros=libros)

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    if not 'login' in session:
        return redirect("/admin/login")
    _nombre=request.form['txtNombre']
    _url=request.form['txtURL']
    _archivo=request.files['txtImagen']

    tiempo= datetime.now()
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/img/"+nuevoNombre)

    sql ="INSERT INTO `libros` (`ID`, `NOMBRE`, `IMAGEN`, `URL`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,nuevoNombre,_url)
    
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])    
def admin_libros_borrar():
    if not 'login' in session:
        return redirect("/admin/login")
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM libros WHERE id=%s",(_id))
    libro=cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/img/"+str(libro[0][0])):
        os.unlink("templates/img/"+str(libro[0][0]))

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM libros WHERE id=%s",(_id))
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)
    return redirect('/admin/libros')


if __name__ =='__main__':
    app.run(debug=True)





