from flask import Blueprint, jsonify, request
from services.jsoToken import TokenManager
from services import auth_firebase 
authApi = Blueprint('authApi', __name__)

@authApi.route('/auth/iniciarsesion', methods=['POST'])
def iniciarSesion():
    cedula = request.form.get("cedula")
    password = request.form.get("password")
    respuesta = auth_firebase.iniciar_sesion(cedula, password)
    if respuesta:
        token = TokenManager.generar_token(cedula,respuesta["rol"])
        return jsonify({'status':'succesful','token': token,'informacion': respuesta})
    return jsonify({'status':"Credenciales incorrectas"})

@authApi.route('/auth/validartoken',methods=['POST'])
def validarToken():
    token= request.form.get("token")
    respuesta = TokenManager.validar_token(token)
    if respuesta:
        return jsonify({'status':'succesful','rol':respuesta.get('rol'),'token': token})
    return jsonify({'status':'token no valido'})
