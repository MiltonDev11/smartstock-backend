document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    const forgotPasswordModal = document.getElementById('forgotPasswordModal');
    const closeModal = document.getElementById('closeModal');

    // Muestra el modal cuando se hace clic en "¿Olvidaste tu contraseña?"
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', (e) => {
            e.preventDefault();
            if (forgotPasswordModal) {
                forgotPasswordModal.style.display = 'flex';
            }
        });
    }

    // Oculta el modal cuando se hace clic en la "X"
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            if (forgotPasswordModal) {
                forgotPasswordModal.style.display = 'none';
            }
        });
    }

    // Oculta el modal si se hace clic fuera de él (en el fondo gris)
    window.addEventListener('click', (event) => {
        if (event.target === forgotPasswordModal) {
            forgotPasswordModal.style.display = 'none';
        }
    });
});