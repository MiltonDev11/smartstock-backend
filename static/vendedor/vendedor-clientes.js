document.addEventListener("DOMContentLoaded", () => {
    const btnRegistrar = document.querySelector(".btn-register");

    btnRegistrar.addEventListener("click", async () => {
        const nombre = document.getElementById("nombre-user").value.trim();
        const cedula = document.getElementById("cedula-user").value.trim();
        const celular = document.getElementById("celular-user").value.trim();
        const correo = document.getElementById("correo-user").value.trim();

        if (!nombre || !cedula || !correo) {
            alert("⚠️ Debes completar nombre, cédula y correo");
            return;
        }

        const payload = { nombre, cedula, celular, correo };

        try {
            const res = await fetch("http://localhost:8000/vendedor/registrar-cliente", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const err = await res.json();
                alert("Error: " + err.detail);
                return;
            }

            const data = await res.json();
            alert(`Cliente registrado correctamente: ${data.nombre}`);

            // limpiar campos
            document.getElementById("nombre-user").value = "";
            document.getElementById("cedula-user").value = "";
            document.getElementById("celular-user").value = "";
            document.getElementById("correo-user").value = "";

        } catch (e) {
            alert("❌ Error al conectar con el servidor");
        }
    });
});
