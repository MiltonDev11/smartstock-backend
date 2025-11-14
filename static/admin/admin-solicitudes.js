document.addEventListener("DOMContentLoaded", () => {

    const tbody = document.querySelector(".table tbody");

    const modal = crearModal();
    document.body.appendChild(modal.container);

    async function cargarSolicitudes() {
        const res = await fetch("/admin/api/solicitudes");
        const solicitudes = await res.json();

        tbody.innerHTML = "";

        solicitudes.forEach(s => {

            const valorEsperado = s.items.reduce(
                (acc, it) => acc + (it.cantidad * it.precio_unitario),
                0
            );

            const row = `
                <tr>
                    <td>S${String(s.id).padStart(4,'0')}</td>
                    <td>${s.cliente_cedula}</td>
                    <td>${s.items.length} productos</td>
                    <td>${s.created_at.split("T")[0]}</td>
                    <td>${formatearEstado(s.status)}</td>
                    <td>$${valorEsperado.toLocaleString()}</td>
                    <td>$${(s.valor_recibido || 0).toLocaleString()}</td>
                    <td><button class="btn ghost ver-btn" data-id="${s.id}">Ver</button></td>
                </tr>
            `;

            tbody.insertAdjacentHTML("beforeend", row);
        });

        activarBotonesVer();
    }

    function activarBotonesVer() {
        document.querySelectorAll(".ver-btn").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id = btn.dataset.id;

                const res = await fetch(`/admin/api/solicitudes/${id}`);
                const soli = await res.json();

                modal.setContent(generarHTMLModalSolicitud(soli));
                modal.open();
            });
        });
    }

    function generarHTMLModalSolicitud(s) {

        return `
            <h2>Solicitud S${String(s.id).padStart(4,'0')}</h2>
            <p><strong>Cliente:</strong> ${s.cliente_cedula}</p>
            <p><strong>Fecha creación:</strong> ${s.created_at.split("T")[0]}</p>
            <p><strong>Estado:</strong> ${formatearEstado(s.status)}</p>

            <h3 style="margin-top:20px;">Productos</h3>

            <table class="table">
                <thead>
                    <tr>
                        <th>Descripción</th>
                        <th>Cantidad</th>
                        <th>Precio unitario</th>
                        <th>Subtotal</th>
                        <th>Encargado</th>
                        <th>Estado</th>
                        <th>Fecha completado</th>
                    </tr>
                </thead>
                <tbody>
                    ${s.items.map(it => `
                        <tr>
                            <td>${it.descripcion}</td>
                            <td>${it.cantidad}</td>
                            <td>$${it.precio_unitario.toLocaleString()}</td>
                            <td>$${(it.cantidad * it.precio_unitario).toLocaleString()}</td>
                            <td>${it.encargado || "No asignado"}</td>
                            <td>${formatearEstado(it.estado)}</td>
                            <td>${it.fecha_completado ? it.fecha_completado.split("T")[0] : "-"}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    }

    function formatearEstado(e) {
        if (e === "pendiente") return "Pendiente";
        if (e === "en_proceso") return "En proceso";
        if (e === "completado") return "Completado";
        return e;
    }

    cargarSolicitudes();

    // ==========================
    // COMPONENTE MODAL
    // ==========================
    function crearModal() {
        const container = document.createElement("div");
        container.classList.add("modal-overlay");
        container.innerHTML = `
            <div class="modal">
                <button class="close-btn">X</button>
                <div class="modal-content"></div>
            </div>
        `;

        const closeBtn = container.querySelector(".close-btn");
        const content = container.querySelector(".modal-content");

        closeBtn.addEventListener("click", () => container.classList.remove("open"));

        return {
            container,
            setContent(html) {
                content.innerHTML = html;
            },
            open() {
                container.classList.add("open");
            }
        };
    }
});
