# ETAPA 2 — levantamento: o que existe nos arquivos e não está no estado corrente

**Data:** 24/08/2026

**O que este documento é:** a lista das decisões, restrições e pendências que
existem nos arquivos do projeto e **não aparecem** em
`docs/migration-sources/ESTADO_CORRENTE_23_08_2026.md`. Cada linha traz o arquivo, a linha, e a
origem: fala direta de Thaís com citação, decisão registrada sem citação, ou
proposta de Claude nunca confirmada.

**O que este documento NÃO é:** não incorporou nada ao estado corrente, não
decidiu nada, não corrigiu nenhum arquivo. **Nenhum item abaixo está
aprovado.** A lista existe para ser percorrida por blocos, com Thaís
confirmando item a item. Só depois disso alguma coisa entra no documento
único.

---

## PROCEDÊNCIA

**Lidos por inteiro nesta etapa, na ordem mandada pela Fase 5:**

1. `FASE1_ESCOPO_PROJETO_PORTFOLIO.md`
2. `FASE2_3_DECISAO_PROJETO_PORTFOLIO.md`
3. `HANDOFF_FASE4_MODELAGEM_REGISTRO_MEDICACAO.md`
4. `MODELAGEM_REGISTRO_MEDICACAO.md`
5. `CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md`
6. `PROMPT_VISIBILIDADE_E_INTEGRACAO_V2.md`
7. `REGRAS_COMPORTAMENTO_PROJETO.md`
8. `O_QUE_O_PROJETO_NAO_FAZ.md` (já lido na Etapa 1)

**Fora do acervo, por decisão de Thaís em 26/08/2026:** o arquivo do projeto
futuro do gerador de escala. Ela o removeu da pasta — *"não tem nada a ver com
esse projeto"* — e mandou tirar toda menção a ele. Nada dele entra neste
levantamento.

**Não lidos, por proibição da Fase 5:** todos os `EXTRATO_*.md`.

**Não lidos, por não estarem na lista da Etapa 2:** `00_CRONOLOGIA.md`,
`00_INDICE_POR_ASSUNTO.md`, `PROMPT_FASE2_CANDIDATOS_PROJETO.md`,
`PROMPT_FASE4_TESTE_ESTRESSE.md`.

---

## COMO LER A ORIGEM

| Marca | Significado | O que fazer |
|---|---|---|
| **FALA** | existe citação literal de Thaís sustentando | confirmar que continua valendo, e incorporar |
| **REGISTRO** | decisão escrita como fechada, sem citação literal ao lado | perguntar antes de incorporar |
| **CLAUDE** | proposta de Claude, nunca confirmada por Thaís | **não incorporar** sem decisão dela |
| **ABERTO** | pergunta que nenhum documento respondeu | vira pendência, não decisão |

---

## RESUMO DOS BLOCOS

| Bloco | Assunto | Itens | O maior risco se ficar de fora |
|---|---|---|---|
| A | Restrições de base do projeto | 9 | o documento único não diz o que o projeto pode e não pode usar |
| B | Autenticação e prova de isolamento | 4 | a decisão central do projeto não está escrita em lugar nenhum do estado corrente |
| C | Método de trabalho e ferramental | 3 | a ordem de construção do projeto não está registrada |
| D | Modelagem do remédio e do uso | 9 | a modelagem não fecha; falta campo decidido e sobra pergunta aberta |
| E | Telegram — o que ainda falta | 2 | a integração decidida não tem como funcionar sem isto |
| F | Escopo excluído que sumiu das listas | 3 | exclusões decididas por Thaís deixaram de constar |
| G | Vocabulário | 1 | nunca foi confirmado |
| H | Listas pequenas ainda abertas | 6 | não bloqueiam desenho, bloqueiam código |

**Total: 37 itens.** Nenhum incorporado.

---

# BLOCO A — RESTRIÇÕES DE BASE DO PROJETO

O estado corrente usa várias destas restrições sem nunca as ter escrito. Ele
cita "a decisão de hospedagem gratuita da Fase 1" (§7.4) e "a restrição de
exatamente uma integração externa" (§7.1) como se o leitor já as conhecesse —
mas elas não estão no documento. Quem ler só o estado corrente não sabe de
onde vêm.

### A1 — Thaís escreve o próprio código; a IA não entrega código pronto

`FASE1...` 31, restrição R3: *"Thaís escreve o próprio código e roda os
próprios comandos. IA explica lógica e raciocínio; não entrega código pronto.
Isso entra no dimensionamento de esforço."*

**Origem: REGISTRO.** É restrição fixa da Fase 1, sem citação literal ao lado,
mas `FASE1...` 120 registra que a capacidade de defender o projeto em
entrevista **depende** dela se manter durante toda a execução.

**Por que importa agora:** é a última fase antes do código. Esta é a regra que
governa como as próximas conversas funcionam, e ela não está no documento que
vai ser lido.

### A2 — Hospedagem: gratuito é o alvo, com válvula de escape de 5 a 10 euros por mês

`FASE1...` 42, decisão D1. A verba existe *"a ser acionada só se o problema de
hibernação se mostrar sério na hora de publicar"*.

**Origem: REGISTRO.** Sem citação literal.

**O estado corrente usa a metade e omite a outra:** §7.4 invoca "a decisão de
hospedagem gratuita" para proibir processo permanente, mas não registra que
existe verba autorizada. Isso pode mudar a resposta do risco da §7.5 — se a
hibernação atrapalhar o Telegram, existe dinheiro autorizado para resolver.

### A3 — Tarefa agendada é permitida; worker permanente é que é proibido

`FASE1...` 124 a 136, seção inteira chamada *"CORREÇÃO registrada — worker
permanente ≠ cron job"*, com tabela comparando os dois e a conclusão:
*"'receber algo automaticamente todo dia' é cron, e está liberado."*

**Origem: REGISTRO**, escrito como correção de um erro de Claude que
*"quase eliminou metade das ideias de Thaís injustamente"*.

**Contradição a resolver, e é real:** `O_QUE_O_PROJETO_NAO_FAZ.md` item 17 diz
*"O sistema não roda nada continuamente fora do ciclo de requisição e
resposta"*, e o motivo dado é a proibição do worker permanente. A frase, como
está, também exclui cron — que a Fase 1 declara **permitido**. Não sei se o
projeto vai querer cron; sei que a lista de exclusões hoje fecha uma porta que
a Fase 1 deixou aberta.

### A4 — Firebase, Supabase e a categoria inteira de backend-como-serviço estão descartados

`FASE1...` 51 a 54, decisão D2. Motivo: substituem exatamente o que o projeto
precisa provar. Cloud Run descartado por custo de horas, não por incapacidade.

**Origem: REGISTRO.**

### A5 — Exatamente uma integração externa, e o canal de entrega conta como integração

`FASE1...` 67, decisão D4, com **FALA** de Thaís na linha 68: *"não mais que
uma também porque, por causa do tempo limitado do projeto"*.

E a armadilha de contagem, `FASE1...` 72: *"o canal de entrega conta como
integração externa"* — um projeto que gera conteúdo com serviço externo e
entrega por Telegram tem **duas**, não uma.

**Origem: FALA** (a regra) **+ REGISTRO** (a armadilha de contagem).

**O estado corrente usa a regra sem nunca a enunciar.** §7.1 diz que o
Telegram *"satisfaz a restrição de exatamente uma integração externa"* sem
dizer qual é a restrição nem de onde vem. A armadilha de contagem não aparece
em lugar nenhum — e é ela que sustenta a vigilância da §8 sobre o e-mail.

### A6 — Domínio de utilidade real, com escopo congelado no dia 1

`FASE1...` 78, decisão D5, com **FALA** na linha 79: *"apesar de ser para
resolver um problema real, ele é para o meu portfólio. Então eu não posso,
vamos dizer, escalar muito o projeto. Eu tenho que tentar me limitar ao tempo
proposto."*

Motivo registrado: utilidade real é a maior fonte de inchaço de escopo que
existe.

### A7 — Dados e aprendizado de máquina estão fora do domínio

`FASE1...` 97, decisão D7, com **FALA** na linha 98: *"Esse projeto é backend,
não é dados. Isso, em questão de dados está excluído."*

Permitido: consumir serviço externo a partir do backend e servir o resultado
pela própria API. Excluído: treinar modelo, afinar modelo, avaliar modelos,
pipeline de dados.

**Não está no estado corrente nem na lista do que o projeto não faz.**

### A8 — Reaproveitar o que já sabe, sempre acrescentando aprendizado novo

`FASE1...` 112, decisão D9, com **FALA** na linha 113: *"Tudo que eu puder
aproveitar do meu conhecimento de construir o SkillBridge, se for possível, a
gente tem que tentar aproveitar, mas sempre colocando mais conhecimento e mais
aprendizado."*

**Onde isso ainda opera:** §12.3 do estado corrente compara a arquitetura de
contas com a do SkillBridge, e a §8 reaproveita o registro consciente de
proteção de dados. O critério que autoriza essas comparações não está escrito.

### A9 — A plataforma de hospedagem nunca foi escolhida

`FASE1...` 46: *"Plataforma NÃO foi escolhida. É assunto da conversa de
deploy."* Com três dados de 21/08/2026 marcados como **a reverificar**:
hibernação do Render em 15 minutos com retorno de 30 a 60 segundos; expiração
do banco gratuito do Render **não resolvida**, com fontes se contradizendo
entre 30 dias, 90 dias e nunca; e o Neon com plano gratuito permanente de
0,5 GB.

`FASE2_3...` 136 mantém isso em aberto.

**Origem: ABERTO.**

**Por que importa mais do que parece:** a §7.5 do estado corrente usa o dado da
hibernação para levantar o risco do Telegram, mas o dado é de uma plataforma
que **ainda não foi escolhida**. E a dúvida sobre o banco gratuito expirar em
30 dias é risco direto para um projeto que precisa ficar no ar num link de
currículo.

---

# BLOCO B — AUTENTICAÇÃO E PROVA DE ISOLAMENTO

Este é o bloco mais grave do levantamento. **A decisão central do projeto — o
que ele existe para provar — não está no estado corrente.**

- As escolhas dadas:

Nível 1 — usuário único, você. O sistema serve só a você. Ninguém mais cadastra. Normalmente resolvido com uma chave secreta simples ou com o próprio admin do Django. Custo: baixo.

Nível 2 — múltiplos usuários com dados isolados. Qualquer pessoa se cadastra, faz login, e vê apenas o que é dela. Custo: significativamente mais alto, e vale entender por quê.

Não é o login em si — Django já traz sistema de usuários pronto e você já usa Argon2 no SkillBridge. O custo está em três coisas que vêm junto:

Autenticação por token na API. Uma API REST não usa sessão de navegador. Ela usa token — geralmente JWT — que o cliente manda em cada requisição. É configuração nova e conceito novo.
Isolamento em cada consulta. Toda consulta ao banco precisa filtrar pelo dono. Esquecer isso numa única view vaza dados de um usuário para outro. É a falha de segurança mais comum em API júnior.
Testes dobram. Cada endpoint passa a precisar de teste "com o dono" e teste "com outro usuário, que tem que receber 403".

O lado a favor do Nível 2: o seu Fase_2_entrevista.md lista "REST stateless" como conceito que você ainda não conhece, e isso é justamente o que autenticação por token te ensina na prática. É um item real de mercado.

- o que foi escolhido: Nivel 2, veja abaixo.

### B1 — Autenticação de múltiplos usuários com dados isolados


`FASE1...` 83, decisão D6, com **FALA** na linha 84. Ela escolheu contra a
recomendação de Claude, que era o nível mais simples. Motivo dela: *"isso
mostra que você sabe fazer algo que é uma qualidade a mais você saber trabalhar com essa autenticação da maneira correta."*.

`FASE2_3...` 28 registra por que este projeto foi escolhido e não outro:
*"a autenticação nível 2 é a regra de negócio central, não um item de
checklist. Nos outros candidatos, 'cada um vê só o seu' era um filtro numa
consulta. Aqui é o motivo do sistema existir."*

**Origem: FALA.**

**O que o estado corrente tem:** §9 lista "usuário B recebe 403 no dado do
usuário A" como critério de avaliação, e §14.2 manda o README ensinar a chegar
nesse 403. Ou seja: ele registra **o teste** e nunca **a decisão que o teste
verifica**.

### B2 — Autenticação por token, com a biblioteca nomeada e uma ressalva que envelheceu

`FASE1...` 91 a 95: pesquisa feita a pedido de Thaís em 21/08/2026.
`djangorestframework-simplejwt` na versão 5.5.1, sob o coletivo Jazzband,
manutenção sustentável.

E a ressalva, `FASE1...` 94: *"a página lida não menciona Django 6.0. Não foi
possível determinar se a página está desatualizada ou se o suporte ainda não
saiu. **Conferir a compatibilidade da versão vigente no momento de
instalar.**"*

`FASE1...` 95 registra que a escolha não é consenso técnico, e que vence por
motivo não-técnico: *"é o termo que aparece nos anúncios"*.

**Origem: REGISTRO**, com pesquisa datada.

**Por que virou mais urgente, e não menos:** §3.3 do estado corrente registra o
ambiente de Thaís como **Django 6.1**. A ressalva foi escrita quando a dúvida
era sobre o Django 6.0. Hoje o ambiente está uma versão à frente do que a
biblioteca declarava suportar quando foi pesquisada. Isso não é problema
resolvido; é problema que ficou maior e continua sem verificação.

### B3 — A tabela de testes obrigatórios de permissão

`MODELAGEM...` 269 a 277, **DECIDIDO na Fase 1 e embutido ali**. Em **cada**
endpoint, no mínimo:

| Quem | Leitura | Escrita |
|---|---|---|
| dono do dado | 200 | 200 |
| convidado com compartilhamento **aceito** | 200 | **403** |
| convidado com compartilhamento **pendente** | **403** | **403** |
| conta sem relação nenhuma | **403** | **403** |
| sem token | **401** | **401** |

`CORRECAO...` 232 mantém essa tabela expressamente viva: *"A tabela de testes
obrigatórios da §7 de `MODELAGEM_REGISTRO_MEDICACAO.md` continua valendo
inteira, trocando 'dono do titular' por 'dona do dado'."*

**Origem: REGISTRO**, com validade reafirmada em documento posterior.

**O estado corrente tem uma linha dessa tabela — a do 403 — e não tem a
tabela.** E a tabela ficou **incompleta** depois da decisão §6.3 (convite com
escopo): falta a linha do convidado que tem acesso a remédios e não a doenças.
Hoje ela não existe em lugar nenhum.

### B4 — Nome e e-mail nunca aparecem em registro de log

`CORRECAO...` 114, **DECIDIDO**, com **FALA** na linha 116: *"a gente tem que
tomar cuidado nos logs, a gente não pode exibir nada disso nos logger()"*.

E o alerta técnico da linha 120, que é o que dá substância ao item: o log
óbvio é fácil de evitar; o difícil é o **log de erro**, que pode carregar o
objeto inteiro com nome e e-mail dentro sem ninguém ter escrito isso. *"É a
categoria de vazamento que só aparece em produção."*

**Origem: FALA.**

**Não está no estado corrente.** É decisão dela, é sobre dado sensível, e é
item de definição de pronto.

---

# BLOCO C — MÉTODO DE TRABALHO E FERRAMENTAL

`FASE2_3...` 82 diz o que este bloco é: *"Este item foi recuperado por Thaís
durante a Fase 2 e não estava registrado na Fase 1. **É condição, não
sugestão.**"*

### C1 — Fatia vertical: cada funcionalidade vai do banco até produção antes de a próxima começar

`FASE2_3...` 84 a 90. Nada de terminar todos os modelos, depois todas as
views, depois todos os testes. Custo registrado: cerca de 10% a mais de tempo
bruto. Benefício: *"em qualquer semana existe algo inteiro e no ar.
Interrupção na semana 6 deixa um sistema pequeno funcionando, não um
esqueleto."* Motivo: *"é a correção direta do que aconteceu no SkillBridge"*.

**Origem: REGISTRO**, declarado como recuperado de Thaís e como condição.

### C2 — Ferramental completo desde a fatia zero, antes da primeira funcionalidade

`FASE2_3...` 92 a 105. A lista: `uv` para pacotes e ambiente, `ruff` como
linter e formatador, `mypy` para tipos, `pre-commit` como trava antes do
commit, `pytest` com relatório de cobertura, Docker e Docker Compose com
PostgreSQL, integração contínua que **barra merge**, e **deploy vazio no ar na
primeira semana** — um endereço de saúde respondendo em produção antes de
existir qualquer funcionalidade.

Custo estimado ali: 20 a 28 horas.

**Origem: REGISTRO.**

**O estado corrente encosta e não registra:** §9 diz que o avaliador espera
"roda na máquina dele com um comando" e "integração contínua que barra merge".
São dois itens dos oito, escritos como expectativa de avaliador, não como
decisão de construção.

### C3 — A primeira fatia depois da autenticação nunca foi escolhida

`HANDOFF...` 47 e `CORRECAO...` 286 listam isto como entregável da Fase 4 que
nunca foi produzido.

**Origem: ABERTO.**

---

# BLOCO D — MODELAGEM DO REMÉDIO E DO USO

Aqui está o maior volume de decisão real que ficou fora. O estado corrente
fechou nome, duplicidade, estado e doença — e **não registrou a maior parte
dos campos**.

### D1 — A regra "não pode haver dois usos ativos do mesmo medicamento" está derrubada

`HANDOFF...` 68 e `MODELAGEM...` 192. Derrubada por contraexemplos de Thaís:
remédio tomado três vezes ao dia; remédio de pressão de manhã e de noite; dose
diferente em horários diferentes do mesmo remédio. **FALA** registrada em
`MODELAGEM...` 194: *"Isso aí encontra barreiras na vida real da pessoa."*

E o aprendizado que ficou registrado junto, `HANDOFF...` 72: *"quando uma
regra de unicidade choca com a realidade, o problema quase nunca é a regra — é
que falta um atributo no modelo, e a regra está compensando essa falta."*

**Origem: FALA.**

**Continua aberto ao lado disso** (`MODELAGEM...` 198): se alguma regra
substitui a derrubada, ou se nenhuma substitui.

### D2 — Frequência estruturada, não texto livre

`HANDOFF...` 74, com **FALA** na linha 76: *"Eu prefiro uma frequência
estruturada, com campos separados e opções."*

Estruturam-se **quantas vezes** e **unidade de tempo** (diário, semanal, dias
específicos). Datas também estruturadas.

**Origem: FALA.** Não está no estado corrente.

### D3 — O critério que decidiu isso, e que ela mesma formulou

`HANDOFF...` 80: *"estrutura-se o que o sistema precisa **entender**;
deixa-se livre o que o sistema só precisa **guardar e devolver**."*

Registrado ali como *"critério que orientou esta e as decisões seguintes,
formulado por Thaís e adotado como regra"*.

**Origem: REGISTRO de uma formulação atribuída a ela**, sem aspas na origem.

**Por que vale registrar:** é o critério que decide sozinho várias das listas
pequenas ainda abertas do bloco H. E é o mesmo critério que `CORRECAO...` 186
registra como tendo sido **mal aplicado** por Claude uma vez, contra o
critério mais forte de não devolver a dor ao usuário.

### D4 — A dose é só um número

`CORRECAO...` 172, **DECIDIDO**. `FUROSEMIDA · 50 mg · comprimido`, dose `2` —
lê-se "2 comprimidos" porque a forma já diz qual é a unidade.

Consequência registrada na linha 176: *"Não existe verificação de coerência
entre forma e dose, porque não há duas listas para combinar. Nenhum mapa a
escrever, nenhuma regra a testar."*

Contra assumido na linha 178: quebra para insulina, cuja forma é caneta e cuja
dose se mede em unidades internacionais. Quem usa insulina registra a dose em
unidades da caneta.

**Origem: REGISTRO de decisão dela** — `CORRECAO...` 182 detalha que Claude
recomendou texto livre, **Thaís recusou**, e registra os três defeitos do
argumento de Claude. A recusa é dela; a formulação final é do documento.

**Não está no estado corrente.**

### D5 — A forma do remédio: lista fechada com opção de escape

`CORRECAO...` 164, **DECIDIDO**, e a ideia é dela. A lista: comprimido,
cápsula, gota, ml, sachê, adesivo, supositório, pomada — mais opção "outra".

O argumento que a sustenta, linha 168: *"o campo não foi acrescentado; foi
movido para onde pertencia"* — era a unidade da dose, que se repetia em cada
período de uso quando é característica da caixa e nunca muda.

**Origem: REGISTRO de ideia dela.**

**O estado corrente usa a forma sem nunca a definir.** §3.1 põe a forma dentro
da trava de duplicidade e §3.2 dá a ela o valor padrão "não informada" — mas em
nenhum lugar o documento diz **o que é o campo forma, que é lista fechada, nem
quais valores tem**. E fica uma pergunta nova, criada pela §3.2 e nunca feita:
"não informada" é um item a mais dentro dessa lista?

### D6 — Concentração: valor numérico livre, unidade de lista fechada com opção "outro"

`HANDOFF...` 94, **DECIDIDO**. Pesquisado antes de decidir: não existe lista
universal de concentrações; o que é lista fechada é a **unidade**.

**FALA** em `MODELAGEM...` 105 sobre o valor: *"o valor pode ser gigante mesmo.
E aí é melhor deixar um número livre"*. E a opção "outro" foi justificada por
ela pelo caso da pomada.

Unidades já decididas: mg, g, ml, outro. Ainda abertas: mcg, unidade
internacional, mg/ml — *"não sei se a gente coloca essas outras coisas não"*.

**Origem: FALA.**

**O estado corrente cita "valor da concentração" e "unidade da concentração"
dentro da trava de duplicidade (§3.1) sem nunca ter registrado a decisão que
criou esses dois campos.**

### D7 — Remédio é nome e concentração numa tabela só

`HANDOFF...` 102 e `MODELAGEM...` 147, **DECIDIDO** — o chamado caminho 1.
`FUROSEMIDA 5 mg` e `FUROSEMIDA 20 mg` são duas linhas da mesma tabela.

O argumento, que os documentos registram como a defesa em entrevista: separar
substância de apresentação é a modelagem de um catálogo farmacêutico — o
projeto que se decidiu não construir. *"O que está na gaveta não é furosemida;
é uma caixa de furosemida 5 mg."*

Contra assumido: se a pessoa toma o mesmo remédio em duas concentrações, o
nome aparece repetido e agrupar exige consulta mais trabalhosa.

**Origem: REGISTRO.**

**O estado corrente decide o nome (§13.1) e a trava (§3.1) sem registrar a
decisão de desenho que está por baixo das duas.**

### D8 — A relação entre remédio e período de uso é um-para-muitos

`HANDOFF...` 112 e `MODELAGEM...` 36, registrado expressamente porque houve
confusão na conversa: um remédio tem vários períodos; cada período pertence a
um só remédio; não há tabela intermediária.

**Origem: REGISTRO.**

**Por que continua valendo a pena escrever:** o estado corrente hoje tem duas
relações muitos-para-muitos (compartilhamento e doença) e nunca diz quais
relações **não** são. É a informação que impede a confusão de voltar.

### D9 — Quase tudo é opcional, com algumas exceções que nunca foram confirmadas — **RESOLVIDO em 26/08/2026**

`CORRECAO...` 190, **DECIDIDO**, com **FALA** na linha 192: *"Esses campos
todos têm que ser opcional. (...) Isso não é para um médico, isso não é para
uma farmácia. Isso é pra uso pessoal. Então, obrigar a pessoa a preencher
qualquer coisa, tirando o cadastro, seria um furo no sistema."*

E logo abaixo, linha 196, **CLAUDE**: duas exceções *"apontadas por Claude e
não contestadas — confirmar em uma linha"*: o **nome do remédio**, e a
**ligação entre o período de uso e o remédio**. O argumento é que não são dados
sobre o remédio, são o que faz a linha existir.

**Aqui há uma contradição viva com o estado corrente, e ela precisa de
resposta:** §1.1 diz, sem exceção, *"Não existe campo obrigatório"*. Mas §3.3
descreve o comportamento da trava com o exemplo *"dois cadastros do mesmo
remédio sem nada preenchido **além do nome**"* — o que pressupõe que o nome
está lá.

Um remédio sem nome nenhum é uma linha que não representa nada, e entra na
lista da pessoa como um espaço em branco. Ou o nome é obrigatório e a §1.1
precisa dizer isso, ou o nome é opcional e o sistema aceita cadastrar nada.
**As duas leituras estão escritas hoje, em seções diferentes do mesmo
documento.**

---

> **RESOLVIDO em conversa de 26/08/2026.** Thaís decidiu: **o nome do remédio é
> obrigatório**, e não tem tamanho mínimo. **E-mail e senha também são
> obrigatórios**, e sempre foram — a regra "nada é obrigatório" vale para os
> dados que a pessoa registra, nunca para as credenciais da conta. Os demais
> dados do remédio continuam opcionais. A §1.1 do estado corrente foi reescrita
> e a §13.7 foi criada; a §12.2 passou a registrar a senha.
>
> Palavras dela: *"Não precisa ter dosagem, não precisa ter mais nada, mas
> precisa ter o nome do remédio."*
>
> **As exceções não eram duas — são mais.** O que ficou obrigatório, hoje:
>
> | Campo | Situação |
> |---|---|
> | e-mail e senha da conta | **DECIDIDO em 26/08/2026** (§1.1, §12.2) |
> | nome do remédio | **DECIDIDO em 26/08/2026** (§1.1, §13.7) |
> | ligação entre o período de uso e o remédio | **DECIDIDO em 26/08/2026** (§17.4-A). Não existe período de uso solto; sem isso ele não teria dono, porque o dono se descobre atravessando o remédio (§17.1) |
> | identificador da conversa do Telegram | obrigatório **para quem usa o bot**, e só para essa pessoa — sem ele o bot não tem para onde responder (§7.3, §7.6). Quem não fala com o bot nunca tem esse dado |

---

# BLOCO E — TELEGRAM: O QUE AINDA FALTA

### E1 — Como quem fala com o bot prova ser dono da conta

`FASE2_3...` 133, dentro da proposta original do Telegram: *"Custo lateral:
exige guardar o identificador da conversa vinculado ao usuário, e decidir como
quem fala com o bot prova ser quem diz ser."*

`PROMPT_VISIBILIDADE...` 82 repete o mesmo custo lateral e acrescenta a peça
que ajuda: *"quem inicia é o dono, do próprio celular — o ato de falar com o
bot **é** o que vincula a conversa à conta"*.

**Origem: ABERTO.** Nenhum documento decide o mecanismo.

**Por que isto bloqueia:** o estado corrente decidiu o Telegram (§7.1) e
decidiu o webhook (§7.4), e não decidiu **como o backend sabe de quem é a
conversa que chegou**. Sem isso, o endpoint do Telegram não tem como responder
nada — e provavelmente há uma coluna ou uma tabela nova na modelagem
dependendo da resposta. É o único item do levantamento que bloqueia a
integração já decidida.

### E2 — Nenhum telefone é necessário, e a suposição contrária não é decisão dela

`PROMPT_VISIBILIDADE...` 84: Thaís supôs que um telefone seria necessário,
por não conhecer o mecanismo do bot. *"A suposição está corrigida e não deve
ser registrada como decisão dela."*

**Origem: REGISTRO de uma correção.** Não é decisão, é o oposto: é o aviso de
não tratar como decisão. Vale entrar como nota, para não voltar.

---

# BLOCO F — ESCOPO EXCLUÍDO QUE SUMIU DAS LISTAS

Três exclusões decididas que **não estavam** em `O_QUE_O_PROJETO_NAO_FAZ.md`,
que é hoje a lista viva.

> **Bloco fechado em 26/08/2026.** Duas viraram item da lista — histórico
> versionado (item 20) e calendário/agendamento (item 21). A terceira, o
> serviço de modelo de linguagem, foi descartada por Thaís como resíduo da fase
> de escolha do projeto e **não vira item**.

### F1 — Histórico versionado por período — **INCORPORADO em 26/08/2026**

> Virou o **item 20** de `O_QUE_O_PROJETO_NAO_FAZ.md`, com a fronteira escrita:
> estado do remédio e períodos de uso ficam **dentro**; guardar em que dia o
> estado mudou fica **fora**. A §2 do estado corrente ganhou a linha
> correspondente. Confirmado por fala de Thaís em 26/08/2026.

`FASE2_3...` 137: *"Guardar histórico versionado por período (responder 'o que
ele tomava em 15 de março') foi discutido, custa 145–180h e sai do escopo.
Fica registrado como evolução possível."*

Estava como item 4 na lista de onze de `CORRECAO...` 299, e como item 4 na
lista de sete de `HANDOFF...` 197. **Não está na lista atual.**

**Origem: REGISTRO**, com número de horas.

**Por que importa:** é a exclusão mais fácil de reintroduzir sem perceber. A
§2 do estado corrente decidiu que o remédio tem estado próprio (em uso /
suspenso), e a pergunta "e quando ele mudou de estado?" é o primeiro passo de
volta para o histórico versionado.

### F2 — Serviço de modelo de linguagem — **NÃO ENTRA NA LISTA**

`PROMPT_VISIBILIDADE...` 100: *"Descartado por Thaís — a pessoa não pesquisa
nada, só registra e consulta o que registrou."*

> **DECIDIDO em 26/08/2026: não vira item da lista do que o projeto não faz.**
> Palavras de Thaís: *"ele nem tem que entrar, porque isso daí tinha muito mais
> a ver com a questão de quando a gente estava planejando qual seria o projeto,
> eu falei que não era uma integração com LLM. Então acabou que ficou isso solto
> aí totalmente errado."*
>
> Era resíduo da fase de **escolher** o projeto, não decisão de escopo deste
> projeto. A lista de exclusões existe para o README, e um item assim só
> confundiria quem lê. O assunto já está coberto pelo item 4 da lista — o
> projeto tem exatamente uma integração externa, e é o Telegram.

### F3 — Calendário e agendamento de consulta — **INCORPORADO em 26/08/2026**

`PROMPT_VISIBILIDADE...` 99: *"Descartado por Thaís: o projeto não marca
consulta nem agenda nada."*

> Virou o **item 21** de `O_QUE_O_PROJETO_NAO_FAZ.md`, confirmado por Thaís em
> 26/08/2026 com citação literal: *"esse projeto é um projeto para uso pessoal
> e não é pra virar um projeto médico, em que a pessoa faz agendamento de
> consultas, faz calendários, nada disso."*

---

# BLOCO G — VOCABULÁRIO

### G1 — A palavra "titular" sai de circulação — **CONFIRMADO em 26/08/2026**

> Deixou de ser proposta de Claude. Palavras de Thaís: *"Não existe titular. A
> API vai ter apenas um usuário que irá se cadastrar e ele poderá registrar seus
> dados de remédios e doenças e poderá compartilhar esses dados com um terceiro
> que também é um usuário cadastrado e vice e versa."* Escrito na §4.1 do estado
> corrente, e a palavra foi trocada no texto vivo do estado corrente e da lista
> do que o projeto não faz. Citações literais anteriores ficaram como estavam.

`CORRECAO...` 240, marcada no próprio documento como **PENDENTE DE
CONFIRMAÇÃO** — ou seja, **CLAUDE**, nunca confirmado por Thaís.

A proposta: **usuário** é quem tem conta, faz login e registra os próprios
remédios e doenças; **convidado** é a conta que recebeu e aceitou acesso de
leitura. E convidado é palavra de conversa, não campo no banco.

**Situação hoje:** o estado corrente usa "titular" o tempo todo — §7.1
("usado pelo próprio titular"), §6.3, §6.4. Ou seja, a proposta de aposentar a
palavra não pegou, e nunca foi confirmada nem descartada. Está viva num
documento e ignorada no outro.

---

# BLOCO H — LISTAS PEQUENAS AINDA ABERTAS

`CORRECAO...` 255 chamava isto de "nove listas a fechar". Duas foram fechadas
depois — o nome do remédio, pela §13.4 e §13.5 do estado corrente, e a lista de
doenças, pela §5.2. **Estas seis continuam abertas**, e nenhuma aparece no
estado corrente:

| # | O que falta decidir | Onde está registrado |
|---|---|---|
| H1 | quais unidades de concentração além de mg, g, ml — entram mcg, unidade internacional, mg/ml? | `CORRECAO...` 259, `MODELAGEM...` 116 |
| H2 | quais formas entram na lista da caixa, e se "não informada" é uma delas | `CORRECAO...` 260, mais a §3.2 do estado corrente |
| H3 | quais valores a frequência aceita — diário, semanal, dias específicos? | `CORRECAO...` 261, `MODELAGEM...` 166 |
| H4 | a frequência tem opção "outro"? | `CORRECAO...` 262. Claude recomendou que não; Thaís nunca respondeu |
| H5 | a opção "outro" na unidade de concentração carrega texto livre, ou é só rótulo? | `CORRECAO...` 263 |
| H6 | confirmar que "outras" na doença **não** carrega texto livre | `CORRECAO...` 264, marcado como derivado a confirmar em uma linha |

**Origem de todas: ABERTO.**

Nenhuma muda o desenho das tabelas. Todas precisam estar decididas antes de
escrever o modelo, porque são o conteúdo das listas fechadas.

---

# O QUE NÃO ENTROU NESTE LEVANTAMENTO, E POR QUÊ

Registro para não parecer omissão.

- **Os critérios de escolha de projeto** (`FASE2_3...` 194 a 243, oito
  critérios) — são critérios para **escolher** um projeto. O projeto está
  escolhido e confirmado (§0). O único que continua operando é o segundo — o
  sistema tem que resolver a dor, não devolvê-la ao usuário — e o estado
  corrente já o cita, na §5.
- **Os erros de método registrados** (`FASE2_3...` 267, `CORRECAO...` 180,
  `MODELAGEM...` 22) — são sobre como conduzir a conversa, não sobre o
  produto. Pertencem a `REGRAS_COMPORTAMENTO_PROJETO.md`.
- **As vinte regras de comportamento** — já vivem em documento próprio, e a
  Fase 5 as trata como regras de método. Uma observação, porém: `FASE1...`
  215, `PROMPT_VISIBILIDADE...` 111 e o arquivo de regras trazem **três
  conjuntos diferentes** de regras de trabalho, com deriva entre eles. A
  auditoria já apontou isso na Parte 2 e ninguém decidiu qual vale.
- **A discussão sobre o feed de calendário contar como zero integrações**
  (`FASE2_3...` 259) — o próprio documento diz que *"não afeta o projeto
  escolhido"*.
- **A pesquisa de fontes de dados da Fase 2** (`FASE2_3...` 171) — foi para
  escolher entre candidatos que já foram descartados.
- **Tudo que a modelagem e o handoff dizem sobre `Titular`** — a tabela deixou
  de existir por decisão dela (`CORRECAO...` 71, *"sim confirmo"*), e a §4 do
  estado corrente fecha o assunto.
