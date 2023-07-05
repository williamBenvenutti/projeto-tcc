function openLoginModal(action) {
    var modal = document.getElementById("loginModal");
    var form = document.getElementById('loginForm');
    var submitButton = document.getElementById('modalSubmitButton');

    if (action === 'finalizar') {
        form.action = "{% url 'finaliza_compra' %}";
        submitButton.value = 'Comprar';
    } else if (action === 'gastos') {
        form.action = "{% url 'mostra_gasto' %}";
        submitButton.value = 'Mostrar Gastos';
    }

    modal.style.display = "flex";
}


function closeLoginModal() {
    var modal = document.getElementById("loginModal");
    window.location.href = "{% url 'realizar_compras'%}";
    modal.style.display = "none";
}

var modalCompra = document.querySelector('#modalCompra');

setTimeout(function() {
    modalCompra = modalCompra.style.display = "none";
    window.location.href = "{% url 'realizar_compras'%}"
}, 5000);