# FLUXO — como o dado de cada conta fica separado do das outras

**Data:** 26/08/2026
**Para que serve:** responder, com as linhas da tabela à vista, o que acontece
quando duas pessoas diferentes cadastram o mesmo remédio. É a base do desenho
das tabelas e das consultas.

**O que este documento é:** o passo a passo do que o sistema faz, e a
explicação de onde vem a separação entre as contas.

**O que este documento NÃO é:** não é modelagem final, não tem lista de
endpoints, não tem código. E não decide nada novo — só torna visível o que já
estava decidido e nunca tinha sido escrito de forma que se pudesse enxergar.

**Origem:** conversa de 26/08/2026, em que Thaís levantou a dúvida — *"um
segundo usuário registra e digita também aquele medicamento, e aí o que
acontece com esse segundo usuário?"* — e a resposta mostrou que faltava esta
página no acervo.

---

## O MAL-ENTENDIDO QUE ISTO DESFAZ

A dúvida era razoável e vinha de uma palavra: **"tabela de medicamentos"**
soa como **catálogo** — uma lista pronta, compartilhada, de onde as pessoas
escolheriam. Se fosse isso, duas pessoas não poderiam ter a mesma furosemida.

**Não é catálogo. É depósito.** Uma tabela onde cada linha guarda, junto, o
carimbo de quem é. Ninguém escolhe de lista nenhuma, e ninguém vê o que outro
digitou.

É a mesma confusão que a §13.1 do estado corrente já teve de desfazer uma vez,
quando `FASE2_3_DECISAO_PROJETO_PORTFOLIO.md` 51 chamou o modelo de *"catálogo
digitado pela usuária"*.

---

## O PASSO A PASSO

### 1. Maria cria conta

A tabela de remédios está vazia. Não existe "tabela da Maria" sendo criada
neste momento — tabela é estrutura, criada por migração antes de o sistema ir
ao ar, não a cada cadastro.

### 2. Maria digita o remédio dela

`FUROSEMIDA`, `5`, `mg`, `comprimido`.

| id | dono | nome | valor | unidade | forma |
|---|---|---|---|---|---|
| 1 | **Maria** | FUROSEMIDA | 5 | mg | comprimido |

### 3. João cria conta e digita exatamente a mesma coisa

| id | dono | nome | valor | unidade | forma |
|---|---|---|---|---|---|
| 1 | **Maria** | FUROSEMIDA | 5 | mg | comprimido |
| 2 | **João** | FUROSEMIDA | 5 | mg | comprimido |

**Aceito, sem erro.** Duas linhas com o mesmo nome, a mesma miligramagem e a
mesma forma convivendo na tabela.

**Por que a trava de duplicidade não dispara aqui, e este é o ponto central
do documento:** a trava não é sobre nome + valor + unidade + forma. É sobre
**conta** + nome + valor + unidade + forma (§3.1 do estado corrente). A conta
é a primeira coluna da combinação. A linha 1 tem Maria; a linha 2 tem João.
São combinações diferentes, e o banco só recusa quando **as cinco**
coincidem.

### 4. Maria tenta cadastrar a mesma caixa outra vez

**Recusado como duplicata.** Esta é a única situação em que a trava dispara: a
mesma conta cadastrando a mesma caixa duas vezes. É exatamente o problema para
o qual ela foi criada.

### 5. Cada uma pede a própria lista

Maria recebe só a linha 1. João recebe só a linha 2. Nenhum dos dois sabe que
o outro existe, nem que digitou o mesmo remédio.

A consulta é a mesma para os dois; o que muda é o valor do filtro — a conta de
quem está pedindo.

### 6. João tenta pedir o remédio de identificador 1, que é da Maria

**404** — decidido em 26/08/2026, §17.5 do estado corrente. A linha 1 não está
no conjunto do João, e a resposta não revela sequer que ela existe. (Este passo
dizia **403** até 26/08/2026, herdado de uma tabela anterior ao filtro em ponto
único da §17.2.)

É o teste que a §9 do estado corrente coloca como o item que faz um avaliador
reconhecer trabalho competente, e o roteiro do README (§14.2) leva quem avalia
até ele.

---

## O ERRO DE DIGITAÇÃO, NESTE DESENHO

Maria digita `FUROSEMIDA`. João digita `FUSOSEMIDA`, errado.

Entram as duas, cada uma na conta de quem digitou, e **uma nunca encosta na
outra**. O erro só tem consequência dentro da própria conta: a pessoa vê o
nome errado na própria lista.

Nenhum usuário escolhe, vê ou reaproveita o que outro digitou. **Nada é
compartilhado entre contas por acidente** — só pelo convite com aceite, que é
explícito e reversível (§6.1 e §6.4).

Isso é o item 12 da lista do que o projeto não faz: o sistema aceita o nome
errado e não corrige.

---

## DE ONDE VEM A SEPARAÇÃO ENTRE AS CONTAS

Não vem de as linhas morarem em lugares fisicamente diferentes. Vem de três
peças, e as três precisam existir:

| Peça | O que faz | Onde está decidida |
|---|---|---|
| A **coluna de dono** em cada tabela | carimba cada linha com a conta a que pertence | `CORRECAO_MODELAGEM...` 219 e 221 — `Medicamento` e `Doenca` têm *dono → conta* |
| O **filtro por dono em toda consulta** | faz cada conta enxergar só as próprias linhas | `FASE1...` D6, e a regra de permissão do estado corrente |
| A **restrição no banco** | garante o que o código poderia esquecer | §3.1 e §3.3 do estado corrente |

**A terceira existe porque as duas primeiras são código, e código se esquece.**
A restrição no banco vale mesmo que uma consulta seja escrita errada.

---

## POR QUE UMA TABELA, E NÃO UMA POR PESSOA

Registro das razões, porque a pergunta é boa e vai voltar.

**Quatro razões específicas deste projeto:**

1. **A trava de duplicidade decidida não existiria.** A combinação inclui a
   conta; dentro de uma tabela que fosse só da Maria, toda linha já seria
   dela, e a palavra "conta" na combinação não teria função.
2. **O compartilhamento não funcionaria.** Quando João aceita o convite da
   Maria, o sistema busca os remédios dela enquanto ele está logado. Com uma
   tabela por pessoa, seria preciso descobrir o nome da tabela da Maria em
   tempo de execução.
3. **O argumento de entrevista deixaria de existir.** O teste do 403 só faz
   sentido porque os dados convivem e o sistema os separa. Em tabelas
   fisicamente separadas não há isolamento a demonstrar.
4. **O painel administrativo e as migrações.** O Django não gera migração para
   tabelas criadas em tempo de execução, e cada mudança de campo viraria
   tantas alterações quantas fossem as contas.

**Sobre o desempenho, e é ao contrário do que a intuição sugere:** uma tabela
com índice na coluna de dono é **mais rápida** do que muitas tabelas. É o
desenho que todo sistema com vários usuários usa.

**Sobre a repetição do nome entre contas:** é intencional. Segue o mesmo
raciocínio já registrado de `FUROSEMIDA 5 mg` e `FUROSEMIDA 20 mg` serem duas
linhas da mesma tabela (`HANDOFF...` 126). A tabela não guarda "o remédio
furosemida"; guarda **a caixa que está na gaveta de alguém**. Duas pessoas
terem a mesma caixa em casa não é duplicata.

---

## O PERÍODO DE USO — DECIDIDO EM 26/08/2026

O período de uso — a linha com dose, quantas vezes ao dia, início e fim —
**não tem coluna de dono**. Ele aponta para o remédio, e o remédio é que tem
o carimbo.

Ou seja: a informação de quem toma **existe**, mas está a um passo de
distância. Toda consulta ao período de uso precisa atravessar até o remédio
para saber de quem é.

**A decisão:** o desenho continua assim, e o filtro por dono passa a morar num
ponto único do código, por onde toda consulta passa. Cada endpoint declara
apenas o caminho até o dono — direto no remédio e na doença, atravessando o
remédio no período de uso. Endpoint novo que não declare esse caminho **não
sobe**: falha na primeira chamada, em vez de funcionar e vazar em silêncio.

A alternativa examinada — dar ao período de uso uma coluna própria de dono —
foi descartada por Thaís, por guardar a mesma informação em dois lugares que
poderiam discordar.

Detalhamento, motivos e o que isso obriga na definição de pronto: seção 17 do
estado corrente. Isso encerra o achado 7 da auditoria — o último dos doze.
