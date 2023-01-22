import pyotp #generates para contraseñas de un solo uso.
import sqlite3 #database para nombre de usuario/contraseñas
import hashlib #secure para hashes y resumenes de mensajes
import uuid #for para crear identificadores universales unicos de la importación del flask, solicitar
from flask import Flask, Request

app = Flask(__name__) #Asegurese de usar dos guiones bajos antes y despuesde «nombre»
db_name = 'test.db'

@app.route('/')
def index():
    return 'Bienvenido al laboratorio práctico para una evolución de los sistemas de contraseñas!'

########################################### Texto sin formato 
###########################################################
@app.route('/signup/v1', methods=['POST'])
def signup_v1(): 
    conn = sqlite3.connect (db_name)
    c = conn.cursor() 
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN(USERNAME TEXT PRIMARY KEY NOT NULL,PASSWORD TEXT NOT NULL);''')
    conn.commit ()
    
    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME,PASSWORD) ""VALUES ('{0}', '{1}')".format(Request.form['username'], 
        Request.form['password']))
        conn.commit () 
    
    except sqlite3.IntegrityError:
        return "el usuario ha sido registrado"
    
    print ('username: ', Request.form['username'], ' password: ' , Request.form ['password'])
    
    return "registro exitoso"
########################################################################################################
def verify_plain(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password
#######################################################################################################
@app.route('/login/v1', methods=['GET', 'POST'])
def login_v1():
    error = None
    if Request.method == 'POST':
        if verify_plain(Request.form['username'], Request.form['password']):
            error = 'inicio de sesión exitoso'
        else:
            error = 'Usuario/contraseña inválidos'

    else:
        error = 'Método no válido'
    return error
#######################################################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
