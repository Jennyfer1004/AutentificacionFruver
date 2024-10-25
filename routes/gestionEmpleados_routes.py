from flask import Blueprint, jsonify, request
from services.jsoToken import TokenManager
from services import auth_firebase 
gestionEmpleados = Blueprint('gestionEmpleados', __name__)

@gestionEmpleados.route('/gestion/crearempleado', methods=['POST'])
def crearEmpleado():
    cedula = request.form.get("cedula")
    nombre = request.form.get("nombre")
    password = request.form.get("password")
    correo = request.form.get("correo")
    telefono = request.form.get("telefono")
    token = request.form.get("token")
    if(token == None):
        return jsonify({'status':'no se proporciono un token'})
    respuestaToken = TokenManager.validar_token(token)
    if respuestaToken:
        if respuestaToken.get('rol') == "administrador":
            respuesta = auth_firebase.crear_usuario(cedula, nombre, password,correo, telefono,"empleado")
            return jsonify(respuesta)
        else:
            return jsonify({'status':'no eres rol administrador'})
    return jsonify({'status':'token no valido'})

@gestionEmpleados.route('/gestion/eliminarempleado', methods=['POST'])
def eliminarEmpleado():
    cedula = request.form.get("cedula")
    token = request.form.get("token")
    if(token == None):
        return jsonify({'status':'no se proporciono un token'})
    respuestaToken = TokenManager.validar_token(token)
    if respuestaToken:
        if respuestaToken.get('rol') == "administrador":
            respuesta = auth_firebase.eliminar_empleado(cedula)
            return jsonify(respuesta)
        else:
            return jsonify({'status':'no eres rol administrador'})
    return jsonify({'status':'token no valido'})

@gestionEmpleados.route('/gestion/consultarempleados', methods=['POST'])
def consultarEmpleados():
    token = request.form.get("token")
    if(token == None):
        return jsonify({'status':'no se proporciono un token'})
    respuestaToken = TokenManager.validar_token(token)
    if respuestaToken:
        if respuestaToken.get('rol') == "administrador":
            return jsonify(auth_firebase.consultar_empleados())
        else:
            return jsonify({'status':'no eres rol administrador'})
    return jsonify({'status':'token no valido'})

@gestionEmpleados.route('/gestion/modificarempleado', methods=['POST'])
def modificarEmpleado():
    token = request.form.get("token")
    cedula = request.form.get("cedula")
    nuevo_nombre = request.form.get("nuevo_nombre")
    nuevo_correo = request.form.get("nuevo_correo")
    nuevo_telefono = request.form.get("nuevo_telefono")
    if(token == None):
        return jsonify({'status':'no se proporciono un token'})
    if(cedula == None):
        return jsonify({'status':'no se proporciono una cedula'})
    respuestaToken = TokenManager.validar_token(token)
    if respuestaToken:
        if respuestaToken.get('rol') == "administrador":
            respuesta = auth_firebase.modificar_usuario(cedula,nuevo_nombre,nuevo_correo,nuevo_telefono)
            return jsonify(respuesta)
        else:
            return jsonify({'status':'no eres rol administrador'})
    return jsonify({'status':'token no valido'})