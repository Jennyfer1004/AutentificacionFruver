import firebase_admin
from firebase_admin import credentials, firestore
import hashlib

# Inicializa la aplicación con la clave privada
jsonFirebase= 'firebasetoken.json'
try:
    cred = credentials.Certificate("services/"+jsonFirebase)
except:
    print("no olvides agregar el archivo firebasetoken.json, pero ojo no se le puede hacer commit al archivo")

firebase_admin.initialize_app(cred)
db = firestore.client()

# Función para hashear contraseñas
def hashear_contraseña(contraseña):
    return hashlib.sha256(contraseña.encode()).hexdigest()


def crear_usuario(cedula, nombre, contraseña, correo, telefono, rol):
    # validar que cedula,correo y telefono no existan
    usuarios = db.collection('usuarios').where(filter=('cedula', '==', cedula)).get()
    if usuarios:
        return({'status':'no creado','mensaje':'La cedula ya está en uso.'})
    
    usuarios = db.collection('usuarios').where(filter=('correo', '==', correo)).get()
    if usuarios:
        return({'status':'no creado','mensaje':'El correo ya está en uso.'})
    
    usuarios = db.collection('usuarios').where(filter=('telefono', '==', telefono)).get()
    if usuarios:
        return({'status':'no creado','mensaje':'El teléfono ya está en uso.'})
    
    # Crea el usuario
    db.collection('usuarios').document(cedula).set({
        'cedula': cedula,
        'nombre': nombre,
        'password': hashear_contraseña(contraseña),
        'correo': correo,
        'telefono': telefono,
        'rol': rol
    })
    return({'status':'succesful','mensaje':'usuario creado correctamente'})

# Función para iniciar sesión
def iniciar_sesion(cedula, contraseña):
    usuario_ref = db.collection('usuarios').document(cedula).get()
    
    if usuario_ref.exists:
        usuario = usuario_ref.to_dict()
        if usuario['password'] == hashear_contraseña(contraseña):
            return usuario
    return False

# Función para modificar un usuario
def modificar_usuario(cedula, nuevo_nombre, nuevo_correo, nuevo_telefono):
    usuario_ref = db.collection('usuarios').document(cedula).get()
    
    if not usuario_ref.exists:
        return ({'status':'no modificado','mensaje':'usuario no existe'})
    
    # Actualiza el nombre
    if nuevo_nombre:
        db.collection('usuarios').document(cedula).update({'nombre': nuevo_nombre})

    # Verifica y actualiza el correo
    if nuevo_correo:
        usuarios = db.collection('usuarios').where(filter=('correo', '==', nuevo_correo)).get()
        if usuarios:
            return ({'status':'no modificado','mensaje':'El correo ya está en uso.'})
        db.collection('usuarios').document(cedula).update({'correo': nuevo_correo})

    # Verifica y actualiza el teléfono
    if nuevo_telefono:
        usuarios = db.collection('usuarios').where(filter=('telefono', '==', nuevo_telefono)).get()
        if usuarios:
            return ({'status':'no modificado','mensaje':'El teléfono ya está en uso.'})
        db.collection('usuarios').document(cedula).update({'telefono': nuevo_telefono})
    return({'status':'succesful','mensaje':'usuario modificado correctamente'})

# Función para eliminar un usuario
def eliminar_empleado(cedula):
    usuario_ref = db.collection('usuarios').document(cedula).get()
    if usuario_ref.exists:
        db.collection('usuarios').document(cedula).delete()
        return {'status': 'succesful', 'mensaje': 'usuario eliminado correctamente'}
    return {'status': 'no eliminado', 'mensaje': 'usuario no existe'}

# Función para consultar todos los empleados
def consultar_empleados():
    empleados = db.collection('usuarios').where('rol', '==', 'empleado').get()
    lista_empleados = [
        {k: v for k, v in empleado.to_dict().items() if k != 'password'}
        for empleado in empleados
    ]
    return lista_empleados if lista_empleados else {'status': 'no hay empleados', 'mensaje': 'usuario no existe'}

# Función para consultar un empleado por su nombre
def consultar_empleado_nombre(nombre_parcial):
    empleados = db.collection('usuarios')\
                  .where('rol', '==', 'empleado')\
                  .order_by('nombre')\
                  .start_at([nombre_parcial])\
                  .end_at([nombre_parcial + '\uf8ff'])\
                  .get()
    lista_empleados = [
        {k: v for k, v in empleado.to_dict().items() if k != 'password'}
        for empleado in empleados
    ]
    return lista_empleados if lista_empleados else {'status': 'error', 'mensaje': f'No se encontraron empleados con un nombre parecido a {nombre_parcial}'}

# Función para consultar un empleado por su cédula
def consultar_empleado_cedula(cedula):
    empleados = db.collection('usuarios').where('cedula', '==', cedula).where('rol', '==', 'empleado').get()
    lista_empleados = [
        {k: v for k, v in empleado.to_dict().items() if k != 'password'}
        for empleado in empleados
    ]
    return lista_empleados if lista_empleados else {'status': 'error', 'mensaje': f'No se encontró un empleado con la cédula {cedula}'}

# NO OLVIDEN PRIMERO CREAR SUS ADMINISTRADORES EN FIREBASE #
#crear_usuario('1004926901', 'Jennyfer Natalia Garcia', 'jennyfer', 'jennyfer@example.com', '+57 542554344', 'administrador')
