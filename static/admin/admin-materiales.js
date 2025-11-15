/*
  Módulo: static/admin/admin-materiales.js
  Descripción: Funciones de frontend para la gestión de materiales:
  - Cargar y renderizar la lista de materiales
  - Registrar nuevos materiales mediante POST a /admin/registrar-material
  - Filtrado y mejoras de UI (scroll limitado)
*/
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('formRegistrarMaterial');
  const tablaBody = document.querySelector('.table tbody');
  const inputBuscar = document.querySelector('.search-input');

  // Cargar materiales
  async function cargarMateriales() {
    try {
      const res = await fetch("/admin/api/materiales");
      const data = await res.json();
      renderMateriales(data);

      inputBuscar.addEventListener("input", () => {
        const filtro = inputBuscar.value.toLowerCase();
        const filtrados = data.filter(m =>
          m.material.toLowerCase().includes(filtro) ||
          (m.medida && m.medida.toLowerCase().includes(filtro))
        );
        renderMateriales(filtrados);
      });
    } catch (err) {
      tablaBody.innerHTML = `<tr><td colspan="8">Error al cargar materiales</td></tr>`;
    }
  }

  // Renderizar
  function renderMateriales(lista) {
    tablaBody.innerHTML = "";
    if (lista.length === 0) {
      tablaBody.innerHTML = `<tr><td colspan="8">No hay materiales registrados</td></tr>`;
      return;
    }
    lista.forEach(m => {
      const row = `
        <tr>
          <td>M${String(m.id).padStart(3, "0")}</td>
          <td>${m.material}</td>
          <td>${m.medida || "-"}</td>
          <td>${m.unidad || "-"}</td>
          <td>$${m.precio_unitario.toLocaleString()}</td>
          <td>${m.marca || "-"}</td>
          <td>${m.cantidad}</td>
          <td>$${m.ingreso.toLocaleString()}</td>
        </tr>`;
      tablaBody.insertAdjacentHTML("beforeend", row);
    });
  }

  // Registrar material
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const material = document.getElementById("nombreMaterial").value.trim();
      const medida = document.getElementById("medidaMaterial").value.trim();
      const unidad = document.getElementById("unidadMaterial").value.trim();
      const precio_unitario = parseFloat(document.getElementById("precioMaterial").value);
      const marca = document.getElementById("marcaMaterial").value.trim();
      const cantidad = parseInt(document.getElementById("cantidadMaterial").value);

      if (!material || !precio_unitario || !cantidad) {
        alert("Por favor llena todos los campos obligatorios");
        return;
      }

      const payload = { material, medida, unidad, precio_unitario, marca, cantidad };

      try {
        const res = await fetch("/admin/registrar-material", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          alert("✅ Material registrado correctamente");
          form.reset();
          cargarMateriales();
        } else {
          const err = await res.json();
          alert("Error: " + (err.detail || err.msg));
        }
      } catch (error) {
        alert("Error en la conexión con el servidor");
      }
    });
  }

  // Scroll limitado
  const tableWrap = document.querySelector(".table-wrap");
  if (tableWrap) {
    tableWrap.style.maxHeight = "300px";
    tableWrap.style.overflowY = "auto";
  }

  cargarMateriales();
});
