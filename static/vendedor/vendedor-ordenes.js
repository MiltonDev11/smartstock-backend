/*
    Módulo: static/vendedor/vendedor-ordenes.js
    Descripción: Lógica para crear órdenes/solicitudes desde la vista del
    vendedor. Recolecta ítems del formulario y llama a `/vendedor/crear-solicitud`.
*/
document.addEventListener("DOMContentLoaded", () => {

    console.log("vendedor-ordenes.js cargado correctamente");

    const btnRegistrarOrden = document.querySelector(".btn-register-order");
    console.log("¿Encontré el botón registrar orden?:", btnRegistrarOrden);

    btnRegistrarOrden?.addEventListener("click", async (e) => {
        e.preventDefault();
        console.log("CLICK DETECTADO ✓");

        const cedula = document.getElementById("cedula-order").value.trim();
        if (!cedula) return alert("Ingresa la cédula");

        const items = [];

        document.querySelectorAll(".order-item").forEach((node) => {
            const desc = node.querySelector(`[id^="descripcion-"]`)?.value?.trim() || "";
            const cantidad = parseInt(node.querySelector(`[id^="cantidad-"]`)?.value || 0);
            const precio = parseFloat(node.querySelector(`[id^="precio-"]`)?.value || 0);

            if (desc && cantidad > 0) {
                items.push({ descripcion: desc, cantidad, precio_unitario: precio });
            }
        });

        if (items.length === 0) return alert("Agrega al menos un ítem");

        const payload = { cliente_cedula: cedula, items };

        try {
            const res = await fetch("/vendedor/crear-solicitud", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!res.ok) {
                const err = await res.json();
                return alert("Error: " + err.detail);
            }

            const data = await res.json();
            alert("Solicitud creada correctamente");

        } catch (e) {
            alert("Error conectando con el servidor");
        }
    });

});
