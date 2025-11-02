document.addEventListener('DOMContentLoaded', function() {
    // -------------------------------------------------------------------
    // 1. Funcionalidad Colapsar/Expandir (Registrar usuario)
    // -------------------------------------------------------------------
    const collapseToggle = document.getElementById('userCollapseToggle');
    const collapseContent = document.getElementById('userCollapseContent');
    const collapseArrow = document.getElementById('collapseArrow');

    if (collapseToggle && collapseContent && collapseArrow) {
        collapseToggle.addEventListener('click', function() {
            const isCollapsed = collapseContent.classList.toggle('collapsed');

            if (isCollapsed) {
                // Si se colapsa, la flecha mira hacia abajo (posición por defecto)
                collapseArrow.classList.remove('arrow-up');
            } else {
                // Si se expande, la flecha gira para mirar hacia arriba
                collapseArrow.classList.add('arrow-up');
            }
        });
        
        // Inicialmente, se ve expandido, pero la flecha apunta hacia abajo.
        // Si quieres que inicie colapsado, descomenta las siguientes 2 líneas:
        // collapseContent.classList.add('collapsed');
        // collapseArrow.classList.remove('arrow-up');
    }

    // -------------------------------------------------------------------
    // 2. Funcionalidad Duplicar/Eliminar Campos (Registrar orden)
    // -------------------------------------------------------------------
    const addBtn = document.getElementById('addOrderItem');
    const removeBtn = document.getElementById('removeOrderItem');
    const container = document.getElementById('orderItemsContainer');
    let itemCount = 1; // Contador para ID únicos

    // Función para crear un nuevo conjunto de campos Descripción y Cantidad
    function createOrderItem() {
        itemCount++; // Incrementa para el nuevo ID
        const newItem = document.createElement('div');
        newItem.classList.add('order-item');
        newItem.dataset.itemId = itemCount; // Identificador para eliminar

        newItem.innerHTML = `
            <div class="field-container description-field">
                <label for="descripcion-${itemCount}">Descripción</label>
                <textarea id="descripcion-${itemCount}" placeholder="Descripción"></textarea>
            </div>
            <div class="field-container quantity-field">
                <label for="cantidad-${itemCount}">Cantidad</label>
                <input type="number" id="cantidad-${itemCount}" placeholder="Número">
            </div>
        `;
        return newItem;
    }

    // Evento para AGREGAR campos (+)
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            const newItem = createOrderItem();
            container.appendChild(newItem);
        });
    }

    // Evento para ELIMINAR campos (-)
    if (removeBtn) {
        removeBtn.addEventListener('click', function() {
            // Obtiene todos los elementos de orden
            const items = container.querySelectorAll('.order-item');
            
            // La lógica es: solo eliminar si hay más de 1 (el original/por defecto)
            if (items.length > 1) {
                // Elimina el último elemento agregado
                const lastItem = items[items.length - 1];
                container.removeChild(lastItem);
            } else {
                // Opcional: Notificar al usuario que no se puede eliminar el campo por defecto
                console.log("No se puede eliminar el campo de orden por defecto.");
                // alert("Debe haber al menos un campo de orden.");
            }
        });
    }
});