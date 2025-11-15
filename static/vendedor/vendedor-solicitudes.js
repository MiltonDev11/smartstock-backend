/*
  Módulo: static/vendedor/vendedor-solicitudes.js
  Descripción: Carga y muestra las solicitudes (lista y detalle) para la
  vista administrativa de solicitudes y permite cambiar estados.
*/
document.addEventListener("DOMContentLoaded", () => {

  // ============================================================
  //  1. CARGAR TABLA DE SOLICITUDES
  // ============================================================

  const tbody = document.querySelector(".table tbody");
  const productosContainer = document.createElement("div");
  productosContainer.style.marginTop = "25px";
  productosContainer.innerHTML = ""; // Contenedor vacío al inicio
  document.querySelector(".container-card").appendChild(productosContainer);

  async function cargarSolicitudes() {
    try {
      const res = await fetch("/admin/api/solicitudes");
      const data = await res.json();

      tbody.innerHTML = "";

      data.forEach(s => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
          <td>S${String(s.id).padStart(4, "0")}</td>
          <td>${s.cliente_cedula}</td>
          <td>${s.items.length} producto(s)</td>
          <td>${s.created_at ? s.created_at.split("T")[0] : "-"}</td>
          <td><span class="small ${getEstadoClase(s.status)}">${formatearEstado(s.status)}</span></td>
          <td><button class="btn ghost ver-btn" data-id="${s.id}">Ver</button></td>
        `;

        tbody.appendChild(tr);
      });

      activarBotonesVer();

    } catch (err) {
      console.error("Error cargando solicitudes:", err);
    }
  }

  function formatearEstado(e) {
    if (e === "pendiente") return "Pendiente";
    if (e === "en_proceso") return "En proceso";
    if (e === "completado") return "Completado";
    return e;
  }

  function getEstadoClase(e) {
    if (e === "pendiente") return "estado-pendiente";
    if (e === "en_proceso") return "estado-proceso";
    if (e === "completado") return "estado-completado";
    return "";
  }

  cargarSolicitudes();


  // ============================================================
  //  2. MOSTRAR TABLA DE PRODUCTOS DE UNA SOLICITUD
  // ============================================================

  function activarBotonesVer() {
    document.querySelectorAll(".ver-btn").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;

        const res = await fetch(`/admin/api/solicitudes/${id}`);
        const soli = await res.json();

        productosContainer.innerHTML = `
          <h3 style="margin:12px 0;">Productos de solicitud S${String(soli.id).padStart(4, "0")}</h3>

          <table class="table">
            <thead>
              <tr>
                <th>Descripción</th>
                <th>Cantidad</th>
                <th>Precio unitario</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              ${soli.items.map(it => `
                <tr>
                  <td>${it.descripcion}</td>
                  <td>${it.cantidad}</td>
                  <td>$${it.precio_unitario.toLocaleString()}</td>
                  <td>$${(it.cantidad * it.precio_unitario).toLocaleString()}</td>
                </tr>
              `).join("")}
            </tbody>
          </table>
        `;
      });
    });
  }

  // ============================================================
  //  3. CAMBIAR ESTADO DE SOLICITUD
  // ============================================================

  const btnCambiarEstado = document.getElementById("btnCambiarEstado");

  btnCambiarEstado?.addEventListener("click", async () => {
    const id = document.getElementById("estadoIdInput").value.trim();
    const nuevoEstado = document.getElementById("estadoSelect").value;

    if (!id || nuevoEstado === "seleccionar") {
      alert("Completa todos los campos.");
      return;
    }

    const res = await fetch(`/admin/api/solicitudes/${id}/estado?nuevo_estado=${nuevoEstado}`, {
      method: "POST"
    });

    if (!res.ok) {
      const err = await res.json();
      alert("❌ Error: " + err.detail);
      return;
    }

    alert("✔ Estado actualizado.");
    cargarSolicitudes();
  });


  // ============================================================
  //  4. (YA EXISTENTE) CREAR SOLICITUD DESDE VENDEDOR
  // ============================================================

  const btnRegistrarOrden = document.querySelector(".btn-register-order");
  console.log("¿Encontré el botón registrar orden?:", btnRegistrarOrden);

  btnRegistrarOrden?.addEventListener("click", async (e) => {
    console.log("Se hizo click ✓");
    e.preventDefault();

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
      // limpiar cedula
      document.getElementById("cedula-order").value = "";
            
      // limpiar todos los items
      document.querySelectorAll(".order-item").forEach((node, index) => {
          if (index === 0) {
              node.querySelector(`[id^="descripcion-"]`).value = "";
              node.querySelector(`[id^="cantidad-"]`).value = "";
              node.querySelector(`[id^="precio-"]`).value = "";
          } else {
              node.remove();
          }
      });
      cargarSolicitudes(); // refrescar admin

    } catch (e) {
      alert("Error conectando con el servidor");
    }
  });

});
