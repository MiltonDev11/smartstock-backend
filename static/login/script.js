document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const forgotPasswordModal = document.getElementById('forgotPasswordModal');
    const closeModal = document.getElementById('closeModal');
    const validarBtn = document.querySelector('.btn-validar'); // Botón Validar
    const resultadoDiv = document.getElementById('resultado'); // Donde mostraremos el mensaje

    // === Muestra el modal al hacer clic en "¿Olvidaste tu contraseña?" ===
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (forgotPasswordModal) {
                forgotPasswordModal.style.display = 'flex';
            }
        });
    }

    // === Cierra el modal al hacer clic en la "X" ===
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            if (forgotPasswordModal) {
                forgotPasswordModal.style.display = 'none';
                resultadoDiv.innerHTML = ""; // Limpia mensajes al cerrar
            }
        });
    }

    // === Cierra el modal si se hace clic fuera del cuadro ===
    window.addEventListener('click', (event) => {
        if (event.target === forgotPasswordModal) {
            forgotPasswordModal.style.display = 'none';
            resultadoDiv.innerHTML = ""; // Limpia mensajes
        }
    });

    // === Lógica para el botón "Validar" ===
    if (validarBtn) {
        validarBtn.addEventListener('click', async () => {
            const cedula = document.getElementById('cedula').value.trim();

            if (!cedula) {
                resultadoDiv.innerHTML = `
                    <div style='background-color: #f8d7da; color: #842029; padding: 10px; border-radius: 6px; text-align: center;'>
                        Por favor, ingresa una cédula.
                    </div>`;
                return;
            }

            const formData = new FormData();
            formData.append("cedula", cedula);

            try {
                const response = await fetch("/password-reset", {
                    method: "POST",
                    body: formData
                });

                const message = await response.text();
                resultadoDiv.innerHTML = message;
            } catch (error) {
                resultadoDiv.innerHTML = `
                    <div style='background-color: #f8d7da; color: #842029; padding: 10px; border-radius: 6px; text-align: center;'>
                        Ocurrió un error al conectar con el servidor.
                    </div>`;
            }
        });
    }
});
