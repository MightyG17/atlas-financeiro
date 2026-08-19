let currentPage = 1;
let itemsPerPage = 10;
let totalItems = 0;

document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    
    // Configurar data padrão
    const hoje = new Date();
    document.getElementById('lancamentoData').value = formatDateISO(hoje);
    
    carregarLancamentos();
});

async function carregarLancamentos(page = 1) {
    currentPage = page;
    
    try {
        const tipo = document.getElementById('filterTipo').value;
        const status = document.getElementById('filterStatus').value;
        const dataInicio = document.getElementById('filterDataInicio').value;
        const dataFim = document.getElementById('filterDataFim').value;
        
        const filtros = {
            skip: (page - 1) * itemsPerPage,
            limit: itemsPerPage
        };
        
        if (tipo) filtros.tipo = tipo;
        if (status) filtros.status = status;
        if (dataInicio) filtros.data_inicio = dataInicio;
        if (dataFim) filtros.data_fim = dataFim;
        
        const lancamentos = await api.getLancamentos(filtros);
        const tbody = document.getElementById('lancamentosTable');
        
        if (!lancamentos || lancamentos.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted">Nenhum lançamento encontrado</td>
                </tr>
            `;
            return;
        }
        
        totalItems = lancamentos.length;
        
        tbody.innerHTML = lancamentos.map(l => `
            <tr>
                <td>${formatDate(l.data_lancamento)}</td>
                <td>
                    <span class="status-badge ${l.tipo === 'receita' ? 'pago' : 'pendente'}">
                        ${l.tipo === 'receita' ? '📈 Receita' : l.tipo === 'despesa' ? '📉 Despesa' : '🔄 Transferência'}
                    </span>
                </td>
                <td>${l.categoria}</td>
                <td>${l.descricao || '-'}</td>
                <td class="${l.tipo === 'receita' ? 'text-success' : 'text-danger'}">
                    ${formatMoney(l.valor)}
                </td>
                <td>
                    <span class="status-badge ${l.status}">${l.status}</span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn edit" onclick="editarLancamento(${l.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="confirmarDeletarLancamento(${l.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
        
        // Atualizar paginação
        atualizarPaginacao();
        
    } catch (error) {
        console.error('Erro ao carregar lançamentos:', error);
        showToast('Erro ao carregar lançamentos', 'error');
    }
}

function atualizarPaginacao() {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const pagination = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let html = '';
    for (let i = 1; i <= totalPages; i++) {
        html += `<button class="${i === currentPage ? 'active' : ''}" onclick="carregarLancamentos(${i})">${i}</button>`;
    }
    pagination.innerHTML = html;
}

function limparFiltros() {
    document.getElementById('filterTipo').value = '';
    document.getElementById('filterStatus').value = '';
    document.getElementById('filterDataInicio').value = '';
    document.getElementById('filterDataFim').value = '';
    carregarLancamentos(1);
}

function abrirModalLancamento(id = null) {
    const modal = document.getElementById('modalLancamento');
    const form = document.getElementById('formLancamento');
    const title = document.getElementById('modalTitle');
    
    form.reset();
    document.getElementById('lancamentoId').value = '';
    
    if (id) {
        title.textContent = 'Editar Lançamento';
        // Carregar dados para edição
        carregarLancamentoParaEdicao(id);
    } else {
        title.textContent = 'Novo Lançamento';
        const hoje = new Date();
        document.getElementById('lancamentoData').value = formatDateISO(hoje);
        document.getElementById('lancamentoStatus').value = 'pendente';
    }
    
    modal.classList.add('active');
}

async function carregarLancamentoParaEdicao(id) {
    try {
        const lancamento = await api.getLancamentos({ limit: 1000 });
        const item = lancamento.find(l => l.id === id);
        
        if (!item) {
            showToast('Lançamento não encontrado', 'error');
            return;
        }
        
        document.getElementById('lancamentoId').value = item.id;
        document.getElementById('lancamentoTipo').value = item.tipo;
        document.getElementById('lancamentoCategoria').value = item.categoria;
        document.getElementById('lancamentoDescricao').value = item.descricao || '';
        document.getElementById('lancamentoValor').value = item.valor;
        document.getElementById('lancamentoData').value = formatDateISO(item.data_lancamento);
        document.getElementById('lancamentoStatus').value = item.status;
        
    } catch (error) {
        console.error('Erro ao carregar lançamento:', error);
        showToast('Erro ao carregar dados do lançamento', 'error');
    }
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('active');
}

async function salvarLancamento(event) {
    event.preventDefault();
    
    const id = document.getElementById('lancamentoId').value;
    const data = {
        tipo: document.getElementById('lancamentoTipo').value,
        categoria: document.getElementById('lancamentoCategoria').value,
        descricao: document.getElementById('lancamentoDescricao').value || null,
        valor: parseFloat(document.getElementById('lancamentoValor').value),
        data_lancamento: document.getElementById('lancamentoData').value,
        status: document.getElementById('lancamentoStatus').value
    };
    
    try {
        if (id) {
            await api.atualizarLancamento(id, data);
            showToast('Lançamento atualizado com sucesso!', 'success');
        } else {
            await api.criarLancamento(data);
            showToast('Lançamento criado com sucesso!', 'success');
        }
        
        fecharModal('modalLancamento');
        carregarLancamentos();
    } catch (error) {
        console.error('Erro ao salvar lançamento:', error);
        showToast('Erro ao salvar lançamento', 'error');
    }
}

function confirmarDeletarLancamento(id) {
    if (confirm('Tem certeza que deseja excluir este lançamento?')) {
        deletarLancamento(id);
    }
}

async function deletarLancamento(id) {
    try {
        await api.deletarLancamento(id);
        showToast('Lançamento excluído com sucesso!', 'success');
        carregarLancamentos();
    } catch (error) {
        console.error('Erro ao deletar lançamento:', error);
        showToast('Erro ao excluir lançamento', 'error');
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {
    const modal = document.getElementById('modalLancamento');
    if (event.target === modal) {
        fecharModal('modalLancamento');
    }
});