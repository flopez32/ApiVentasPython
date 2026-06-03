from flask import  Flask, request, jsonify
import pyodbc

class CConexion:
    def ConexionBaseDeDatos():
        try:
            conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS01;'
        'DATABASE=ventas;'
        'Trusted_Connection=yes;')
            
            print("Conexión exitosa a la base de datos")

            return conexion
        except Exception as e:
            print("Error al conectar a la base de datos:", e)
            return None
        
    ConexionBaseDeDatos()  