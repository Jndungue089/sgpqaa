# Roadmap de Implementação — Software de Gestão de Quotas ANATA

**Projecto:** Sistema de Gestão de Pagamento de Quotas dos Associados da ANATA  
**Equipa:** Dumildes Muanha · Emanuel Congolo · Flora Jinga  
**Instituição:** Instituto Médio Comercial de Luanda — Turma ANI, 13ª Classe  
**Orientador:** Prof. Marcial Mbango

---

## Visão Geral das Fases

| Fase | Nome | Período estimado | Estado |
|------|------|-----------------|--------|
| 1 | MVP — Base do sistema | Semanas 1–3 | 🔧 Em desenvolvimento |
| 2 | Pagamentos e notificações | Semanas 4–5 | ⏳ Planeado |
| 3 | Relatórios e gestão avançada | Semanas 6–7 | ⏳ Planeado |
| 4 | Integração e entrega final | Semana 8 | ⏳ Planeado |

---

## Fase 1 — MVP: Base do Sistema

> Objectivo: ter o sistema funcional com as acções essenciais — registo, login e pagamento manual.

### 1.1 Estrutura de ficheiros e configuração

- [ ] Criar estrutura de pastas (`/pages`, `/assets/css`, `/assets/js`, `/data`)
- [ ] Definir ficheiro `config.js` com constantes (valor da quota, nome da associação)
- [ ] Configurar armazenamento local (`localStorage`) para persistência de dados

### 1.2 Autenticação (UC1)

- [ ] Página `login.html` — formulário de login (email + palavra-passe)
- [ ] Página `registo.html` — criação de conta de membro
- [ ] Validação de campos no lado do cliente (JavaScript)
- [ ] Sessão de utilizador com `sessionStorage` (manter login activo)
- [ ] Diferenciação de perfis: Membro / Tesoureiro / Administrador

### 1.3 Registo de veículo (UC2)

- [ ] Formulário para registar carro (placa, modelo, ano, cor)
- [ ] Associar carro ao membro autenticado
- [ ] Listagem dos carros do membro (`Meus Carros`)
- [ ] Funcionalidade de remover carro

### 1.4 Pagamento de quota mensal (UC3)

- [ ] Gerar automaticamente a quota do mês corrente para cada carro
- [ ] Página `pagar-quota.html` com valor e data de vencimento
- [ ] Opção de pagamento em dinheiro (registo manual pelo Tesoureiro)
- [ ] Opção de pagamento via Multicaixa (simulação de confirmação)
- [ ] Marcar quota como "paga" após confirmação

---

## Fase 2 — Pagamentos e Notificações

> Objectivo: automatizar alertas e melhorar o controlo financeiro.

### 2.1 Consulta de débitos (UC4)

- [ ] Página `debitos.html` mostrando quotas em atraso por carro
- [ ] Cálculo automático de juros/multas por atraso (configurável pelo Admin)
- [ ] Destaque visual para quotas vencidas há mais de 30 dias

### 2.2 Histórico de pagamentos (UC5)

- [ ] Tabela com todos os pagamentos do membro: mês, valor, data, forma de pagamento
- [ ] Filtro por período (mês/ano)
- [ ] Exportação do histórico em PDF (usando `window.print()`)

### 2.3 Validação de pagamento pelo Tesoureiro (UC6)

- [ ] Painel do Tesoureiro com lista de pagamentos pendentes de validação
- [ ] Botão "Validar" com confirmação
- [ ] Registo do nome do Tesoureiro e data/hora da validação

### 2.4 Emissão de recibo (UC7)

- [ ] Geração automática de recibo após validação
- [ ] Recibo com: nº de associado, placa do carro, mês referente, valor, data, assinatura digital (nome do Tesoureiro)
- [ ] Botão de impressão / download do recibo

---

## Fase 3 — Relatórios e Gestão Avançada

> Objectivo: dar ferramentas de decisão ao Administrador e ao Tesoureiro.

### 3.1 Relatório de inadimplência (UC8)

- [ ] Listagem de todos os membros/carros com quotas em atraso
- [ ] Filtro por staff, período e valor em dívida
- [ ] Gráfico de barras com taxa de pagamento por mês (Chart.js ou D3)
- [ ] Exportação do relatório (PDF ou impressão)

### 3.2 Gestão de membros pelo Administrador (UC9)

- [ ] Painel Admin com lista completa de membros
- [ ] Cadastrar novo membro (nome, BI, email, telefone, nº carteira, staff)
- [ ] Editar dados de membro existente
- [ ] Remover/desactivar membro (manter histórico — nunca apagar registo)
- [ ] Pesquisa e filtro por nome, staff ou número de associado

### 3.3 Definição do valor da quota (UC10)

- [ ] Formulário do Admin para definir o valor mensal da quota
- [ ] Histórico de alterações de valor com data de vigência
- [ ] Confirmação antes de aplicar novo valor

### 3.4 Geração automática de quotas (UC11)

- [ ] Script que corre no primeiro dia de cada mês (simulado via botão no Admin)
- [ ] Cria automaticamente registos de quota para todos os carros activos
- [ ] Notificação na área do membro: "A sua quota de [mês] está disponível"

---

## Fase 4 — Integração e Entrega Final

> Objectivo: testar, polir e preparar para apresentação.

### 4.1 Testes e correcção de erros

- [ ] Teste de fluxo completo (registo → login → pagar → validar → recibo)
- [ ] Teste de todos os perfis (Membro, Tesoureiro, Admin)
- [ ] Verificar responsividade em telemóvel e desktop
- [ ] Correcção de bugs encontrados

### 4.2 Melhoria da interface

- [ ] Rever consistência visual (cores, tipografia, espaçamento)
- [ ] Adicionar mensagens de sucesso/erro em todas as acções
- [ ] Página 404 e mensagem de sessão expirada
- [ ] Favicon e título correcto no browser

### 4.3 Documentação

- [ ] Comentar o código JavaScript principal
- [ ] Actualizar o relatório final (capturas de ecrã das telas finais)
- [ ] Preparar apresentação oral com demonstração ao vivo

### 4.4 Entrega

- [ ] Compactar o projecto final em `.zip`
- [ ] Garantir que o sistema funciona ao abrir `index.html` directamente (sem servidor)
- [ ] Entregar ao Professor Marcial Mbango

---

## Estrutura de Ficheiros Recomendada

```
ANATA/
├── index.html              ← Página inicial (menu principal)
├── login.html              ← Autenticação
├── registo.html            ← Criação de conta
├── pages/
│   ├── dashboard.html      ← Área do associado
│   ├── meus-carros.html    ← UC2
│   ├── pagar-quota.html    ← UC3
│   ├── debitos.html        ← UC4
│   ├── historico.html      ← UC5
│   ├── tesoureiro.html     ← UC6 + UC7
│   └── admin.html          ← UC8 + UC9 + UC10 + UC11
├── assets/
│   ├── css/
│   │   └── estilo.css
│   ├── js/
│   │   ├── auth.js
│   │   ├── quotas.js
│   │   ├── relatorios.js
│   │   └── dados.js        ← localStorage helpers
│   └── img/
│       └── logo-anata.png
└── README.md
```

---

## Prioridades Críticas para a PAP

1. **Fase 1 completa** é o mínimo aceitável para a apresentação.
2. **Emissão de recibo** (UC7) é o elemento visual mais impactante para a banca.
3. **Relatório de inadimplência** (UC8) demonstra valor prático para a ANATA real.
4. Todo o sistema deve funcionar **sem internet** (apenas `localStorage`).

---

*Luanda, 2026 — Grupo 2, Turma ANI*