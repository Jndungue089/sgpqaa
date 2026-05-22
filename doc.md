# Documentacao Viva do SGPQAA

## 1. O que e este documento

Este ficheiro vai acompanhar o desenvolvimento do sistema e explicar tudo de forma simples.
O objectivo e ajudar a banca a perceber:

- o que o sistema faz
- porque cada parte foi criada
- como o codigo esta organizado
- como os pagamentos sao simulados

Sempre que fizermos uma alteracao importante, vamos registar aqui.

## 2. Visao geral do sistema

Nome do sistema: **SGPQAA**  
Significado: **Sistema de Gestao de Pagamento de Quotas dos Associados da ANATA**

Este sistema esta a ser construido com **Django**, um framework Python que ajuda a criar
aplicacoes web organizadas, seguras e faceis de manter.

## 3. Primeiras decisoes tecnicas

### 3.1 Porque usar Django

Escolhemos Django porque ele ja traz:

- sistema de rotas
- painel administrativo
- integracao com base de dados
- sistema de autenticacao
- separacao clara entre logica, interface e dados

Isto e importante num trabalho escolar porque reduz improvisos e deixa o projecto com cara
de sistema real.

### 3.2 Base de dados

A base de dados final do projecto sera **MySQL**.

Nesta fase inicial, o projecto ficou preparado de duas formas:

- quando existirem variaveis de ambiente do MySQL, o Django usara MySQL
- quando isso ainda nao estiver configurado, o sistema pode arrancar com SQLite para facilitar o desenvolvimento local

Isto permite comecar ja, sem bloquear o trabalho, e no final ligamos ao MySQL.

Variaveis previstas para a ligacao final:

- `MYSQL_DATABASE`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`

### 3.3 Pagamentos

Nao teremos integracao real com Multicaixa ou outro gateway.
Em vez disso, vamos simular muito bem o processo, com:

- pagamento em dinheiro
- pagamento por Multicaixa simulado
- validacao por Tesoureiro
- estado do pagamento
- emissao de recibo numa fase seguinte

## 4. Estrutura inicial criada

Nesta primeira etapa, montamos:

- projecto Django base
- app principal chamada `portal`
- configuracao de `templates`
- configuracao de ficheiros estaticos (`static`)
- landing page inicial
- configuracao inicial para MySQL
- modelos de dados principais
- inicio desta documentacao viva

## 5. Modelos pensados desde o inicio

Criamos os modelos principais para representar o negocio:

### 5.1 `MemberProfile`

Guarda os dados do associado e o seu papel no sistema:

- Associado
- Tesoureiro
- Administrador

### 5.2 `Vehicle`

Guarda as viaturas ligadas a cada associado.

### 5.3 `QuotaConfig`

Guarda o valor da quota e possiveis multas.
Isto vai permitir mudar o valor no futuro sem destruir o historico.

### 5.4 `MonthlyQuota`

Representa a quota mensal de uma viatura.
Cada quota tem:

- mes de referencia
- data de vencimento
- valor
- estado

### 5.5 `PaymentRecord`

Representa o pagamento feito para uma quota.
Nesta tabela vamos registar:

- metodo de pagamento
- valor pago
- data
- referencia simulada
- estado da validacao

## 6. Landing page inicial

A landing page foi criada para ser a porta de entrada do sistema.
Ela mostra:

- o nome do projecto
- o objectivo do sistema
- os perfis de utilizador
- a ideia de simulacao de pagamentos
- o estado actual da implementacao

Esta pagina ajuda muito na apresentacao porque, antes mesmo do login, a banca consegue
entender o que esta a ser demonstrado.

## 7. Historico de alteracoes

### Alteracao 1

Data: 22 de Maio de 2026

Foi feito:

- leitura do `project.md`
- definicao de Django como base oficial do sistema
- criacao da app `portal`
- configuracao inicial do projecto para templates e ficheiros estaticos
- preparacao da ligacao futura com MySQL
- criacao dos modelos principais
- criacao da primeira landing page
- criacao deste `doc.md`

### Alteracao 2

Data: 22 de Maio de 2026

Foi feito:

- criacao de um `manage.py` na raiz do workspace
- simplificacao do arranque do servidor Django usando sempre o `venv` da raiz

Comando recomendado para desenvolvimento local:

```bash
./.venv/bin/python manage.py runserver
```

Observacao:

O comando `django-admin runserver` sozinho pode falhar porque ele nao sabe automaticamente
qual projecto Django deve carregar. O `manage.py` existe exactamente para resolver isso.

### Alteracao 3

Data: 22 de Maio de 2026

Foi feito:

- simplificacao da landing page
- mudanca do tom visual para algo mais comercial e directo
- remocao de textos com explicacao tecnica no frontend

Decisao:

A pagina inicial deve parecer uma apresentacao simples do produto, como uma landing page
que vende a ideia do sistema, e nao uma pagina a explicar arquitetura ou desenvolvimento.

## 8. Proximos passos previstos

Nas proximas etapas, vamos construir:

- autenticacao
- registo de associados
- registo de viaturas
- dashboard por perfil
- simulacao de pagamento
- validacao pelo tesoureiro
- recibo
- relatorios
