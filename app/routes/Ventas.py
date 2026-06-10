from flask import Blueprint, request, jsonify
from app.db.conexion import CConexion

ventas_bp = Blueprint('ventas', __name__)

# ✅ GET - Obtener todas las ventas
@ventas_bp.route("/ventas1", methods=["GET"])
def get_ventas():

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute("""SELECT TOP 10 Id, Nombre, Producto, Precio, Domicilio FROM Ventas_Mes ORDER BY Id DESC""")

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
@ventas_bp.route("/ventas", methods=["POST"])
def create_venta():

    data = request.get_json()

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Ventas_Mes (Nombre, Producto, Precio, Domicilio) VALUES (?, ?, ?, ?)",
        (data["nombre"], data["producto"], data["precio"], data["domicilio"])
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Venta creada correctamente ✅"}


# ✅ GET - Obtener venta por ID
@ventas_bp.route("/ventas/<int:id>", methods=["GET"])
def get_venta(id):

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT Id, Nombre, Producto, Precio, Domicilio FROM Ventas_Mes WHERE Id = ?",
        (id,)
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

    return {"error": "Venta no encontrada"}, 404


# ✅ PUT - Actualizar venta
@ventas_bp.route("/ventas2/<int:id>", methods=["PUT"])
def update_venta(id):

    data = request.get_json()

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Ventas_Mes SET Nombre = ?, Producto = ?, Precio = ?, Domicilio = ? WHERE Id = ?",
        (data["nombre"], data["producto"], data["precio"], data["domicilio"], id)
    )

    conn.commit()
    conn.close()

    return {"mensaje": "Venta actualizada correctamente ✅"}


# ✅ DELETE - Eliminar venta
@ventas_bp.route("/ventas/<int:id>", methods=["DELETE"])
def delete_venta(id):

    conn = CConexion.ConexionBaseDeDatos()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Ventas_Mes WHERE Id = ?", (id,))

    conn.commit()
    conn.close()

    return {"mensaje": "Venta eliminada correctamente ✅"} 