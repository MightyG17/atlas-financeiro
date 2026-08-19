document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    
    carregarDashboard();
});

async function carregarDashboard() {
    try {
        // Carrega resumo do caixa
        const resumo = await api.getResumoCaixa();
        if (resumo) {
            document.getElementById('saldoTotal').textContent = formatMoney(resumo.saldo_total);
            document.getElementById('totalReceitas').textContent = formatMoney(resumo.total_receitas);
            document.getElementById('totalDespesas').textContent = formatMoney(resumo.total_despesas);
        }

        // Carrega últimos lançamentos
        await carregarUltimosLancamentos();

        // Carrega resumos por período
        await carregarResumosPeriodo();

        // Carrega faturas pendentes
        await carregarFaturasPendentes();

    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
        showToast('Erro ao carregar dados do dashboard', 'error');
    }
}

async function carregarUltimosLancamentos() {
    try {
        const lancamentos = await api.getLancamentos({ limit: 5 });
        const container = document.getElementById('ultimosLancamentos');
        
        if (!lancamentos || lancamentos.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum lançamento recente</p>';
            return;
        }

        container.innerHTML = lancamentos.map(l => `
            <div class="lancamento-item ${l.tipo === 'receita' ? 'success' : 'danger'}">
                <div class="lancamento-info">
                    <span class="descricao">${l.descricao || l.categoria}</span>
                    <span class="categoria">${l.categoria} • ${formatDate(l.data_lancamento)}</span>
                </div>
                <span class="lancamento-valor ${l.tipo}">${formatMoney(l.valor)}</span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar lançamentos:', error);
        document.getElementById('ultimosLancamentos').innerHTML = '<p class="text-muted">Erro ao carregar lançamentos</p>';
    }
}

async function carregarResumosPeriodo() {
    const hoje = new Date();
    const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    const inicio30dias = new Date(hoje);
    inicio30dias.setDate(hoje.getDate() - 30);
    const inicio90dias = new Date(hoje);
    inicio90dias.setDate(hoje.getDate() - 90);

    try {
        // Este mês
        const resumoMes = await api.getResumoPeriodo(
            formatDateISO(inicioMes),
            formatDateISO(hoje)
        );
        document.getElementById('receitasMes').textContent = formatMoney(resumoMes.total_receitas);
        document.getElementById('despesasMes').textContent = formatMoney(resumoMes.total_despesas);

        // Últimos 30 dias
        const resumo30d = await api.getResumoPeriodo(
            formatDateISO(inicio30dias),
            formatDateISO(hoje)
        );
        document.getElementById('receitas30d').textContent = formatMoney(resumo30d.total_receitas);
        document.getElementById('despesas30d').textContent = formatMoney(resumo30d.total_despesas);

        // Últimos 90 dias
        const resumo90d = await api.getResumoPeriodo(
            formatDateISO(inicio90dias),
            formatDateISO(hoje)
        );
        document.getElementById('receitas90d').textContent = formatMoney(resumo90d.total_receitas);
        document.getElementById('despesas90d').textContent = formatMoney(resumo90d.total_despesas);

    } catch (error) {
        console.error('Erro ao carregar resumos:', error);
    }
}

async function carregarFaturasPendentes() {
    try {
        const faturas = await api.getFaturas({ status: 'pendente' });
        const pendentes = faturas ? faturas.length : 0;
        document.getElementById('faturasPendentes').textContent = pendentes;
    } catch (error) {
        console.error('Erro ao carregar faturas:', error);
        document.getElementById('faturasPendentes').textContent = '0';
    }
}

function toggleMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
}