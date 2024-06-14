// Función para cargar los datos de la habitación seleccionada en la modal de edición
function editarHabitacion(idhabitacion, numero_habitacion, tipo_habitacion, precio) {
    document.getElementById('editarIdHabitacion').value = idhabitacion;
    document.getElementById('editarNumeroHabitacion').value = numero_habitacion;
    document.getElementById('editarTipoHabitacion').value = tipo_habitacion;
    document.getElementById('editarPrecio').value = precio;

    // Modificar el atributo 'action' del formulario con la URL adecuada
    var editarHabitacionForm = document.getElementById('editarHabitacionForm'); // Cambiado de editarOficinaForm a editarHabitacionForm
    editarHabitacionForm.action = '/habitacion/editar/' + idhabitacion; // Cambiado de idOficina a idhabitacion

    // Abrir la modal de edición
    var myModal = new bootstrap.Modal(document.getElementById('modalEditarHabitacion'), {
        keyboard: false
    });
    myModal.show();
}

 