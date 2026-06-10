# Lechonería Bucaneros - Sistema de Gestión de Ventas

## 📋 Descripción

Sistema web de gestión de ventas para Lechonería Bucaneros. Aplicación que permite administrar ventas de productos con autenticación de usuarios y control de roles (administrador y empleado). La plataforma incluye funcionalidades para crear, consultar, actualizar y eliminar registros de ventas en tiempo real.

## 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **Base de Datos**: SQL Server (ODBC Driver 17)
- **Autenticación**: JWT (JSON Web Tokens)
- **Frontend**: HTML5, Bootstrap 5.3.0, JavaScript
- **Librerías principales**:
  - `flask` - Framework web
  - `flask-jwt-extended` - Gestión de tokens JWT
  - `pyodbc` - Conexión a SQL Server

## 🔌 Endpoints de la API

### Autenticación

#### POST `/login`
Autentica un usuario y retorna un token JWT.

**Body:**
```json
{
  "username": "usuario",
  "password": "contraseña"
}
```

**Respuesta (201):**
```json
{
  "mensaje": "Login exitoso ✅",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Ventas (CRUD)

#### GET `/ventas1`
Obtiene todas las ventas registradas.

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "producto": "Lechona",
    "precio": 25.50,
    "domicilio": "Calle 1 #123"
  }
]
```

#### POST `/ventas`
Crea una nueva venta.

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Juan Pérez",
  "producto": "Lechona",
  "precio": 25.50,
  "domicilio": "Calle 1 #123"
}
```

**Respuesta (201):**
```json
{
  "mensaje": "Venta creada correctamente ✅"
}
```

#### GET `/ventas/<id>`
Obtiene una venta específica por ID.

**Respuesta (200):**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "producto": "Lechona",
  "precio": 25.50,
  "domicilio": "Calle 1 #123"
}
```

#### PUT `/ventas2/<id>`
Actualiza una venta existente.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "nombre": "Juan Pérez",
  "producto": "Lechona Premium",
  "precio": 30.00,
  "domicilio": "Calle 2 #456"
}
```

**Respuesta (200):**
```json
{
  "mensaje": "Venta actualizada correctamente ✅"
}
```

#### DELETE `/ventas/<id>`
Elimina una venta.

**Respuesta (200):**
```json
{
  "mensaje": "Venta eliminada correctamente ✅"
}
```

---

### Páginas Web

#### GET `/`
Carga la página de login.

#### GET `/index`
Carga la página principal (requiere token JWT válido).

---

## 👥 Control de Roles

- **Administrador**: Acceso completo a todas las funciones (crear, buscar, eliminar)
- **Empleado**: Solo visualización de ventas

## 🚀 Instalación y Uso

1. Instalar dependencias:
```bash
pip install flask flask-jwt-extended pyodbc
```

2. Configurar la conexión a SQL Server en `Conexion.py`

3. Ejecutar la aplicación:
```bash
python main.py
```

4. Acceder a: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
ApiPythonCrud/
├── main.py                 # Aplicación principal con rutas
├── Conexion.py            # Clase de conexión a BD
├── templates/
│   ├── login.html         # Página de login
│   └── index.html         # Página principal
└── static/
    ├── logo3.png          # Logo de la empresa
    └── Diseño.png         # Imagen de fondo
```
