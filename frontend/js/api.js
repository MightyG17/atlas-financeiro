// API Configuration
const API_BASE_URL = 'http://localhost:8000';
let authToken = localStorage.getItem('authToken');

// Helper para requisições
async function apiRequest(endpoint, method = 'GET', body = null, requiresAuth = true) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
    };

    if (requiresAuth) {
        const token = getAuthToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        } else {
            throw new Error('Token não encontrado. Faça login novamente.');
        }
    }

    const options = {
        method,
        headers,
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, options);
        
        if (response.status === 401) {
            // Token expirado ou inválido
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            window.location.href = 'login.html';
            throw new Error('Sessão expirada. Faça login novamente.');
        }

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.message || 'Erro na requisição');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Função para pegar o token
function getAuthToken() {
    if (!authToken) {
        authToken = localStorage.getItem('authToken');
    }
    return authToken;
}

// Função para setar o token
function setAuthToken(token) {
    authToken = token;
    if (token) {
        localStorage.setItem('authToken', token);
    } else {
        localStorage.removeItem('authToken');
    }
}

// Função para pegar os dados do usuário
function getUserData() {
    const data = localStorage.getItem('userData');
    return data ? JSON.parse(data) : null;
}

// Função para setar os dados do usuário
function setUserData(data) {
    localStorage.setItem('userData', JSON.stringify(data));
}

// API Endpoints

// Autenticação
async function login(email, password) {
    try {
        const data = await apiRequest('/auth/login', 'POST', { email, senha: password }, false);
        
        setAuthToken(data.access_token);
        setUserData({
            id: data.usuario_id,
            nome: data.nome,
            email: data.email
        });
        
        return { success: true, data };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

async function cadastrar(nome, email, password) {
    try {
        const data = await apiRequest('/auth/cadastrar', 'POST', { nome, email, senha: password }, false);
        
        setAuthToken(data.access_token);
        setUserData({
            id: data.usuario_id,
            nome: data.nome,
            email: data.email
        });
        
        return { success: true, data };
    } catch (error) {
        return { success: false, message: error.message };
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    authToken = null;
    window.location.href = 'login.html';
}

function checkAuth() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Lançamentos
async function getLancamentos(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    const endpoint = `/lancamentos/${params ? '?' + params : ''}`;
    return await apiRequest(endpoint);
}

async function criarLancamento(data) {
    return await apiRequest('/lancamentos/', 'POST', data);
}

async function atualizarLancamento(id, data) {
    return await apiRequest(`/lancamentos/${id}`, 'PUT', data);
}

async function deletarLancamento(id) {
    return await apiRequest(`/lancamentos/${id}`, 'DELETE');
}

async function getResumoPeriodo(dataInicio, dataFim) {
    return await apiRequest(`/lancamentos/resumo/periodo?data_inicio=${dataInicio}&data_fim=${dataFim}`);
}

// Faturas
async function getFaturas(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    const endpoint = `/faturas/${params ? '?' + params : ''}`;
    return await apiRequest(endpoint);
}

async function criarFatura(data) {
    return await apiRequest('/faturas/', 'POST', data);
}

async function atualizarFatura(id, data) {
    return await apiRequest(`/faturas/${id}`, 'PUT', data);
}

async function deletarFatura(id) {
    return await apiRequest(`/faturas/${id}`, 'DELETE');
}

// Energia
async function getContratos(ativo = true) {
    return await apiRequest(`/api/v1/energia/contratos?ativo=${ativo}`);
}

async function criarContrato(data) {
    return await apiRequest('/api/v1/energia/contratos', 'POST', data);
}

async function getFaturasEnergia(filtros = {}) {
    const params = new URLSearchParams(filtros).toString();
    const endpoint = `/api/v1/energia/faturas/${params ? '?' + params : ''}`;
    return await apiRequest(endpoint);
}

async function criarFaturaEnergia(data) {
    return await apiRequest('/api/v1/energia/faturas', 'POST', data);
}

async function getAnaliseEnergia(faturaId) {
    return await apiRequest(`/api/v1/energia/analises/${faturaId}`);
}

// Grupos
async function getGrupos(status = null) {
    const params = status ? `?status=${status}` : '';
    return await apiRequest(`/grupos/${params}`);
}

async function criarGrupo(data) {
    return await apiRequest('/grupos/', 'POST', data);
}

// Contabilidade
async function getPlanoContas(tipo = null, ativo = true) {
    const params = new URLSearchParams();
    if (tipo) params.append('tipo', tipo);
    params.append('ativo', ativo);
    return await apiRequest(`/contabilidade/plano-contas?${params.toString()}`);
}

async function criarPlanoConta(data) {
    return await apiRequest('/contabilidade/plano-contas', 'POST', data);
}

async function getBalancoPeriodo(dataInicio, dataFim) {
    return await apiRequest(`/contabilidade/balanco-periodo?data_inicio=${dataInicio}&data_fim=${dataFim}`);
}

// Dashboard
async function getResumoCaixa(dataReferencia = null) {
    const params = dataReferencia ? `?data_referencia=${dataReferencia}` : '';
    return await apiRequest(`/caixa/resumo${params}`);
}

// Export
window.api = {
    login,
    cadastrar,
    logout,
    checkAuth,
    getAuthToken,
    getUserData,
    
    getLancamentos,
    criarLancamento,
    atualizarLancamento,
    deletarLancamento,
    getResumoPeriodo,
    
    getFaturas,
    criarFatura,
    atualizarFatura,
    deletarFatura,
    
    getContratos,
    criarContrato,
    getFaturasEnergia,
    criarFaturaEnergia,
    getAnaliseEnergia,
    
    getGrupos,
    criarGrupo,
    
    getPlanoContas,
    criarPlanoConta,
    getBalancoPeriodo,
    
    getResumoCaixa
};