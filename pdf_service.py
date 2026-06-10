from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generar_factura(venta):
    # Crear carpeta facturas si no existe
    carpeta = "static/facturas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    nombre_archivo = f"factura_{venta['id']}.pdf"
    ruta = os.path.join(carpeta, nombre_archivo)

    c = canvas.Canvas(ruta, pagesize=letter)

    c.setFont("Helvetica", 12)

    # Título
    c.drawString(200, 750, "FACTURA DE VENTA")

    # Datos de la venta
    c.drawString(100, 700, f"ID: {venta['id']}")
    c.drawString(100, 680, f"Cliente: {venta['nombre']}")
    c.drawString(100, 660, f"Producto: {venta['producto']}")
    c.drawString(100, 640, f"Precio: ${venta['precio']}")

    c.drawString(100, 600, "Gracias por su compra")

    c.save()

    return ruta
