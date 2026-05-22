# SGPQAA

Sistema de Gestao de Pagamento de Quotas dos Associados da ANATA.

Este projecto foi desenvolvido em Django para fins escolares e simula a gestao de:

- associados
- viaturas
- quotas mensais
- pagamentos em maos
- transferencias bancarias com comprovante em PDF
- validacao pela tesouraria
- recibos
- relatorios de debitos e multas

## Visao Geral

O sistema foi pensado para funcionar como uma aplicacao web local, clara e organizada, com
tres papeis principais:

- `Associado`
- `Tesoureiro`
- `Administrador`

O associado regista viaturas, consulta quotas, envia comprovantes e acompanha o historico.
O tesoureiro valida pagamentos, acompanha debitos e usa relatorios financeiros.
O administrador define o valor da quota e gere o sistema pelo painel admin do Django.

## Principais Funcionalidades

- landing page institucional
- autenticacao com Django
- registo publico de associados
- criacao de administrador por CLI
- registo e desactivacao logica de viaturas
- geracao automatica de quotas a partir da configuracao activa
- botao explicito no admin para gerar quotas do mes
- pagamento em maos marcado pela tesouraria
- transferencia bancaria com upload de comprovante PDF
- revisao do comprovativo antes da validacao
- recibo de pagamento validado
- historico de pagamentos
- relatorio de debitos e multas por atraso
- pagina 404 personalizada
- pagina de sessao expirada

## Tecnologias

- Python
- Django
- MySQL
- PyMySQL
- HTML
- CSS

## Estrutura do Projecto

```text
sgpqaa/
├── manage.py
├── .env
├── doc.md
├── README.md
└── sgpqaa/
    ├── manage.py
    ├── db.sqlite3
    ├── portal/
    ├── static/
    ├── templates/
    └── sgpqaa/
```

## Requisitos

Antes de executar, garanta que tem:

- Python 3
- MySQL activo
- ambiente virtual `.venv` na raiz do workspace

## Configuracao da Base de Dados

O projecto usa MySQL e le as configuracoes do ficheiro `.env`.

Exemplo:

```env
MYSQL_DATABASE=sgpqaa
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

## Instalacao

1. Clonar o repositorio
2. Criar e activar o ambiente virtual
3. Instalar as dependencias
4. Configurar o `.env`
5. Aplicar as migrations

Exemplo:

```bash
python -m venv .venv
source .venv/bin/activate
pip install django pymysql
python manage.py migrate
```

## Execucao

Para iniciar o servidor:

```bash
./.venv/bin/python manage.py runserver
```

Depois, abrir no browser:

```text
http://127.0.0.1:8000/
```

## Criar Administrador

O administrador nao deve ser criado publicamente.
Por seguranca, deve ser criado pela linha de comando:

```bash
./.venv/bin/python manage.py createsuperuser
```

Depois disso, o acesso administrativo fica em:

```text
http://127.0.0.1:8000/admin/
```

## Papeis do Sistema

### Associado

- cria conta
- regista viaturas
- consulta quotas
- submete comprovantes em PDF
- acompanha pagamentos
- visualiza recibos

### Tesoureiro

- usa dashboard da tesouraria
- confirma pagamento em maos
- revê comprovativos PDF
- valida transferencias
- acompanha relatorios de debitos e multas

### Administrador

- entra no painel admin do Django
- define o valor da quota
- gere utilizadores e perfis
- cria ou promove tesoureiros
- pode accionar a rotina explicita de geracao de quotas

## Fluxo Principal do Sistema

1. O administrador define a configuracao da quota.
2. O sistema gera quotas para viaturas activas.
3. O associado consulta as suas quotas.
4. O associado paga em maos ou por transferencia.
5. Se for transferencia, envia comprovante PDF.
6. O tesoureiro revê e valida.
7. O sistema emite recibo.

## Testes

Para correr os testes:

```bash
./.venv/bin/python manage.py test portal
```

## Documentacao Complementar

Existe um ficheiro adicional com explicacao detalhada do sistema em linguagem simples:

- [doc.md](doc.md)

Esse documento foi preparado para defesa escolar e explica:

- arquitectura
- modelos
- relacoes
- autenticacao
- pagamentos
- relatorios
- decisoes tecnicas

## Observacoes

- os comprovantes de transferencia devem ser enviados em PDF
- o pagamento em maos so pode ser marcado por tesoureiro ou administrador
- o projecto foi pensado para demonstracao local
- a documentacao foi escrita para ser acessivel tambem a pessoas leigas

## Estado Actual

O sistema ja cobre a base funcional principal do projecto:

- autenticacao
- viaturas
- quotas
- pagamentos
- recibos
- historico
- debitos
- relatorios da tesouraria

## Autor

Projecto academico desenvolvido para apresentacao escolar.
