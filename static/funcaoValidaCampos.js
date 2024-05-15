
    document.getElementById('btnCadastrar').addEventListener('click', function(event) {
        event.preventDefault(); // Evita que o formulário seja enviado automaticamente

        // Validação dos campos obrigatórios
        var data_nasc = document.getElementById('data_nasc').value;
        var data_contrato = document.getElementById('data_contrato').value;

        if (!data_nasc || !data_contrato) {
            alert('Por favor, preencha todos os campos obrigatórios.');
            return;
        } else {
        // Se todos os campos obrigatórios estiverem preenchidos, envie o formulário
        document.getElementById('cadastroForm').submit();
    }
    });
