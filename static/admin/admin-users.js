document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('formRegistrarUsuario');
  const tablaBody = document.querySelector('#tablaUsuarios tbody');
  const inputBuscar = document.querySelector('.search-input');

  // ==========================
  // 1️⃣ FUNCIÓN: Cargar usuarios
  // ==========================
  async function cargarUsuarios() {
    try {
      const res = await fetch("/admin/usuarios");
      if (!res.ok) throw new Error("Error al obtener usuarios");
      const data = await res.json();
      renderUsuarios(data);

      // Filtro de búsqueda
      inputBuscar.addEventListener("input", () => {
        const filtro = inputBuscar.value.toLowerCase();
        const filtrados = data.filter(u =>
          u.cedula.toLowerCase().includes(filtro) ||
          u.id.toLowerCase().includes(filtro)
        );
        renderUsuarios(filtrados);
      });

    } catch (err) {
      console.error("Error al cargar usuarios:", err);
      tablaBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align:center; color:#777;">
            Error al cargar usuarios
          </td>
        </tr>`;
    }
  }

  // ==========================
  // 2️⃣ FUNCIÓN: Renderizar tabla
  // ==========================
  function renderUsuarios(lista) {
    tablaBody.innerHTML = "";
    if (lista.length === 0) {
      tablaBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align:center; color:#777;">No hay usuarios registrados</td>
        </tr>`;
      return;
    }

    lista.forEach(u => {
      const row = `
        <tr>
          <td>${u.id}</td>
          <td>${u.nombre}</td>
          <td>${u.cedula}</td>
          <td>${u.celular || '-'}</td>
          <td>${u.correo}</td>
          <td>${u.role}</td>
          <td style="color:${u.estado === "Vinculado" ? "green" : "red"}; font-weight:600;">
            ${u.estado}
          </td>
        </tr>`;
      tablaBody.insertAdjacentHTML("beforeend", row);
    });
  }

  // ==========================
  // 3️⃣ FUNCIÓN: Registrar usuario
  // ==========================
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const nombre = document.getElementById('nombreUsuario').value.trim();
      const cedula = document.getElementById('cedulaUsuario').value.trim();
      const celular = document.getElementById('celularUsuario').value.trim();
      const correo = document.getElementById('correoUsuario').value.trim();

      if (!nombre || !cedula || !correo) {
        alert("Por favor completa los campos obligatorios.");
        return;
      }

      const payload = { nombre, cedula, celular: celular || null, correo };

      try {
        const res = await fetch("/admin/register-user", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          const data = await res.json();
          alert(`Usuario creado y correo enviado a: ${data.correo}`);
          form.reset();
          cargarUsuarios(); // 🔁 refresca la tabla automáticamente
        } else {
          const err = await res.json();
          alert("Error: " + (err.detail || err.msg || JSON.stringify(err)));
        }
      } catch (error) {
        alert("Error conectando al servidor: " + error.message);
      }
    });
  }

  // ==========================
  // 4️⃣ Aplicar scroll limitado a la tabla
  // ==========================
  const tableWrap = document.querySelector(".table-wrap");
  if (tableWrap) {
    tableWrap.style.maxHeight = "300px"; // ajusta altura visible
    tableWrap.style.overflowY = "auto";
  }

  // ==========================
  // 5️⃣ Cargar usuarios al inicio
  // ==========================
  cargarUsuarios();
});
