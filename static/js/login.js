window.onload = function () {

    document.getElementById("btnLogin").addEventListener("click", function () {

        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        })
        .then(res => res.json())
        .then(data => {

            if (data.token) {

                localStorage.setItem("token", data.token);

                alert("Login exitoso ✅");

                window.location.href = "/index";

            } else {
                alert("Credenciales incorrectas ❌");
            }

        })
        .catch(error => console.log("ERROR:", error));

    });

};
