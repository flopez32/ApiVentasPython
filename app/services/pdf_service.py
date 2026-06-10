from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generar_factura(venta):

    carpeta = "static/facturas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    ruta = os.path.join(carpeta, f"factura_{venta['id']}.pdf")

    c = canvas.Canvas(ruta, pagesize=letter)

    # ✅ LOGO
    c.drawImage("static/logo3.png", 240, 700, width=80, height=60)

    # ✅ FECHA
    hoy = datetime.now()

    # ✅ TABLA ORDEN
    datos_orden = [
        [f"ORDEN DE COMPRA N° {venta['id']}"],
        ["DÍA", "MES", "AÑO"],
        [hoy.strftime("%d"), hoy.strftime("%m"), hoy.strftime("%Y")]
    ]

    tabla_orden = Table(datos_orden, colWidths=[200, 100, 100])
    tabla_orden.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER")
    ]))

    tabla_orden.wrapOn(c, 50, 620)
    tabla_orden.drawOn(c, 50, 620)

    # ✅ TITULO
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 580, "LECHONERIA BUCANEROS")

    c.setFont("Helvetica", 10)
    c.drawString(50, 560, "Sabemos lo que te gusta")
    c.drawString(300, 560, "● DE FÁBRICA")

    # ✅ DATOS EMPRESA
    c.drawString(50, 540, "Bogotá D.C.")
    c.drawString(50, 525, "Cel. 3107237192")
    c.drawString(50, 510, "Whatsapp: 3223034621-3107237192")
    c.drawString(50, 495, "Instagram: lechoneriabucaneros")
    c.drawString(50, 480, "https://www.lechoneriabucaneros.com.co/")

    # ✅ DATOS CLIENTE (TABLA)
    datos_cliente = [
        ["Nombre o razón social:", venta['nombre']],
        ["Dirección:", venta.get('domicilio', '')],
        ["Teléfono:", "------"],
        ["Fecha entrega:", hoy.strftime("%d/%m/%Y"), "Hora:", "01:00 p.m"]
    ]

    tabla_cliente = Table(datos_cliente, colWidths=[150, 250])
    tabla_cliente.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    tabla_cliente.wrapOn(c, 50, 400)
    tabla_cliente.drawOn(c, 50, 400)

    # ✅ PRODUCTO
    datos_producto = [
        ["CANTIDAD", "DESCRIPCIÓN DE PRODUCTO", "VALOR"],
        ["1", venta['producto'], f"$ {venta['precio']}"]
    ]

    tabla_producto = Table(datos_producto, colWidths=[80, 250, 100])
    tabla_producto.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey)
    ]))

    tabla_producto.wrapOn(c, 50, 300)
    tabla_producto.drawOn(c, 50, 300)

    # ✅ TOTALES
    total = float(venta['precio'])
    abonado = total * 0.5
    restante = total - abonado

    datos_total = [
        ["SALDO ABONADO", f"$ {abonado}"],
        ["SALDO RESTANTE", f"$ {restante}"],
        ["VALOR TOTAL", f"$ {total}"]
    ]

    tabla_total = Table(datos_total, colWidths=[200, 100])
    tabla_total.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black)
    ]))

    tabla_total.wrapOn(c, 50, 220)
    tabla_total.drawOn(c, 50, 220)

    # ✅ FIRMAS
    c.drawString(50, 180, "__________________________")
    c.drawString(50, 165, "FIRMA ADMINISTRADOR")

    c.drawString(300, 180, "__________________________")
    c.drawString(300, 165, "FIRMA CLIENTE")

    # ✅ CONDICIONES
    c.setFont("Helvetica", 8)
    c.drawString(50, 130, "1) SI SOLICITA EL PEDIDO CON BANDEJA TIENE UN COSTO DE $30.000...")
    c.drawString(50, 115, "2) LA BANDEJA DEBE ENTREGARSE MÁXIMO TRES DÍAS...")
    c.drawString(50, 100, "3) NO NOS HACEMOS RESPONSABLE POR MAL USO DEL PRODUCTO...")

    c.save()

    return ruta