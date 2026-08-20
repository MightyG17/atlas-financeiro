-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/08/2026 às 02:52
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `atlas_financeiro`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `analises_fatura_energia`
--

CREATE TABLE `analises_fatura_energia` (
  `id` int(11) NOT NULL,
  `fatura_id` int(11) NOT NULL,
  `consumo_kwh` decimal(10,2) DEFAULT NULL,
  `valor_kwh` decimal(10,4) DEFAULT NULL,
  `inconsistencias` text DEFAULT NULL,
  `sugestao_economia` text DEFAULT NULL,
  `status_analise` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `analise_fatura_energia`
--

CREATE TABLE `analise_fatura_energia` (
  `id` int(11) NOT NULL,
  `fatura_id` int(11) NOT NULL,
  `consumo_mes_anterior` float DEFAULT NULL,
  `consumo_mes_atual` float DEFAULT NULL,
  `variacao_consumo` float DEFAULT NULL,
  `valor_mes_anterior` float DEFAULT NULL,
  `valor_mes_atual` float DEFAULT NULL,
  `variacao_valor` float DEFAULT NULL,
  `consumo_medio_ultimos_3` float DEFAULT NULL,
  `consumo_medio_ultimos_6` float DEFAULT NULL,
  `consumo_medio_ultimos_12` float DEFAULT NULL,
  `preco_medio_kwh` float DEFAULT NULL,
  `tarifa_mais_vantajosa` varchar(50) DEFAULT NULL,
  `economia_potencial` float DEFAULT NULL,
  `alertas` text DEFAULT NULL,
  `recomendacoes` text DEFAULT NULL,
  `data_analise` date NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `contratos_energia`
--

CREATE TABLE `contratos_energia` (
  `id` int(11) NOT NULL,
  `numero_contrato` varchar(100) NOT NULL,
  `distribuidora` varchar(100) NOT NULL,
  `tarifa_kwh` decimal(10,4) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `contrato_energia`
--

CREATE TABLE `contrato_energia` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `numero_contrato` varchar(50) NOT NULL,
  `concessionaria` varchar(255) NOT NULL,
  `unidade_consumidora` varchar(50) NOT NULL,
  `modalidade_tarifaria` varchar(50) NOT NULL,
  `tensao` varchar(20) NOT NULL,
  `subgrupo` varchar(20) DEFAULT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `despesas_grupo`
--

CREATE TABLE `despesas_grupo` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `descricao` text NOT NULL,
  `valor` decimal(15,2) NOT NULL,
  `data_despesa` date NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `pago_por` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `divisoes_despesa`
--

CREATE TABLE `divisoes_despesa` (
  `id` int(11) NOT NULL,
  `despesa_id` int(11) NOT NULL,
  `participante_id` int(11) NOT NULL,
  `valor_proporcional` decimal(15,2) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `faturas_concessionaria`
--

CREATE TABLE `faturas_concessionaria` (
  `id` int(11) NOT NULL,
  `concessionaria` varchar(100) NOT NULL,
  `mes_referencia` varchar(20) NOT NULL,
  `data_vencimento` date NOT NULL,
  `valor_total` decimal(15,2) NOT NULL,
  `status_pagamento` varchar(50) DEFAULT NULL,
  `observacoes` text DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `faturas_concessionarias`
--

CREATE TABLE `faturas_concessionarias` (
  `id` int(11) NOT NULL,
  `codigo_barras` varchar(50) NOT NULL,
  `valor` decimal(15,2) NOT NULL,
  `data_vencimento` date NOT NULL,
  `data_pagamento` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `descricao` text DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `faturas_energia`
--

CREATE TABLE `faturas_energia` (
  `id` int(11) NOT NULL,
  `contrato_id` int(11) NOT NULL,
  `mes_referencia` varchar(20) NOT NULL,
  `consumo_kwh` decimal(10,2) NOT NULL,
  `valor_total` decimal(15,2) NOT NULL,
  `data_vencimento` date NOT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `fatura_energia`
--

CREATE TABLE `fatura_energia` (
  `id` int(11) NOT NULL,
  `contrato_id` int(11) NOT NULL,
  `mes_referencia` date NOT NULL,
  `data_vencimento` date NOT NULL,
  `codigo_barras` varchar(50) DEFAULT NULL,
  `numero_fatura` varchar(50) DEFAULT NULL,
  `consumo_kwh` float NOT NULL,
  `valor_total` float NOT NULL,
  `valor_tusd` float DEFAULT NULL,
  `valor_te` float DEFAULT NULL,
  `valor_bandeira` float DEFAULT NULL,
  `valor_iluminacao_publica` float DEFAULT NULL,
  `valor_icms` float DEFAULT NULL,
  `valor_pis_cofins` float DEFAULT NULL,
  `valor_contribuicao` float DEFAULT NULL,
  `bandeira_ativa` varchar(20) DEFAULT NULL,
  `fk_analise` int(11) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `data_pagamento` date DEFAULT NULL,
  `arquivo_original` varchar(500) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `grupos_eventos`
--

CREATE TABLE `grupos_eventos` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `descricao` text DEFAULT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `criado_por` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `lancamentos`
--

CREATE TABLE `lancamentos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `perfil_id` int(11) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `valor` decimal(15,2) NOT NULL,
  `data_lancamento` date NOT NULL,
  `data_vencimento` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `logs_energia`
--

CREATE TABLE `logs_energia` (
  `id` int(11) NOT NULL,
  `fatura_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `acao` varchar(100) NOT NULL,
  `detalhes` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `logs_energia`
--

INSERT INTO `logs_energia` (`id`, `fatura_id`, `usuario_id`, `acao`, `detalhes`, `created_at`) VALUES
(1, NULL, 1, 'UPLOAD_FATURA', 'Arquivo: 2021_08.pdf, Contrato: None', '2026-08-19 10:34:06'),
(2, NULL, 1, 'UPLOAD_FATURA', 'Arquivo: 2021_08.pdf, Contrato: None', '2026-08-19 10:55:56'),
(3, NULL, 1, 'UPLOAD_FATURA', 'Arquivo: 2021_08.pdf, Contrato: None', '2026-08-19 11:06:52'),
(4, NULL, 1, 'UPLOAD_FATURA', 'Arquivo: 2026_03.pdf, Contrato: None', '2026-08-19 11:23:19');

-- --------------------------------------------------------

--
-- Estrutura para tabela `log_energia`
--

CREATE TABLE `log_energia` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `acao` varchar(100) NOT NULL,
  `detalhes` text DEFAULT NULL,
  `ip_origem` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `participantes_grupo`
--

CREATE TABLE `participantes_grupo` (
  `id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `papel` varchar(50) DEFAULT NULL,
  `joined_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `perfis_financeiros`
--

CREATE TABLE `perfis_financeiros` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `saldo_inicial` decimal(15,2) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `plano_contas`
--

CREATE TABLE `plano_contas` (
  `id` int(11) NOT NULL,
  `codigo` varchar(20) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `pai_id` int(11) DEFAULT NULL,
  `nivel` int(11) DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tarifas_bandeira`
--

CREATE TABLE `tarifas_bandeira` (
  `id` int(11) NOT NULL,
  `cor` varchar(50) NOT NULL,
  `adicional_kwh` decimal(10,4) NOT NULL,
  `mes_referencia` varchar(20) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tarifa_bandeira`
--

CREATE TABLE `tarifa_bandeira` (
  `id` int(11) NOT NULL,
  `bandeira` varchar(20) NOT NULL,
  `valor_kwh` float NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `ativo` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `senha_hash` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Despejando dados para a tabela `usuarios`
--

INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha_hash`, `created_at`, `updated_at`) VALUES
(1, 'Jardel de Avelar Teixeira', 'jardelteixeira41@gmail.com', '$2b$12$04D14jejrfb9bcD6SSPDHeC/zmGrkLafG8UFywTy8MAlWP0cw6iNq', '2026-08-17 19:06:49', NULL),
(3, 'Avellar Teixeira', 'avellar789@gmail.com', '$2b$12$qQsqQ.DCrP0MrKfJ9Vx4L.lxB8tZZ/WxSrLSxTQS27.Kw7IhoKjzy', '2026-08-17 21:32:01', NULL),
(4, 'Usuario Teste', 'teste@email.com', '$2b$12$Aq4UGpl5FJFDbQwrYBccZ..RLjJcfNWhySxVr11CLwD65rbyKux5W', '2026-08-17 22:23:30', NULL);

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `analises_fatura_energia`
--
ALTER TABLE `analises_fatura_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fatura_id` (`fatura_id`),
  ADD KEY `ix_analises_fatura_energia_id` (`id`);

--
-- Índices de tabela `analise_fatura_energia`
--
ALTER TABLE `analise_fatura_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_analise_fatura_energia_id` (`id`);

--
-- Índices de tabela `contratos_energia`
--
ALTER TABLE `contratos_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_contratos_energia_id` (`id`);

--
-- Índices de tabela `contrato_energia`
--
ALTER TABLE `contrato_energia`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_contrato` (`numero_contrato`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_contrato_energia_id` (`id`);

--
-- Índices de tabela `despesas_grupo`
--
ALTER TABLE `despesas_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `pago_por` (`pago_por`),
  ADD KEY `ix_despesas_grupo_id` (`id`);

--
-- Índices de tabela `divisoes_despesa`
--
ALTER TABLE `divisoes_despesa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `despesa_id` (`despesa_id`),
  ADD KEY `participante_id` (`participante_id`),
  ADD KEY `ix_divisoes_despesa_id` (`id`);

--
-- Índices de tabela `faturas_concessionaria`
--
ALTER TABLE `faturas_concessionaria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_faturas_concessionaria_id` (`id`);

--
-- Índices de tabela `faturas_concessionarias`
--
ALTER TABLE `faturas_concessionarias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_barras` (`codigo_barras`),
  ADD KEY `ix_faturas_concessionarias_id` (`id`);

--
-- Índices de tabela `faturas_energia`
--
ALTER TABLE `faturas_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_faturas_energia_id` (`id`);

--
-- Índices de tabela `fatura_energia`
--
ALTER TABLE `fatura_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_fatura_energia_id` (`id`);

--
-- Índices de tabela `grupos_eventos`
--
ALTER TABLE `grupos_eventos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `criado_por` (`criado_por`),
  ADD KEY `ix_grupos_eventos_id` (`id`);

--
-- Índices de tabela `lancamentos`
--
ALTER TABLE `lancamentos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `perfil_id` (`perfil_id`),
  ADD KEY `ix_lancamentos_id` (`id`);

--
-- Índices de tabela `logs_energia`
--
ALTER TABLE `logs_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fatura_id` (`fatura_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_logs_energia_id` (`id`);

--
-- Índices de tabela `log_energia`
--
ALTER TABLE `log_energia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_log_energia_id` (`id`);

--
-- Índices de tabela `participantes_grupo`
--
ALTER TABLE `participantes_grupo`
  ADD PRIMARY KEY (`id`),
  ADD KEY `grupo_id` (`grupo_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_participantes_grupo_id` (`id`);

--
-- Índices de tabela `perfis_financeiros`
--
ALTER TABLE `perfis_financeiros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `ix_perfis_financeiros_id` (`id`);

--
-- Índices de tabela `plano_contas`
--
ALTER TABLE `plano_contas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `pai_id` (`pai_id`),
  ADD KEY `ix_plano_contas_id` (`id`);

--
-- Índices de tabela `tarifas_bandeira`
--
ALTER TABLE `tarifas_bandeira`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_tarifas_bandeira_id` (`id`);

--
-- Índices de tabela `tarifa_bandeira`
--
ALTER TABLE `tarifa_bandeira`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_tarifa_bandeira_id` (`id`);

--
-- Índices de tabela `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_usuarios_email` (`email`),
  ADD KEY `ix_usuarios_id` (`id`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `analises_fatura_energia`
--
ALTER TABLE `analises_fatura_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `analise_fatura_energia`
--
ALTER TABLE `analise_fatura_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `contratos_energia`
--
ALTER TABLE `contratos_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `contrato_energia`
--
ALTER TABLE `contrato_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `despesas_grupo`
--
ALTER TABLE `despesas_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `divisoes_despesa`
--
ALTER TABLE `divisoes_despesa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `faturas_concessionaria`
--
ALTER TABLE `faturas_concessionaria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `faturas_concessionarias`
--
ALTER TABLE `faturas_concessionarias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `faturas_energia`
--
ALTER TABLE `faturas_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `fatura_energia`
--
ALTER TABLE `fatura_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `grupos_eventos`
--
ALTER TABLE `grupos_eventos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `lancamentos`
--
ALTER TABLE `lancamentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `logs_energia`
--
ALTER TABLE `logs_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `log_energia`
--
ALTER TABLE `log_energia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `participantes_grupo`
--
ALTER TABLE `participantes_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `perfis_financeiros`
--
ALTER TABLE `perfis_financeiros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `plano_contas`
--
ALTER TABLE `plano_contas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tarifas_bandeira`
--
ALTER TABLE `tarifas_bandeira`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tarifa_bandeira`
--
ALTER TABLE `tarifa_bandeira`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `analises_fatura_energia`
--
ALTER TABLE `analises_fatura_energia`
  ADD CONSTRAINT `analises_fatura_energia_ibfk_1` FOREIGN KEY (`fatura_id`) REFERENCES `faturas_energia` (`id`);

--
-- Restrições para tabelas `contratos_energia`
--
ALTER TABLE `contratos_energia`
  ADD CONSTRAINT `contratos_energia_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `contrato_energia`
--
ALTER TABLE `contrato_energia`
  ADD CONSTRAINT `contrato_energia_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `despesas_grupo`
--
ALTER TABLE `despesas_grupo`
  ADD CONSTRAINT `despesas_grupo_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos_eventos` (`id`),
  ADD CONSTRAINT `despesas_grupo_ibfk_2` FOREIGN KEY (`pago_por`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `divisoes_despesa`
--
ALTER TABLE `divisoes_despesa`
  ADD CONSTRAINT `divisoes_despesa_ibfk_1` FOREIGN KEY (`despesa_id`) REFERENCES `despesas_grupo` (`id`),
  ADD CONSTRAINT `divisoes_despesa_ibfk_2` FOREIGN KEY (`participante_id`) REFERENCES `participantes_grupo` (`id`);

--
-- Restrições para tabelas `faturas_concessionaria`
--
ALTER TABLE `faturas_concessionaria`
  ADD CONSTRAINT `faturas_concessionaria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `faturas_energia`
--
ALTER TABLE `faturas_energia`
  ADD CONSTRAINT `faturas_energia_ibfk_1` FOREIGN KEY (`contrato_id`) REFERENCES `contratos_energia` (`id`);

--
-- Restrições para tabelas `fatura_energia`
--
ALTER TABLE `fatura_energia`
  ADD CONSTRAINT `fatura_energia_ibfk_1` FOREIGN KEY (`contrato_id`) REFERENCES `contrato_energia` (`id`);

--
-- Restrições para tabelas `grupos_eventos`
--
ALTER TABLE `grupos_eventos`
  ADD CONSTRAINT `grupos_eventos_ibfk_1` FOREIGN KEY (`criado_por`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `lancamentos`
--
ALTER TABLE `lancamentos`
  ADD CONSTRAINT `lancamentos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `lancamentos_ibfk_2` FOREIGN KEY (`perfil_id`) REFERENCES `perfis_financeiros` (`id`);

--
-- Restrições para tabelas `logs_energia`
--
ALTER TABLE `logs_energia`
  ADD CONSTRAINT `logs_energia_ibfk_1` FOREIGN KEY (`fatura_id`) REFERENCES `faturas_energia` (`id`),
  ADD CONSTRAINT `logs_energia_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `participantes_grupo`
--
ALTER TABLE `participantes_grupo`
  ADD CONSTRAINT `participantes_grupo_ibfk_1` FOREIGN KEY (`grupo_id`) REFERENCES `grupos_eventos` (`id`),
  ADD CONSTRAINT `participantes_grupo_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `perfis_financeiros`
--
ALTER TABLE `perfis_financeiros`
  ADD CONSTRAINT `perfis_financeiros_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Restrições para tabelas `plano_contas`
--
ALTER TABLE `plano_contas`
  ADD CONSTRAINT `plano_contas_ibfk_1` FOREIGN KEY (`pai_id`) REFERENCES `plano_contas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
