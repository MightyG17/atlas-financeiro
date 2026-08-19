document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    carregarGrupos();
});

async function carregarGrupos() {
    try {
        const grupos = await api.getGrupos();
        const container = document.getElementById('gruposGrid');
        
        if (!grupos || grupos.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum grupo encontrado</p>';
            return;
        }
        
        container.innerHTML = grupos.map(g => `
            <div class="grupo-card">
                <h3>${g.nome}</h3>
                <p class="descricao">${g.descricao || 'Sem descrição'}</p>
                <div class="meta">
                    <div>📅 ${formatDate(g.data_inicio)} ${g.data_fim ? `a ${formatDate(g.data_fim)}` : ''}</div>
                    <div>📊 ${g.status}</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar grupos:', error);
        document.getElementById('gruposGrid').innerHTML = '<p class="text-muted">Erro ao carregar grupos</p>';
    }
}

function abrirModalGrupo() {
    document.getElementById('modalGrupo').classList.add('active');
}

async function salvarGrupo(event) {
    event.preventDefault();
    
    const data = {
        nome: document.getElementById('grupoNome').value,
        descricao: document.getElementById('grupoDescricao').value || null,
        data_inicio: document.getElementById('grupoDataInicio').value,
        data_fim: document.getElementById('grupoDataFim').value || null
    };
    
    try {
        await api.criarGrupo(data);
        showToast('Grupo criado com sucesso!', 'success');
        fecharModal('modalGrupo');
        carregarGrupos();
    } catch (error) {
        console.error('Erro ao criar grupo:', error);
        showToast('Erro ao criar grupo', 'error');
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', function(event) {
    const modal = document.getElementById('modalGrupo');
    if (event.target === modal) {
        fecharModal('modalGrupo');
    }
});