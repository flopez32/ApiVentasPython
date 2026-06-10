from flask import Flask, jsonify, render_template, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from app.db.conexion import CConexion
from app.routes.Ventas import ventas_bp
from app.routes.facturas import factura_bp
from app.routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(factura_bp)
app.register_blueprint(ventas_bp)
app.config["JWT_SECRET_KEY"] = "clave-super-secreta"
jwt = JWTManager(app)

# ✅ Ruta base
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")





# ✅ Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)



    
