// Você pode adicionar lógica de validação ou envio aqui


document.querySelector('.login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value;
    const senha = document.getElementById('senha').value;
    fetch('/appbk/cadastrar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nome, cpf, senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensagem) {
            alert('Usuário cadastrado com sucesso!');
        } else {
            alert('Erro: ' + (data.erro || 'Não foi possível cadastrar.'));
        }
    })
    .catch(() => {
        alert('Erro ao conectar com o servidor.');
    });
});
