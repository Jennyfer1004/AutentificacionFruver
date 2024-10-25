from flask import Flask
from routes import auth_routes
from routes import gestionEmpleados_routes
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
if __name__ == '__main__':
    app.register_blueprint(auth_routes.authApi, url_prefix = '/')
    app.register_blueprint(gestionEmpleados_routes.gestionEmpleados, url_prefix = '/')   
    app.config.from_object('config.Config')
    app.run(port=8080,debug=True)