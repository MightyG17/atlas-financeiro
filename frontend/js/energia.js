document.addEventListener('DOMContentLoaded', function() {
    if (!api.checkAuth()) return;
    carregarContratos();
    carregarFaturasEnergia();
});

async function carregarContratos() {
    try {
        const contratos = await api.getContratos();
        const container = document.getElementById('contratosList');
        
        if (!contratos || contratos.length === 0) {
            container.innerHTML = '<p class="text-muted">Nenhum contrato cadastrado</p>';
            return;
        }
        
        container.innerHTML = contratos.map(c => `
            <div class="contrato-item">
                <div class="concessionaria">${c.concessionaria}</div>
                <div class="unidade">UC: ${c.unidade_consumidora}</div>
                <div style="font-size:0.85rem; color: var(--gray-500);">
                    ${c.modalidade_tarifaria} • ${c.tensao} • ${c.ativo ? '✅ Ativo' : '❌ Inativo'}
                </div>
            </div>
        `).join('');
        
        // Popular select de contratos no modal de fatura
        const select = document.getElementById('faturaEnergiaContrato');
        select.innerHTML = '<option value="">Selecione um contrato</option>' + 
            contratos.filter(c => c.ativo).map(c => 
                `<option value="${c.id}">${c.concessionaria} - ${c.unidade_consumidora}</option>`
            ).join('');
            
    } catch (error) {
        console.error('Erro ao carregar contratos:', error);
        document.getElementById('contratosList').innerHTML = '<p class="text-muted">Erro ao carregar contratos</p>';
    }
}

async function carregarFaturasEnergia() {
    try {
        const faturas = await api.getFaturasEnergia({ limit: 100 });
        const tbody = document.getElementById('faturasEnergiaTable');
        
        if (!faturas || faturas.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-muted">Nenhuma fatura de energia encontrada</td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = faturas.map(f => `
            <tr>
                <td>${formatMonthYear(f.mes_referencia)}</td>
                <td>${f.consumo_kwh.toFixed(2)} kWh</td>
                <td>${formatMoney(f.valor_total)}</td>
                <td>
                    <span class="status-badge ${f.bandeira_ativa || 'verde'}">
                        ${f.bandeira_ativa || 'Verde'}
                    </span>
                </td>
                <td>
                    <span class="status-badge ${f.status}">${f.status}</span>
                </td>
                <td>
                    <button class="action-btn edit" onclick="verAnalise(${f.id})">
                        <i class="fas fa-chart-bar"></i> Análise
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erro ao carregar faturas de energia:', error);
    }
}

function abrirModalContrato() {
    document.getElementById('modalContrato').classList.add('active');
}

function abrirModalFaturaEnergia() {
    document.getElementById('modalFaturaEnergia').classList.add('active');
}

async function salvarContrato(event) {
    event.preventDefault();
    
    const data = {
        numero_contrato: document.getElementById('contratoNumero').value,
        concessionaria: document.getElementById('contratoConcessionaria').value,
        unidade_consumidora: document.getElementById('contratoUnidade').value,
        modalidade_tarifaria: document.getElementById('contratoModalidade').value,
        tensao: document.getElementById('contratoTensao').value,
        data_inicio: document.getElementById('contratoDataInicio').value,
        data_fim: document.getElementById('contratoDataFim').value || null
    };
    
    try {
        await api.criarContrato(data);
        showToast('Contrato criado com sucesso!', 'success');
        fecharModal('modalContrato');
        carregarContratos();
    } catch (error) {
        console.error('Erro ao criar contrato:', error);
        showToast('Erro ao criar contrato', 'error');
    }
}

async function salvarFaturaEnergia(event) {
    event.preventDefault();
    
    const data = {
        contrato_id: parseInt(document.getElementById('faturaEnergiaContrato').value),
        mes_referencia: document.getElementById('faturaEnergiaMes').value,
        data_vencimento: document.getElementById('faturaEnergiaVencimento').value,
        consumo_kwh: parseFloat(document.getElementById('faturaEnergiaConsumo').value),
        valor_total: parseFloat(document.getElementById('faturaEnergiaValor').value),
        bandeira_ativa: document.getElementById('faturaEnergiaBandeira').value || null,
        status: 'pendente'
    };
    
    if (!data.contrato_id) {
        showToast('Selecione um contrato', 'error');
        return;
    }
    
    try {
        await api.criarFaturaEnergia(data);
        showToast('Fatura de energia criada com sucesso!', 'success');
        fecharModal('modalFaturaEnergia');
        carregarFaturasEnergia();
    } catch (error) {
        console.error('Erro ao criar fatura de energia:', error);
        showToast('Erro ao criar fatura de energia', 'error');
    }
}

async function verAnalise(faturaId) {
    try {
        const analise = await api.getAnaliseEnergia(faturaId);
        if (analise) {
            alert(`
                📊 Análise da Fatura de Energia
                
                Consumo: ${analise.consumo_mes_atual?.toFixed(2) || 'N/A'} kWh
                Variação Consumo: ${analise.variacao_consumo?.toFixed(2) || 'N/A'}%
                Valor: ${formatMoney(analise.valor_mes_atual || 0)}
                Variação Valor: ${analise.variacao_valor?.toFixed(2) || 'N/A'}%
                Preço Médio: ${formatMoney(analise.preco_medio_kwh || 0)}/kWh
                
                ${analise.alertas ? `⚠️ Alertas: ${analise.alertas}` : ''}
                ${analise.recomendacoes ? `💡 Recomendações: ${analise.recomendacoes}` : ''}
            `);
        } else {
            showToast('Análise não disponível para esta fatura', 'info');
        }
    } catch (error) {
        console.error('Erro ao carregar análise:', error);
        showToast('Erro ao carregar análise', 'error');
    }
}

// Fechar modais ao clicar fora
document.addEventListener('click', function(event) {
    ['modalContrato', 'modalFaturaEnergia'].forEach(id => {
        const modal = document.getElementById(id);
        if (event.target === modal) {
            fecharModal(id);
        }
    });
});