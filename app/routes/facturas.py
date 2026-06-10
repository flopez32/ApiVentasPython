
from flask import Blueprint, send_file
from app.services.pdf_service import generar_factura
from app.db.conexion import CConexion, get_connection

factura_bp = Blueprint('factura', __name__)


def obtener_venta_por_id(id):
    

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


@factura_bp.route('/factura/<int:id>')
def factura(id):

    venta = obtener_venta_por_id(id)

    if not venta:
        return {"error": "Venta no encontrada"}, 404

    ruta = generar_factura(venta)

    return send_file(ruta, as_attachment=True)
