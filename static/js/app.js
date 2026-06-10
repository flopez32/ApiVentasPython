let token = localStorage.getItem("token");
            // ✅ validar sesión
            if (!token) {
                window.location.href = "/";
            }

            // ✅ decodificar token
            let payload = JSON.parse(atob(token.split('.')[1]));

            // ✅ obtener rol
            let rol = payload.sub.rol;

            // ✅ mostrar usuario SIEMPRE
            document.getElementById("usuario").innerText =
                "Bienvenido " + payload.sub.username;

            // ✅ ocultar botones si es empleado
            if (rol === "empleado") {
                document.getElementById("btnBuscar").style.display = "none";
                document.getElementById("btnEliminar").style.display = "none";
            }

            console.log("ROL:", rol);


        function mostrarFormulario() {

        let html = `
            <h3 class="text-white">Crear Venta</h3>
            <div class="card p-4">
                <input id="nombre" class="form-control mb-2" placeholder="Nombre">
                <input id="producto" class="form-control mb-2" placeholder="Producto">
                <input id="precio" class="form-control mb-2" placeholder="Precio">
                <input id="domicilio" class="form-control mb-2" placeholder="Domicilio">
                <button class="btn btn-success" onclick="guardarVenta()">
                    Guardar
                </button>
            </div>
        `;
        document.getElementById("contenido").innerHTML = html;
    }
            
        function guardarVenta() {

    let nombre = document.getElementById("nombre").value;
    let producto = document.getElementById("producto").value;
    let precio = document.getElementById("precio").value;
    let domicilio = document.getElementById("domicilio").value;

        fetch("/ventas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + localStorage.getItem("token")
            },
            body: JSON.stringify({
                nombre,
                producto,
                precio: parseFloat(precio),
                domicilio
            })
        })
        .then(res => res.json())
        
.then(data => {

    alert(data.mensaje);

    // ✅ Volver a mostrar la pantalla principal
    document.getElementById("contenido").innerHTML = `
        <h3 class="text-white">Listado de Ventas</h3>

        <table class="table table-bordered table-striped text-center">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Producto</th>
                    <th>Precio</th>
                </tr>
            </thead>
            <tbody id="tablaVentas"></tbody>
        </table>
    `;

    // ✅ Ahora sí cargar datos
    cargarVentas();
});

}

        function cargarVentas() {
            fetch("http://127.0.0.1:5000/ventas1")
                .then(res => res.json())
                .then(data => {

                    let tabla = document.getElementById("tablaVentas");
                    tabla.innerHTML = "";

                    data.forEach(venta => {

                        let fila = document.createElement("tr");

                        fila.innerHTML = `
                            <td>${venta.id}</td>
                            <td>${venta.nombre}</td>
                            <td>${venta.producto}</td>
                            <td>${venta.precio}</td>
                            <td><a href="/factura/${venta.id}" class="btn btn-sm btn-info" target="_blank">PDF</a></td>
                        `;

                        tabla.appendChild(fila);
                    });
                });
        }
        function crearVenta() {

        let nombre = prompt("Nombre:");
        let producto = prompt("Producto:");
        let precio = prompt("Precio:");
        let domicilio = prompt("Domicilio:");

    fetch("http://127.0.0.1:5000/ventas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            nombre,
            producto,
            precio: parseFloat(precio),
            domicilio
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.mensaje);
        cargarVentas();
    });
}
        function buscarVenta() {

    let id = prompt("Ingrese el ID de la venta:");

    if (!id) {
        alert("Debe ingresar un ID");
        return;
    }

    fetch(`/ventas/${id}`)
        .then(res => res.json())
        .then(data => {

            let tabla = document.getElementById("tablaVentas");
            tabla.innerHTML = "";

            // 🔴 Si no existe
            if (data.error) {
                alert(data.error);
                return;
            }

            let fila = document.createElement("tr");

            fila.innerHTML = `
                <td>${data.id}</td>
                <td>${data.nombre}</td>
                <td>${data.producto}</td>
                <td>${data.precio}</td>
                <td><a href="/factura/${data.id}" class="btn btn-sm btn-info" target="_blank">PDF</a></td>
            `;

            tabla.appendChild(fila);
        })
        .catch(error => console.log("ERROR:", error));
}
        function eliminarVenta() {
        let id = prompt("Ingrese el ID de la venta a eliminar:");
    if (!id) {
        alert("Debe ingresar un ID");
        return;
    }
    if (!confirm("¿Seguro que quieres eliminar esta venta?")) {
        return;
    }
    fetch(`/ventas/${id}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        alert(data.mensaje);
        cargarVentas(); // 🔥 recarga la tabla
    })
    .catch(error => console.log("ERROR:", error));
}
        function cerrarSesion() {
    localStorage.removeItem("token");
    window.location.href = "/";
}  



  