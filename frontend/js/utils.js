// Formatação de moeda
function formatMoney(value) {
    if (value === undefined || value === null) return 'R$ 0,00';
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Formatação de data
function formatDate(date) {
    if (!date) return '-';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '-';
    return d.toLocaleDateString('pt-BR');
}

// Formatação de data ISO
function formatDateISO(date) {
    if (!date) return '';
    const d = date instanceof Date ? date : new Date(date);
    if (isNaN(d.getTime())) return '';
    return d.toISOString().split('T')[0];
}

// Formatação mês/ano
function formatMonthYear(date) {
    if (!date) return '-';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '-';
    return d.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
}

// Toast notifications
function showToast(message, type = 'info') {
    const colors = {
        success: '#22c55e',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${colors[type] || colors.info};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        font-weight: 500;
        max-width: 400px;
        animation: slideUp 0.3s ease;
        font-family: 'Inter', sans-serif;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Funções para modais
function fecharModal(id) {
    document.getElementById(id).classList.remove('active');
}

function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// Fechar menu mobile ao clicar fora
document.addEventListener('click', function(event) {
    const nav = document.querySelector('.navbar .container');
    const menu = document.querySelector('.nav-links');
    const btn = document.querySelector('.mobile-menu-btn');
    
    if (nav && menu && btn && !nav.contains(event.target) && menu.classList.contains('active')) {
        menu.classList.remove('active');
    }
});

// Fechar modais ao clicar fora
document.addEventListener('click', function(event) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });
});