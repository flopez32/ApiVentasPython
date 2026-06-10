
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.db.conexion import CConexion

auth_bp = Blueprint('auth', __name__)



# ✅ login - Autenticación de usuario
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Username, Rol FROM Usuarios WHERE Username = ? AND Password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        token = create_access_token(identity={
            "username": user[0],
            "rol": user[1]
        })

        return {
            "mensaje": "Login exitoso ✅",
            "token": token
        }

    return {"error": "Credenciales incorrectas ❌"}, 401


