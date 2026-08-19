document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    carregarPlanoContas();
});

async function carregarPlanoContas() {
    try {
        const contas = await api.getPlanoContas();
        const tbody = document.getElementById('planoContasTable');
        
        if (!contas || contas.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">Nenhuma conta cadastrada</td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = contas.map(c => `
            <tr>
                <td><code>${c.codigo}</code></td>
                <td>${c.nome}</td>
                <td>
                    <span class="status-badge ${c.tipo}">${c.tipo}</span>
                </td>
                <td>${c.nivel}</td>
                <td>${c.ativo ? '✅ Ativo' : '❌ Inativo'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar plano de contas:', error);
    }
}

function abrirModalPlanoConta() {
    document.getElementById('modalPlanoConta').classList.add('active');
}

async function salvarPlanoConta(event) {
    event.preventDefault();
    
    const data = {
        codigo: document.getElementById('planoContaCodigo').value,
        nome: document.getElementById('planoContaNome').value,
        tipo: document.getElementById('planoContaTipo').value,
        nivel: parseInt(document.getElementById('planoContaNivel').value) || 1
    };
    
    try {
        await api.criarPlanoConta(data);
        showToast('Conta criada com sucesso!', 'success');
        fecharModal('modalPlanoConta');
        carregarPlanoContas();
    } catch (error) {
        console.error('Erro ao criar conta:', error);
        showToast('Erro ao criar conta', 'error');
    }
}

async function carregarBalanco() {
    const dataInicio = document.getElementById('balancoDataInicio').value;
    const dataFim = document.getElementById('balancoDataFim').value;
    
    if (!dataInicio || !dataFim) {
        showToast('Selecione as datas de início e fim', 'error');
        return;
    }
    
    try {
        const balanco = await api.getBalancoPeriodo(dataInicio, dataFim);
        const container = document.getElementById('balancoResultados');
        
        document.getElementById('balancoReceitas').textContent = formatMoney(balanco.total_receitas);
        document.getElementById('balancoDespesas').textContent = formatMoney(balanco.total_despesas);
        document.getElementById('balancoSaldo').textContent = formatMoney(balanco.saldo);
        
        container.style.display = 'block';
    } catch (error) {
        console.error('Erro ao carregar balanço:', error);
        showToast('Erro ao carregar balanço', 'error');
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {
    const modal = document.getElementById('modalPlanoConta');
    if (event.target === modal) {
        fecharModal('modalPlanoConta');
    }
});

// Definir datas padrão para o balanço
document.addEventListener('DOMContentLoaded', function() {
    const hoje = new Date();
    const inicioMes = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    
    document.getElementById('balancoDataInicio').value = formatDateISO(inicioMes);
    document.getElementById('balancoDataFim').value = formatDateISO(hoje);
});