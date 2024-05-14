const btnDelete = document.querySelectorAll('.btn-delete');
if (btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete it?')) {
                e.preventDefault();
            }
        });
    })
}

$(document).ready(function () {
    $('#example').DataTable({
        "aLengthMenu": [[3, 5, 10, 25, -1], [3, 5, 10, 25, "All"]],
        "iDisplayLength": 3
    }
    );
});

function fecharMensagem() {
    // Seleciona todos os elementos com a classe 'close'
    var botoesFechar = document.getElementsByClassName('close');

    // Para cada botão com a classe 'close', adiciona um evento de clique
    for (var i = 0; i < botoesFechar.length; i++) {
        botoesFechar[i].addEventListener('click', function () {
            // Encontra o elemento pai do botão clicado
            var mensagem = this.parentElement;

            // Remove a mensagem da tela
            mensagem.style.display = 'none';
        });
    }
}

// Chama a função para fechar a mensagem quando a página carregar
window.onload = function () {
    fecharMensagem();
};

$('#modalCadastro').on('shown.bs.modal', function () {
    $('#modalCadastro').trigger('focus')

})


