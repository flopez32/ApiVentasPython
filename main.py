from flask import Flask, jsonify, render_template, request, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,get_jwt_identity
from Conexion import CConexion
from pdf_service import generar_factura

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "clave-super-secreta"
jwt = JWTManager(app)

# ✅ Ruta base
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")



# ✅ GET - Obtener todas las ventas
@app.route("/ventas1", methods=["GET"])
def get_ventas():

    conn = CConexion.ConexionBaseDeDatos()

    if conn is None:
        return {"error": "No hay conexión a la base de datos"}, 500

    cursor = conn.cursor()

    cursor.execute("SELECT Id, Nombre, Producto, Precio, Domicilio FROM Ventas_Mes")

    ventas = []

    for row in cursor.fetchall():
        ventas.append({
            "id": row[0],
            "nombre": row[1],
            "producto": row[2],
            "precio": float(row[3]),
            "domicilio": row[4]
        })

    conn.close()

    return jsonify(ventas)


# ✅ POST - Crear nueva venta
@app.route("/ventas", methods=["POST"])
def create_venta():

    data = request.get_json()

    if not data:
        return {"error": "Debe enviar datos en JSON"}, 400

    try:
        conn = CConexion.ConexionBaseDeDatos()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO Ventas_Mes (Nombre, Producto, Precio, Domicilio) VALUES (?, ?, ?, ?)",
            (data["nombre"], data["producto"], data["precio"], data["domicilio"])
        )

        conn.commit()
        conn.close()

        return {"mensaje": "Venta creada correctamente ✅"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


# ✅ GET - Obtener venta por ID
@app.route("/ventas/<int:id>", methods=["GET"])
def get_venta(id):

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Id, Nombre, Producto, Precio, Domicilio FROM Ventas_Mes WHERE Id = ?",
        id
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "producto": row[2],
            "precio": float(row[3]),
            "domicilio": row[4]
        }
    else:
        return {"error": "Venta no encontrada"}, 404


# ✅ PUT - Actualizar venta
@app.route("/ventas2/<int:id>", methods=["PUT"])
def update_venta(id):

    data = request.get_json()

    if not data:
        return {"error": "Debe enviar datos en JSON"}, 400

    try:
        conn = CConexion.ConexionBaseDeDatos()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Ventas_Mes SET Nombre = ?, Producto = ?, Precio = ?, Domicilio = ? WHERE Id = ?",
            (data["nombre"], data["producto"], data["precio"], data["domicilio"], id)
        )

        conn.commit()
        conn.close()

        return {"mensaje": "Venta actualizada correctamente ✅"}

    except Exception as e:
        return {"error": str(e)}, 500


# ✅ DELETE - Eliminar venta
@app.route("/ventas/<int:id>", methods=["DELETE"])
def delete_venta(id):

    try:
        conn = CConexion.ConexionBaseDeDatos()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Ventas_Mes WHERE Id = ?", id)

        conn.commit()
        conn.close()

        return {"mensaje": "Venta eliminada correctamente ✅"}

    except Exception as e:
        return {"error": str(e)}, 500
    

@app.route('/factura/<int:id>')
def factura(id):
    venta = obtener_venta_por_id(id)

    if not venta:
        return {"error": "Venta no encontrada"}, 404

    ruta = generar_factura(venta)

    return send_file(ruta, as_attachment=True)


# ✅ login - Autenticación de usuario
@app.route("/login", methods=["POST"])
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

def obtener_venta_por_id(id):
    from Conexion import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nombre, producto, precio FROM Ventas_Mes WHERE id = ?", 
        (id,)
    )

    row = cursor.fetchone()

    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "producto": row[2],
            "precio": row[3]
        }

    return None

# ✅ Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)

    



