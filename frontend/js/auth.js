// Verifica autenticação ao carregar páginas protegidas
document.addEventListener('DOMContentLoaded', function() {
    const protectedPages = ['dashboard.html', 'lancamentos.html', 'faturas.html', 'energia.html', 'grupos.html', 'contabilidade.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (protectedPages.includes(currentPage)) {
        if (!api.checkAuth()) {
            window.location.href = 'login.html';
        } else {
            // Carrega informações do usuário
            const userData = api.getUserData();
            if (userData && document.getElementById('userName')) {
                document.getElementById('userName').textContent = userData.nome || 'Usuário';
            }
        }
    }
});

// Função de logout
window.logout = function(event) {
    if (event) event.preventDefault();
    api.logout();
};

// Função para verificar se está logado
function isLoggedIn() {
    return !!api.getAuthToken();
}