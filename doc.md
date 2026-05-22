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

### 3.2.1 O que e um ficheiro `.env`

Um ficheiro `.env` e um ficheiro simples de texto onde guardamos configuracoes do sistema
em formato `NOME=valor`.

Exemplo:

```text
MYSQL_DATABASE=sgpqaa
MYSQL_USER=root
MYSQL_PASSWORD=uma_senha_aqui
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Ele nao e uma base de dados.
Ele nao e codigo Python.
Ele e apenas um local organizado para guardar configuracoes do ambiente.

### 3.2.2 Para que serve o `.env`

O `.env` serve para separar:

- o codigo do sistema
- as configuracoes do ambiente
- dados sensiveis, como senhas

Isto e util porque o mesmo sistema pode funcionar em ambientes diferentes.

Exemplo:

- no computador do programador, a senha da base pode ser uma
- no computador da escola, a senha pode ser outra
- num servidor futuro, os dados podem ser diferentes outra vez

Se essas informacoes ficassem escritas directamente no codigo, seria mais dificil mudar,
mais inseguro e menos profissional.

### 3.2.3 Porque usamos `.env` neste projecto

Neste projecto usamos `.env` por tres motivos principais:

1. Para nao escrever a senha do MySQL directamente no codigo-fonte.
2. Para permitir mudar a configuracao da base sem alterar a logica do sistema.
3. Para aproximar o projecto de uma pratica real de desenvolvimento profissional.

### 3.2.4 Quando usar um `.env`

Um `.env` deve ser usado quando o sistema tem configuracoes que podem mudar de um ambiente
para outro.

Exemplos comuns:

- nome da base de dados
- utilizador da base de dados
- senha da base de dados
- endereco do servidor
- chaves secretas
- modo de debug

### 3.2.5 Quando nao faz sentido usar `.env`

Nem tudo precisa ficar no `.env`.

Informacoes que fazem parte da logica permanente do sistema podem ficar no codigo.

Exemplos:

- nome das tabelas
- regras de negocio
- nomes das classes
- campos dos modelos

Ou seja:

- configuracao variavel vai para o `.env`
- estrutura e comportamento do sistema ficam no codigo

Preenchimento local actual:

- `MYSQL_DATABASE=sgpqaa`
- `MYSQL_USER=root`
- `MYSQL_PASSWORD` definida localmente no ficheiro `.env`
- `MYSQL_HOST=127.0.0.1`
- `MYSQL_PORT=3306`

### 3.3 Pagamentos

Nao teremos integracao real com Multicaixa ou outro gateway.
Em vez disso, vamos simular muito bem o processo, com:

- pagamento em dinheiro
- pagamento por Multicaixa simulado
- validacao por Tesoureiro
- estado do pagamento
- emissao de recibo numa fase seguinte

### 3.4 Autenticacao

Autenticacao e o processo de confirmar a identidade de quem entra no sistema.

Em linguagem simples:

- o utilizador diz quem e
- o sistema verifica se isso e verdade
- se estiver certo, o sistema permite a entrada

Exemplo pratico:

- o utilizador escreve nome de utilizador e palavra-passe
- o sistema compara esses dados com o que esta guardado na base de dados
- se os dados coincidirem, o login e aceite

### 3.4.1 Diferenca entre autenticacao e autorizacao

Estas duas ideias costumam ser confundidas, mas nao sao a mesma coisa.

#### Autenticacao

Responde a pergunta:

"Quem e esta pessoa?"

Exemplo:

- esta pessoa e realmente o utilizador `ana`

#### Autorizacao

Responde a pergunta:

"O que esta pessoa pode fazer dentro do sistema?"

Exemplo:

- um associado pode ver as suas quotas
- um tesoureiro pode validar pagamentos
- um administrador pode gerir membros e configuracoes

Ou seja:

- autenticacao confirma identidade
- autorizacao controla permissoes

### 3.4.2 O que vamos usar neste projecto

Neste projecto vamos usar a autenticacao nativa do Django.

Isso significa que o Django vai tratar:

- criacao de utilizadores
- validacao da palavra-passe
- criacao de sessao apos login
- encerramento da sessao no logout
- proteccao de paginas que exigem login

Esta foi a escolha porque:

- e segura para um projecto web escolar
- ja vem pronta no Django
- e facil de explicar
- reduz a probabilidade de erro

### 3.4.3 Como o login funciona no nosso sistema

O fluxo previsto e este:

1. O utilizador abre a pagina de login.
2. Digita o nome de utilizador e a palavra-passe.
3. O Django verifica se esse utilizador existe.
4. O Django verifica se a palavra-passe esta correcta.
5. Se estiver tudo certo, o sistema cria uma sessao.
6. Enquanto a sessao existir, o utilizador pode entrar nas paginas protegidas sem fazer login novamente.

### 3.4.4 O que e uma sessao

Uma sessao e a forma que o servidor usa para "lembrar" que aquele utilizador ja entrou.

Sem sessao, o sistema esqueceria o utilizador a cada clique.

Com a sessao:

- o utilizador faz login uma vez
- o servidor guarda essa informacao
- nas paginas seguintes, o sistema reconhece que ele continua autenticado

### 3.4.5 Como a sessao funciona tecnicamente

De forma simplificada:

1. O utilizador faz login com sucesso.
2. O servidor cria um identificador de sessao.
3. Esse identificador fica associado ao utilizador no servidor.
4. O navegador passa a enviar esse identificador em cada pedido seguinte.
5. O servidor reconhece o identificador e sabe quem e o utilizador.

### 3.4.6 O que e logout

Logout e o processo de terminar a sessao.

Quando o utilizador faz logout:

- a sessao deixa de valer
- o sistema deixa de o reconhecer como autenticado
- as paginas protegidas voltam a exigir login

### 3.4.7 Como guardamos a palavra-passe

O sistema nao deve guardar a palavra-passe em texto normal.

Em vez disso, o Django guarda uma versao protegida da palavra-passe chamada **hash**.

Isto significa:

- o sistema nao guarda a senha original visivel
- o sistema guarda um valor matematicamente transformado
- quando o utilizador tenta entrar, o Django compara a senha digitada com esse valor protegido

Esta e uma medida de seguranca essencial.

### 3.4.8 O que e JWT

JWT significa **JSON Web Token**.

E uma forma de autenticacao muito usada em APIs e sistemas onde o frontend e separado do backend.

Em vez de usar uma sessao tradicional no servidor:

- o sistema gera um token
- esse token vai para o cliente
- o cliente envia esse token nos pedidos seguintes
- o servidor valida o token para reconhecer o utilizador

### 3.4.9 Quando o JWT faz sentido

JWT costuma fazer mais sentido quando temos cenarios como:

- uma API consumida por aplicacao mobile
- frontend em React, Vue ou Angular separado do backend
- varios servicos a falar entre si
- autenticacao sem sessao tradicional no servidor

### 3.4.10 Porque nao vamos usar JWT agora

Neste momento, o nosso projecto e um sistema web tradicional em Django, com:

- backend e frontend no mesmo projecto
- templates renderizados pelo servidor
- login classico por formulario
- necessidade de simplicidade para a defesa

Por isso, usar JWT agora seria pior para este contexto, porque:

- aumentaria a complexidade
- exigiria mais explicacao tecnica
- nao traria beneficio real nesta fase
- sairia do caminho natural do Django para aplicacoes web deste tipo

### 3.4.11 Decisao tomada sobre autenticacao

Decidimos usar:

- autenticacao nativa do Django
- sessao tradicional baseada no servidor
- tabela `auth_user` do Django
- tabela `django_session` para controlo de sessoes

E decidimos nao usar, por agora:

- JWT
- OAuth
- login social
- autenticacao por telemovel

### 3.4.12 Porque esta decisao foi a melhor para o projecto

Esta decisao foi tomada porque ela oferece equilibrio entre:

- seguranca
- simplicidade
- clareza para a banca
- rapidez de desenvolvimento
- organizacao do codigo

Em resumo:

o sistema fica suficientemente profissional para a apresentacao e, ao mesmo tempo,
continua facil de explicar e manter.

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

Campos principais e significado:

- `owner`: indica a quem a viatura pertence
- `plate_number`: matricula da viatura
- `model`: modelo do carro
- `year`: ano da viatura
- `color`: cor da viatura
- `is_active`: indica se a viatura ainda esta activa no sistema

Porque a viatura e uma entidade propria:

- um associado pode ter mais de uma viatura
- cada viatura pode gerar quotas diferentes ao longo do tempo
- o sistema precisa acompanhar historico por viatura

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

### 5.6 Porque estes modelos foram escolhidos

Os modelos nao foram escolhidos por acaso.
Eles foram pensados para representar o funcionamento real do processo de quotas.

#### Decisao 1: separar `User` e `MemberProfile`

O Django ja traz uma tabela chamada `auth_user`.
Ela guarda dados gerais do utilizador, como:

- username
- password
- email

Mas o nosso sistema precisa de mais informacoes especificas da associacao, como:

- numero de associado
- BI
- staff
- papel no sistema

Por isso criamos `MemberProfile`.

Porque esta decisao foi boa:

- aproveita o sistema de autenticacao do Django
- evita recriar uma tabela de login do zero
- separa dados de acesso dos dados da associacao

#### Decisao 2: criar uma tabela propria para viaturas

Uma viatura nao podia ficar misturada com os dados do associado porque:

- um associado pode ter mais de uma viatura
- cada viatura tem vida propria dentro do sistema
- as quotas serao geradas por viatura, nao apenas por pessoa

Por isso a tabela `Vehicle` ficou separada.

#### Decisao 3: criar `QuotaConfig`

O valor da quota pode mudar com o tempo.
Se guardassemos esse valor apenas num sitio fixo, perderiamos historico.

Com `QuotaConfig`, podemos:

- saber quanto valia a quota numa determinada epoca
- mudar o valor sem destruir registos antigos
- preparar o sistema para administracao futura

#### Decisao 4: criar `MonthlyQuota`

A quota mensal precisava de existir como entidade propria porque o sistema tem de acompanhar:

- o mes a que a quota pertence
- a data de vencimento
- o valor devido
- o estado da quota

Se o pagamento fosse ligado directamente a uma viatura sem essa tabela intermediaria,
ficaria muito mais dificil controlar historico mensal.

#### Decisao 5: criar `PaymentRecord`

O pagamento tambem ficou numa tabela separada porque uma quota pode passar por etapas:

- foi gerada
- foi paga
- aguarda validacao
- foi validada ou rejeitada

Separar a quota do pagamento deixa o sistema mais claro e mais proximo de um processo real.

## 6. Tabelas do sistema e estrutura do MER

Nesta fase, o sistema usa tabelas automaticas do Django e tabelas do nosso dominio.

### 6.0 O que e um MER

MER significa **Modelo Entidade-Relacionamento**.

E uma forma de desenhar e planear a base de dados antes, ou durante, a implementacao.

Ele responde a perguntas como:

- quais sao as entidades do sistema?
- que dados cada entidade guarda?
- como essas entidades se ligam umas as outras?

No nosso caso, as entidades principais sao:

- utilizador
- perfil de associado
- viatura
- configuracao de quota
- quota mensal
- pagamento

### 6.0.1 O que e uma entidade

Uma entidade e algo importante do negocio que precisa ser guardado no sistema.

Exemplos no nosso projecto:

- um associado
- uma viatura
- uma quota
- um pagamento

Na pratica, quase sempre uma entidade vira uma tabela na base de dados.

### 6.0.2 O que e um atributo

Atributo e cada informacao guardada dentro de uma entidade.

Exemplo:

Na entidade `Vehicle`, alguns atributos sao:

- matricula
- modelo
- ano
- cor

Na pratica, os atributos viram colunas da tabela.

### 6.0.3 O que e um relacionamento

Relacionamento e a ligacao entre entidades.

Exemplo:

- um associado tem viaturas
- uma viatura tem quotas
- uma quota tem pagamentos

### 6.0.4 Porque fazer o MER antes ou durante o desenvolvimento

O MER ajuda a evitar varios problemas:

- repeticao desnecessaria de dados
- tabelas mal divididas
- confusao nas relacoes
- dificuldade para fazer consultas
- historico incompleto

Em resumo, o MER ajuda a base de dados a nascer organizada.

### 6.0.5 O que e database design

Database design, ou desenho da base de dados, e o processo de decidir:

- que tabelas vao existir
- que campos cada tabela tera
- quais campos sao obrigatorios
- quais campos devem ser unicos
- como as tabelas se relacionam
- que regras garantem consistencia dos dados

Ou seja, e o plano estrutural da base de dados.

Se o frontend e a parte que o utilizador ve, o database design e a fundacao invisivel
que sustenta o sistema inteiro.

### 6.0.6 Como funciona o desenho da base de dados neste projecto

O raciocinio seguido foi este:

1. Identificar os elementos reais do problema.
2. Transformar esses elementos em entidades.
3. Separar cada entidade numa tabela propria.
4. Ligar as tabelas por chaves estrangeiras.
5. Evitar mistura de responsabilidades.
6. Garantir historico e rastreabilidade.

#### Exemplo de aplicacao pratica

Pergunta:

"Como controlar o pagamento de quota de um carro num certo mes?"

Resposta de desenho:

- o associado fica numa tabela
- a viatura fica noutra
- a quota mensal fica noutra
- o pagamento fica noutra

Assim, o sistema consegue guardar o processo completo sem confundir os dados.

### 6.1 Tabelas automaticas do Django

O Django cria algumas tabelas de apoio ao funcionamento interno do sistema:

- `auth_user`: guarda os utilizadores do sistema
- `auth_group`: grupos de permissao
- `auth_permission`: permissoes
- `django_admin_log`: historico do painel admin
- `django_content_type`: controlo interno dos modelos
- `django_session`: sessoes activas
- `django_migrations`: registo das migrations aplicadas

Estas tabelas sao normais em sistemas Django e ajudam na autenticacao, seguranca e administracao.

### 6.2 Tabelas do negocio

#### Tabela `portal_memberprofile`

Representa o perfil funcional do utilizador dentro da associacao.

Campos principais:

- `id`
- `user_id`
- `member_number`
- `phone`
- `identity_card`
- `staff_name`
- `role`
- `is_active_member`
- `created_at`
- `updated_at`

#### Tabela `portal_vehicle`

Representa cada viatura registada por um associado.

Campos principais:

- `id`
- `owner_id`
- `plate_number`
- `model`
- `year`
- `color`
- `is_active`
- `created_at`
- `updated_at`

#### Tabela `portal_quotaconfig`

Representa a configuracao do valor das quotas.

Campos principais:

- `id`
- `amount`
- `late_fee_percentage`
- `effective_from`
- `is_active`
- `created_at`
- `updated_at`

#### Tabela `portal_monthlyquota`

Representa a quota mensal gerada para uma viatura.

Campos principais:

- `id`
- `vehicle_id`
- `reference_month`
- `due_date`
- `amount_due`
- `status`
- `generated_automatically`
- `created_at`
- `updated_at`

#### Tabela `portal_paymentrecord`

Representa o pagamento registado para uma quota.

Campos principais:

- `id`
- `quota_id`
- `method`
- `status`
- `amount_paid`
- `payment_date`
- `simulated_reference`
- `validated_by_id`
- `validated_at`
- `notes`
- `created_at`
- `updated_at`

### 6.3 Relacionamentos do MER

O MER, ou Modelo Entidade-Relacionamento, mostra como as entidades do sistema se ligam.

### 6.3.1 O que significa `1:1`

`1:1` significa **um para um**.

Quer dizer que um registo de uma tabela se liga a apenas um registo da outra tabela,
e vice-versa.

Exemplo no nosso sistema:

- um `auth_user` tem um `MemberProfile`
- um `MemberProfile` pertence a um `auth_user`

Isto faz sentido porque cada conta de acesso deve representar um unico perfil funcional.

### 6.3.2 O que significa `1:N`

`1:N` significa **um para muitos**.

Quer dizer que um registo de uma tabela pode estar ligado a varios registos de outra tabela.

Exemplo no nosso sistema:

- um associado pode ter varias viaturas
- uma viatura pode ter varias quotas mensais
- uma quota pode ter varios registos de pagamento

### 6.3.3 O que significa `N:1`

`N:1` significa **muitos para um**.

Na pratica, e a mesma relacao vista do lado contrario.

Exemplo:

- se dissermos "um associado tem varias viaturas", estamos a olhar como `1:N`
- se dissermos "varias viaturas pertencem a um associado", estamos a olhar como `N:1`

Portanto:

- `1:N` e `N:1` representam a mesma ligacao
- a diferenca esta apenas no ponto de vista de quem esta a explicar

### 6.3.4 Porque estes relacionamentos foram escolhidos

Os relacionamentos foram escolhidos para representar o funcionamento real do negocio.

Exemplos:

- um associado realmente pode ter varias viaturas
- uma viatura realmente acumula varias quotas ao longo dos meses
- uma quota pode ter registos ligados ao processo de pagamento

Se usassemos os relacionamentos errados:

- perderiamos historico
- duplicariamos dados
- dificultariamos consultas e relatorios
- o sistema ficaria menos fiel a realidade

#### Relacao 1: Utilizador e Perfil

- Um registo em `auth_user` tem um `MemberProfile`
- Um `MemberProfile` pertence a um unico `auth_user`

Isto e uma relacao **um para um (1:1)**.

#### Relacao 2: Perfil e Viatura

- Um `MemberProfile` pode ter varias viaturas
- Cada `Vehicle` pertence a um unico `MemberProfile`

Isto e uma relacao **um para muitos (1:N)**.

#### Relacao 3: Viatura e Quota Mensal

- Uma `Vehicle` pode ter varias `MonthlyQuota`
- Cada `MonthlyQuota` pertence a uma unica `Vehicle`

Isto e uma relacao **um para muitos (1:N)**.

#### Relacao 4: Quota Mensal e Pagamento

- Uma `MonthlyQuota` pode ter varios `PaymentRecord`
- Cada `PaymentRecord` pertence a uma unica `MonthlyQuota`

Isto e uma relacao **um para muitos (1:N)**.

#### Relacao 5: Tesoureiro e Validacao

- Um `MemberProfile` com papel de Tesoureiro pode validar varios pagamentos
- Um `PaymentRecord` pode ser validado por um unico `MemberProfile`

Isto e uma relacao **um para muitos (1:N)**.

### 6.4 Leitura simples do MER

Em linguagem muito simples, o fluxo dos dados e este:

1. O utilizador entra no sistema.
2. O sistema associa esse utilizador a um perfil de associado.
3. O associado regista uma ou mais viaturas.
4. Cada viatura recebe quotas mensais.
5. Cada quota pode receber um pagamento.
6. O tesoureiro pode validar esse pagamento.

### 6.5 Desenho textual do MER

```text
auth_user
   1
   |
   | 1:1
   |
portal_memberprofile
   1
   |
   | 1:N
   |
portal_vehicle
   1
   |
   | 1:N
   |
portal_monthlyquota
   1
   |
   | 1:N
   |
portal_paymentrecord

portal_memberprofile
   1
   |
   | 1:N (valida)
   |
portal_paymentrecord
```

### 6.6 Regras de consistencia adoptadas

Ao desenhar a base de dados, tambem tomamos algumas decisoes para evitar erros.

#### Regra 1: campos unicos

Alguns campos foram definidos como unicos, por exemplo:

- `member_number`
- `plate_number`

Porque:

- nao deve existir dois associados com o mesmo numero
- nao deve existir duas viaturas com a mesma matricula

#### Regra 2: proteccao de relacoes importantes

Em varios pontos usamos proteccao para evitar apagar dados importantes por engano.

Exemplo:

- nao queremos apagar uma viatura se ela ja tiver quotas
- nao queremos apagar um associado se ele tiver historico que precisa ser preservado

Isto ajuda a manter integridade historica.

#### Regra 3: historico temporal

Quase todas as tabelas do negocio têm:

- `created_at`
- `updated_at`

Isto permite saber:

- quando algo foi criado
- quando algo foi alterado

Esta decisao e importante para auditoria, demonstracao e controlo.

#### Regra 4: estados em vez de apagar o passado

Em vez de apagar ou sobrescrever tudo, usamos estados como:

- quota pendente
- quota paga
- quota em atraso
- pagamento pendente
- pagamento validado
- pagamento rejeitado

Isto foi escolhido porque um sistema financeiro precisa mostrar o caminho do processo,
e nao apenas o resultado final.

### 6.7 Porque esta estrutura e boa para o projecto

Esta estrutura foi escolhida porque:

- representa bem a realidade do problema
- separa claramente cada responsabilidade
- permite crescimento futuro
- facilita relatorios
- facilita a explicacao para a banca
- reduz risco de desorganizacao nos dados

Em resumo:

o desenho da base de dados foi pensado para ser simples de entender, mas suficientemente
forte para parecer um sistema real.

## 7. Etapa de registo de viaturas

Nesta etapa, o sistema passou a permitir que o associado autenticado registe as suas viaturas.

### 7.1 Porque o registo de viaturas e importante

Neste projecto, a quota nao sera gerada apenas para a pessoa.
Ela sera gerada para a viatura associada ao membro.

Isto significa que a viatura e uma parte central do negocio.

Sem o registo de viaturas, o sistema nao conseguiria:

- saber quantos carros pertencem ao associado
- gerar quotas por carro
- calcular debitos por viatura
- emitir historico correcto por matricula

### 7.2 O que foi implementado

Foi implementado:

- formulario para registar viatura
- listagem das viaturas do associado autenticado
- associacao automatica da viatura ao perfil logado
- desactivacao da viatura sem apagar o historico

### 7.3 Como o registo funciona

O fluxo e este:

1. o associado entra no sistema
2. abre a pagina de viaturas
3. preenche matricula, modelo, ano e cor
4. o sistema valida os dados
5. a viatura fica ligada ao perfil do associado autenticado
6. a viatura passa a aparecer na lista do proprio associado

### 7.4 Porque a viatura fica ligada ao utilizador autenticado

Esta foi uma decisao importante de seguranca e organizacao.

O sistema nao pede ao utilizador para escolher manualmente o dono da viatura no registo publico.
Em vez disso, o sistema usa automaticamente o perfil que esta autenticado.

Isto evita problemas como:

- um associado tentar registar uma viatura no nome de outra pessoa
- erro humano ao escolher o proprietario
- confusao entre perfis

### 7.5 Porque a matricula e unica

A matricula foi definida como unica no sistema.

Isto significa que nao podem existir duas viaturas com a mesma matricula.

Esta decisao foi tomada porque:

- uma viatura real deve ser identificada de forma unica
- evita duplicacao de registos
- melhora a confianca dos dados
- facilita relatorios e pesquisas

### 7.6 Porque usamos desactivacao em vez de apagar

Quando o associado deixa de usar uma viatura, ou quando a viatura sai do sistema, e melhor
desactiva-la em vez de apagar o registo.

Fazemos isso com o campo `is_active`.

Esta decisao foi tomada porque apagar dados pode causar problemas:

- perda de historico
- quebra de relatorios antigos
- confusao com quotas ja geradas
- dificuldade para auditoria

Por isso, o sistema prefere:

- manter o registo
- marcar a viatura como inactiva
- preservar o passado

### 7.7 Porque nao apagamos a viatura fisicamente

Num sistema de gestao, apagar definitivamente nem sempre e a melhor opcao.

Se uma viatura ja teve:

- quotas
- pagamentos
- recibos
- historico financeiro

entao o registo dela tem valor historico.

Mesmo que ela deixe de estar activa, o sistema pode continuar a precisar dela para:

- consultar movimentos antigos
- justificar cobrancas passadas
- mostrar o historico do associado

### 7.8 Relacao entre viatura e quota

O registo de viaturas foi pensado para preparar a proxima fase.

A ideia do sistema e:

- cada viatura activa pode receber quotas mensais
- essas quotas ficam ligadas a uma viatura especifica
- os pagamentos tambem ficam ligados a essa mesma linha de historico

Ou seja:

`Associado -> Viatura -> Quota Mensal -> Pagamento`

Esta cadeia e muito importante para a logica do sistema.

### 7.9 Decisoes tecnicas tomadas nesta etapa

#### Decisao 1: usar uma pagina protegida

O registo de viaturas so pode ser feito por utilizadores autenticados.

Motivo:

- a viatura precisa pertencer a alguem identificado no sistema

#### Decisao 2: usar `ModelForm`

Foi usado um formulario ligado ao modelo `Vehicle`.

Motivo:

- reduz codigo repetido
- usa as validacoes do Django
- deixa o codigo mais limpo

#### Decisao 3: guardar o dono no servidor

O dono da viatura nao vem do formulario publico.
Ele e definido no servidor a partir do utilizador autenticado.

Motivo:

- melhora a seguranca
- evita manipulacao de dados

#### Decisao 4: permitir desactivacao logica

Em vez de eliminar, a viatura passa para estado inactivo.

Motivo:

- preserva historico
- prepara melhor os relatorios futuros

### 7.10 Como esta etapa sera usada depois

O registo de viaturas servira de base para:

- geracao de quotas mensais
- consulta de debitos
- historico de pagamentos
- recibos por viatura
- relatorios de inadimplencia

### 7.11 O que a banca pode entender desta etapa

Em termos simples, esta fase mostra que:

- o associado entra no sistema
- regista os seus carros
- o sistema passa a saber exactamente sobre que carro vai cobrar
- a gestao deixa de ser genérica e passa a ser organizada por viatura

Isto aproxima o projecto de uma situacao real de controlo administrativo.

## 8. Dashboard do tesoureiro, geracao automatica de quotas e validacao de pagamentos

Esta etapa representa o coracao financeiro do sistema.

Aqui o projecto deixa de ser apenas um cadastro e passa a controlar:

- o valor da quota
- a criacao automatica das cobrancas
- a confirmacao de pagamento em maos
- a submissao de comprovantes de transferencia
- a validacao final feita pela tesouraria

### 8.1 Visao geral do fluxo

O fluxo completo desta parte funciona assim:

1. o administrador define o valor da quota no painel admin
2. o sistema passa a ter uma configuracao activa de quota
3. as quotas mensais sao geradas automaticamente para as viaturas activas
4. o associado consulta as suas quotas
5. se pagar por transferencia, envia o comprovante
6. se pagar em maos, o tesoureiro ou admin faz a confirmacao no sistema
7. o tesoureiro valida os comprovantes enviados
8. a quota passa ao estado `Paga`

### 8.2 Porque apenas o administrador define o valor da quota

O valor da quota e uma configuracao sensivel do sistema.

Se qualquer utilizador pudesse alterar esse valor, haveria risco de:

- cobrancas erradas
- perda de controlo financeiro
- confusao na tesouraria
- quebra da confianca no sistema

Por isso, a regra adoptada foi:

- apenas o administrador define ou altera o valor da quota

### 8.3 Como o administrador define o valor da quota

O administrador entra no painel admin do Django e cria ou activa uma configuracao em
`QuotaConfig`.

Essa configuracao guarda:

- valor da quota
- percentagem de multa
- data a partir da qual a configuracao passa a valer
- estado activo ou inactivo

### 8.4 O que acontece quando o admin estabelece o valor da quota

Quando o administrador cria ou activa uma configuracao de quota:

1. essa configuracao passa a ser a configuracao activa
2. o sistema desactiva as configuracoes activas anteriores
3. o sistema gera automaticamente quotas para as viaturas activas

Isto significa que a geracao ja nao depende de um clique manual do tesoureiro para criar as
quotas do periodo principal.

### 8.5 Porque a geracao de quotas foi automatizada

Esta decisao foi tomada porque, na pratica, a cobranca mensal deve nascer a partir da regra
administrativa definida pela associacao.

Se o valor foi definido, o sistema ja sabe:

- quanto cobrar
- a partir de quando cobrar
- para que viaturas cobrar

Automatizar esta parte traz vantagens:

- reduz trabalho manual
- evita esquecimento
- torna o sistema mais realista
- mostra mais maturidade tecnica

### 8.6 Como a geracao automatica funciona tecnicamente

Em linguagem simples, a logica faz isto:

1. procura a configuracao activa
2. identifica o mes de referencia dessa configuracao
3. procura todas as viaturas activas
4. cria uma quota mensal para cada viatura
5. impede duplicacao da mesma quota no mesmo mes

### 8.7 Como evitamos quotas duplicadas

Uma mesma viatura nao pode receber duas quotas para o mesmo mes.

Exemplo:

- se a viatura `LD-88-11-CC` ja tem quota para Junho de 2026
- o sistema nao cria outra quota igual para esse mesmo mes

Esta proteccao foi feita porque duplicacao de quota significaria:

- cobranca errada
- historico confuso
- possivel conflito financeiro

### 8.8 O que acontece quando uma nova viatura e criada

Tambem foi adicionada uma regra importante:

- se ja existir uma configuracao activa de quota
- e uma nova viatura activa for registada
- o sistema pode garantir a criacao da quota correspondente ao periodo activo

Isto ajuda a manter consistencia entre:

- viaturas activas
- configuracao activa
- quotas do sistema

### 8.9 Porque existe uma dashboard propria do tesoureiro

O tesoureiro recebeu uma dashboard propria porque o seu trabalho e diferente do trabalho do associado.

O associado:

- regista viaturas
- consulta quotas
- envia comprovantes

O tesoureiro:

- acompanha as quotas do sistema
- confirma pagamentos em maos
- valida comprovantes de transferencia

Isto respeita a divisao de papeis no negocio.

### 8.10 O que o tesoureiro ve na sua dashboard

Na dashboard do tesoureiro existem areas como:

- configuracao activa de quotas
- transferencias pendentes de validacao
- quotas que podem ser marcadas como pagas em maos
- visao resumida das quotas recentes

### 8.11 Formas de pagamento definidas no sistema

Nesta fase, o sistema passa a reconhecer duas formas principais de pagamento:

- pagamento em maos
- transferencia bancaria

Cada uma tem uma regra diferente.

### 8.12 Como funciona o pagamento em maos

Pagamento em maos significa que o associado entrega o valor fisicamente a um responsavel da
tesouraria.

Nesse caso:

- o associado nao marca sozinho a quota como paga
- o tesoureiro ou administrador e que confirma o pagamento no sistema

### 8.13 Porque o associado nao pode marcar pagamento em maos

Esta restricao existe por seguranca e controlo.

Se o associado pudesse marcar sozinho como pago:

- o sistema poderia registar pagamentos falsos
- a tesouraria perderia controlo
- o historico financeiro deixaria de ser confiavel

Por isso, a regra escolhida foi:

- pagamento em maos so pode ser confirmado por tesoureiro ou administrador

### 8.14 O que acontece quando o tesoureiro marca pagamento em maos

Quando o tesoureiro ou administrador clica para marcar uma quota como paga em maos:

1. o sistema cria um `PaymentRecord`
2. o metodo fica como `Pagamento em maos`
3. o estado do pagamento fica como `Validado`
4. a quota muda imediatamente para `Paga`
5. o sistema guarda quem confirmou
6. o sistema guarda a data da confirmacao

### 8.15 Como funciona a transferencia bancaria

No caso de transferencia bancaria:

- o associado faz o pagamento fora do sistema
- depois entra no sistema
- escolhe a quota
- faz upload do comprovante

O sistema nao confirma automaticamente esse pagamento.

Ele apenas regista que o associado submeteu um comprovante.

### 8.16 O que e o upload de comprovante

Upload de comprovante significa enviar um ficheiro para o sistema.

Esse ficheiro pode representar, por exemplo:

- uma imagem
- um PDF
- um documento digital com prova da transferencia

No sistema, esse ficheiro fica guardado associado ao registo do pagamento.

### 8.17 O que acontece quando o associado envia o comprovante

Quando o associado envia o comprovante:

1. o sistema cria um `PaymentRecord`
2. o metodo fica como `Transferencia bancaria`
3. o estado do pagamento fica como `Comprovante submetido`
4. o sistema guarda o ficheiro enviado
5. a quota passa para `Aguarda validacao`

### 8.18 Porque a quota nao vai directamente para `Paga` na transferencia

Isto foi decidido porque o simples envio de um comprovante ainda nao e confirmacao final.

Ainda pode haver situacoes como:

- comprovante errado
- valor incorrecto
- comprovante ilegivel
- tentativa de fraude

Por isso, o comprovante precisa de ser verificado por um responsavel.

### 8.19 Como funciona a validacao pelo tesoureiro

Na dashboard do tesoureiro aparece a lista de transferencias pendentes.

Quando ele valida:

1. o pagamento passa para `Validado`
2. o sistema guarda quem validou
3. o sistema guarda a data da validacao
4. a quota correspondente passa para `Paga`

### 8.20 Porque o tesoureiro valida o comprovante

O tesoureiro valida porque ele representa o controlo financeiro da associacao.

Isto ajuda a garantir:

- verificacao humana
- confianca no historico
- controlo sobre a tesouraria
- registos coerentes

### 8.21 Estados usados nesta fase

#### Estados da quota

- `Pendente`
- `Aguarda validacao`
- `Paga`
- `Em atraso`

#### Estados do pagamento

- `Pendente`
- `Comprovante submetido`
- `Validado`
- `Rejeitado`

### 8.22 Porque usamos estados

Os estados existem para que o sistema saiba exactamente em que fase esta cada cobranca.

Sem eles, seria dificil responder perguntas como:

- esta quota ja foi criada?
- o associado ja enviou comprovante?
- a tesouraria ja confirmou?
- o pagamento em maos ja foi registado?

### 8.23 Decisoes tecnicas tomadas nesta etapa

#### Decisao 1: o admin define o valor da quota

Motivo:

- configuracao financeira deve ficar com a administracao

#### Decisao 2: geracao automatica de quotas

Motivo:

- reduz trabalho manual
- alinha o sistema com a regra da associacao

#### Decisao 3: pagamento em maos so por tesouraria

Motivo:

- protege a confianca do sistema

#### Decisao 4: transferencia com comprovante

Motivo:

- cria um fluxo convincente sem integracao bancaria real

#### Decisao 5: validacao no servidor

Motivo:

- evita alteracoes falsas apenas no browser
- garante consistencia real dos dados

### 8.24 O que a banca pode entender desta etapa

Em termos simples, esta fase mostra que o sistema ja faz controlo administrativo e financeiro:

- o admin define a regra de cobranca
- o sistema gera as quotas
- o associado envia prova de pagamento
- a tesouraria confirma

Isto aproxima muito o projecto de um sistema real de gestao de quotas.

## 9. Landing page inicial

A landing page foi criada para ser a porta de entrada do sistema.
Ela mostra:

- o nome do projecto
- o objectivo do sistema
- os perfis de utilizador
- a ideia de simulacao de pagamentos
- o estado actual da implementacao

Esta pagina ajuda muito na apresentacao porque, antes mesmo do login, a banca consegue
entender o que esta a ser demonstrado.

## 10. Etapa de autenticacao implementada

Nesta etapa, passamos a ter um fluxo real de entrada no sistema.

### 8.1 O que foi implementado

Foram criadas as seguintes partes:

- pagina de login
- pagina de registo
- criacao de utilizador no sistema
- criacao automatica do `MemberProfile`
- dashboard inicial protegido
- logout
- mensagens de sucesso e erro

### 8.2 Como o registo funciona

Quando um novo utilizador preenche o formulario de registo:

1. o sistema valida os dados
2. verifica se o username ja existe
3. verifica se o email ja existe
4. verifica se o numero de associado ja existe
5. valida a palavra-passe
6. cria o utilizador em `auth_user`
7. cria o perfil correspondente em `portal_memberprofile`
8. inicia a sessao automaticamente

Observacao importante:

No registo publico do associado motorista, o campo `staff` nao aparece.

Motivo:

- o foco do registo publico e o associado comum
- o associado nao precisa definir sozinho um enquadramento interno de staff
- esse tipo de classificacao pode ser tratado depois pela administracao, quando for necessario

### 8.3 Como o login funciona

Quando o utilizador preenche o login:

1. o sistema recebe username e palavra-passe
2. o Django tenta autenticar
3. se os dados estiverem certos, a sessao e criada
4. o utilizador e redireccionado para o dashboard

### 8.4 Como a proteccao de paginas funciona

Algumas paginas nao devem ser abertas por qualquer pessoa.

Por isso, usamos proteccao de login no dashboard.

Significa que:

- se o utilizador estiver autenticado, entra normalmente
- se nao estiver autenticado, o sistema bloqueia o acesso directo

### 8.5 Porque comecamos com este modelo

Comecamos com autenticacao por username e palavra-passe porque:

- e a forma mais clara de demonstrar login
- encaixa bem no Django
- e suficiente para a fase actual
- sera facil evoluir depois para controlo por perfil

### 8.6 O que ainda vamos ligar a esta etapa

Nos proximos passos, esta autenticacao sera ligada a:

- registo de viaturas do associado autenticado
- consulta de quotas do associado autenticado
- simulacao de pagamento do associado autenticado
- validacao feita pelo tesoureiro autenticado
- administracao feita pelo utilizador com perfil administrador

### 8.7 Administrador padrao e politica de seguranca

O sistema tera um administrador padrao criado com o proprio Django.

Isto sera feito pela **CLI**, que significa **Interface de Linha de Comando**.

Em vez de criar administradores por uma pagina publica do sistema, o administrador e criado
directamente por quem tem acesso tecnico ao projecto.

### 8.7.1 Porque o registo publico nao pode criar administradores

Por motivos de seguranca, nao podemos permitir que qualquer pessoa crie uma conta de
administrador pela interface publica.

Se isso fosse permitido, haveria riscos graves:

- qualquer pessoa poderia ganhar controlo total do sistema
- dados sensiveis poderiam ser alterados ou apagados
- pagamentos poderiam ser manipulados
- configuracoes do sistema poderiam ser comprometidas

Por isso, a regra adoptada foi:

- o associado comum pode fazer registo publico
- o administrador nao pode ser criado publicamente
- o administrador so e criado por linha de comando

### 8.7.2 Porque usamos o painel admin do Django

O Django ja traz um painel administrativo muito forte e confiavel.

Esse painel permite:

- gerir utilizadores
- gerir perfis
- gerir viaturas
- gerir quotas
- gerir pagamentos

Em vez de construir ja uma area administrativa completa do zero, aproveitamos o painel admin
do Django porque ele:

- acelera o desenvolvimento
- ja e seguro
- ja trabalha bem com autenticacao
- facilita a demonstracao do sistema

### 8.7.3 Como se cria um administrador no Django

Existem duas formas comuns:

#### Forma interactiva

```bash
./.venv/bin/python manage.py createsuperuser
```

Depois, o terminal vai pedir:

- nome de utilizador
- email
- palavra-passe

#### Forma automatizada

Tambem e possivel criar um administrador por comando de script ou por codigo executado na CLI.

Isto e util quando queremos deixar um administrador inicial pronto para demonstracao.

### 8.7.4 O que e um superuser

No Django, o administrador com permissao total chama-se **superuser**.

Esse utilizador pode:

- entrar no painel admin
- criar e editar utilizadores
- gerir os dados do sistema
- atribuir papeis
- controlar o funcionamento administrativo

### 8.7.5 Quem cria o tesoureiro

O tesoureiro nao sera criado pelo publico.

A regra definida para o projecto e esta:

- o administrador entra no painel admin
- o administrador cria ou edita um utilizador
- o administrador define o perfil desse utilizador como `Tesoureiro`

Isto faz sentido porque o tesoureiro e um papel de confianca dentro do sistema.

### 8.7.6 Porque o administrador cria o tesoureiro

O tesoureiro tem poderes importantes, como:

- validar pagamentos
- confirmar processos financeiros
- participar no controlo das quotas

Por isso, nao e seguro deixar que qualquer pessoa se auto-declare tesoureiro.

A decisao tomada foi:

- o papel de tesoureiro e atribuido apenas pela administracao
- o administrador e quem promove esse utilizador no sistema

## 11. Historico de alteracoes

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

### Alteracao 4

Data: 22 de Maio de 2026

Foi feito:

- preparacao de leitura automatica de variaveis de ambiente a partir de `.env`
- definicao do apontamento local para MySQL
- proteccao do ficheiro `.env` no `.gitignore`

Decisao:

As credenciais locais da base de dados nao devem ficar escritas directamente no codigo.
Por isso, o projecto passa a ler as configuracoes do MySQL a partir de um ficheiro `.env`
na raiz do workspace.

### Alteracao 5

Data: 22 de Maio de 2026

Foi feito:

- criacao da base de dados `sgpqaa` no MySQL local
- configuracao real do projecto para usar MySQL com `PyMySQL`
- detalhamento das tabelas, entidades e relacionamentos no documento

Decisao:

Foi usado `PyMySQL` no lugar de `mysqlclient` porque o ambiente local nao tinha os headers
necessarios para compilar o driver nativo com Python 3.14. Para este projecto, `PyMySQL`
resolve bem e simplifica o desenvolvimento.

### Alteracao 6

Data: 22 de Maio de 2026

Foi feito:

- reforco da documentacao sobre o ficheiro `.env`
- explicacao detalhada do que e um MER
- explicacao dos relacionamentos `1:1`, `1:N` e `N:1`
- aprofundamento do desenho da base de dados e das decisoes tomadas

Decisao:

Esta documentacao passou a ser mais explicita porque a avaliacao sera feita por pessoas
leigas. Por isso, a prioridade aqui nao e resumir, mas explicar com clareza pedagogica.

### Alteracao 7

Data: 22 de Maio de 2026

Foi feito:

- implementacao do fluxo inicial de autenticacao
- criacao das paginas de login, registo, dashboard e logout
- criacao automatica do perfil do associado apos registo
- explicacao detalhada no documento sobre autenticacao, sessao e JWT

Decisao:

Foi adoptada autenticacao classica do Django com sessao no servidor. JWT ficou apenas como
conceito documentado, mas nao como tecnologia usada nesta fase, por ser desnecessario para
o tipo de aplicacao que estamos a construir agora.

### Alteracao 8

Data: 22 de Maio de 2026

Foi feito:

- implementacao do registo de viaturas para o associado autenticado
- criacao da pagina de gestao de viaturas
- criacao de listagem das viaturas do proprio associado
- implementacao de desactivacao logica de viaturas
- reforco completo da documentacao desta etapa

Decisao:

As viaturas passaram a ser tratadas como base da geracao de quotas. A remocao foi feita por
desactivacao logica, e nao por apagamento fisico, para preservar historico e manter o
sistema preparado para as proximas fases.

### Alteracao 9

Data: 22 de Maio de 2026

Foi feito:

- criacao da dashboard do tesoureiro
- implementacao da geracao automatica de quotas a partir da configuracao activa definida pelo administrador
- criacao da pagina de quotas do associado
- implementacao do pagamento em maos marcado pela tesouraria
- implementacao da transferencia bancaria com upload de comprovante
- implementacao da validacao do pagamento pelo tesoureiro
- explicacao detalhada de toda esta logica no documento

Decisao:

O sistema passou a tratar a quota como elemento financeiro central do processo. O
administrador ficou responsavel por definir o valor da quota, o sistema ficou responsavel
pela geracao automatica das cobrancas, e a tesouraria ficou responsavel por confirmar os
pagamentos em maos e validar os comprovantes de transferencia enviados pelos associados.

## 12. Proximos passos previstos

Nas proximas etapas, vamos construir:

- recibo
- historico de pagamentos
- debitos e multas por atraso
- relatorios
