document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    carregarFaturas();
});

async function carregarFaturas() {
    try {
        const faturas = await api.getFaturas();
        const tbody = document.getElementById('faturasTable');
        
        if (!faturas || faturas.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted">Nenhuma fatura encontrada</td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = faturas.map(f => `
            <tr>
                <td><code>${f.codigo_barras}</code></td>
                <td>${formatMoney(f.valor)}</td>
                <td>${formatDate(f.data_vencimento)}</td>
                <td>
                    <span class="status-badge ${f.status}">${f.status}</span>
                </td>
                <td>${f.categoria || '-'}</td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn edit" onclick="editarFatura(${f.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="confirmarDeletarFatura(${f.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar faturas:', error);
        showToast('Erro ao carregar faturas', 'error');
    }
}

function abrirModalFatura(id = null) {
    const modal = document.getElementById('modalFatura');
    const form = document.getElementById('formFatura');
    const title = document.getElementById('modalFaturaTitle');
    
    form.reset();
    document.getElementById('faturaId').value = '';
    
    if (id) {
        title.textContent = 'Editar Fatura';
        carregarFaturaParaEdicao(id);
    } else {
        title.textContent = 'Nova Fatura';
        const hoje = new Date();
        const vencimento = new Date(hoje);
        vencimento.setDate(hoje.getDate() + 30);
        document.getElementById('faturaVencimento').value = formatDateISO(vencimento);
    }
    
    modal.classList.add('active');
}

async function carregarFaturaParaEdicao(id) {
    try {
        const faturas = await api.getFaturas();
        const fatura = faturas.find(f => f.id === id);
        
        if (!fatura) {
            showToast('Fatura não encontrada', 'error');
            return;
        }
        
        document.getElementById('faturaId').value = fatura.id;
        document.getElementById('faturaCodigo').value = fatura.codigo_barras;
        document.getElementById('faturaValor').value = fatura.valor;
        document.getElementById('faturaVencimento').value = formatDateISO(fatura.data_vencimento);
        document.getElementById('faturaPagamento').value = fatura.data_pagamento ? formatDateISO(fatura.data_pagamento) : '';
        document.getElementById('faturaStatus').value = fatura.status;
        document.getElementById('faturaCategoria').value = fatura.categoria || '';
        document.getElementById('faturaDescricao').value = fatura.descricao || '';
        
    } catch (error) {
        console.error('Erro ao carregar fatura:', error);
        showToast('Erro ao carregar dados da fatura', 'error');
    }
}

async function salvarFatura(event) {
    event.preventDefault();
    
    const id = document.getElementById('faturaId').value;
    const data = {
        codigo_barras: document.getElementById('faturaCodigo').value,
        valor: parseFloat(document.getElementById('faturaValor').value),
        data_vencimento: document.getElementById('faturaVencimento').value,
        data_pagamento: document.getElementById('faturaPagamento').value || null,
        status: document.getElementById('faturaStatus').value,
        categoria: document.getElementById('faturaCategoria').value || null,
        descricao: document.getElementById('faturaDescricao').value || null
    };
    
    try {
        if (id) {
            await api.atualizarFatura(id, data);
            showToast('Fatura atualizada com sucesso!', 'success');
        } else {
            await api.criarFatura(data);
            showToast('Fatura criada com sucesso!', 'success');
        }
        
        fecharModal('modalFatura');
        carregarFaturas();
    } catch (error) {
        console.error('Erro ao salvar fatura:', error);
        showToast('Erro ao salvar fatura', 'error');
    }
}

function confirmarDeletarFatura(id) {
    if (confirm('Tem certeza que deseja excluir esta fatura?')) {
        deletarFatura(id);
    }
}

async function deletarFatura(id) {
    try {
        await api.deletarFatura(id);
        showToast('Fatura excluída com sucesso!', 'success');
        carregarFaturas();
    } catch (error) {
        console.error('Erro ao deletar fatura:', error);
        showToast('Erro ao excluir fatura', 'error');
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {
    const modal = document.getElementById('modalFatura');
    if (event.target === modal) {
        fecharModal('modalFatura');
    }
});