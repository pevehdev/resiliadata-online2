
    document.getElementById('cep').addEventListener('blur', function () {
        var cep = document.getElementById('cep').value;
        if (cep.trim() != '') {
            fetch('https://viacep.com.br/ws/' + cep + '/json/')
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        document.getElementById('rua').value = data.logradouro;
                        document.getElementById('cidade').value = data.localidade;
                        document.getElementById('bairro').value = data.bairro;
                        document.getElementById('pais').value = 'Brasil';
                    } else {
                        alert('CEP não encontrado. Por favor, verifique o CEP digitado.');
                    }
                })
                .catch(error => console.error('Erro ao buscar endereço:', error));
        }
    });