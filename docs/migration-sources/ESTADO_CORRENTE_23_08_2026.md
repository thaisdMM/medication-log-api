# ESTADO CORRENTE — decisões da conversa de 23/08/2026

**O que este documento é:** o registro das decisões fechadas e das pendências
abertas na conversa de 23/08/2026. Substitui, nos pontos que trata, qualquer
afirmação em contrário de documento anterior.

**O que este documento NÃO é:** não é o estado completo do projeto. Ele cobre
apenas os itens tratados nesta conversa. Não tem spec, roadmap, endpoints,
tasks nem código.

**Procedência — e ela importa.** O parágrafo abaixo descreve a conversa de
**23/08/2026**, e só ela.

Abertos e lidos por inteiro naquele dia: REGRAS_COMPORTAMENTO_PROJETO.md,
AUDITORIA_CONTRADICOES_E_REGRAS.md, FASE1_ESCOPO_PROJETO_PORTFOLIO.md,
e FASE2_3_DECISAO_PROJETO_PORTFOLIO.md.
Não abertos: HANDOFF_FASE4..., MODELAGEM_REGISTRO_MEDICACAO.md,
CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md e os arquivos de prompt.

**Correção de 26/08/2026.** A frase original terminava com *"Nada deste
documento afirma conteúdo desses quatro"*, e ela deixou de valer. As seções
escritas entre 24 e 26/08/2026 leram esses arquivos e os citam com linha —
§1.1, §6.9, §12.2, §13.1, §13.2 e §17.1. **Essas citações valem.**

---

## 0. PROJETO CONFIRMADO

**DECIDIDO.** O projeto continua sendo o **registro pessoal de medicação**.
A viabilidade foi questionada nesta conversa e confirmada por Thaís.
Não se reabre.

Motivo registrado: os doze achados da auditoria são, na maioria,
contradições de documento e decisões pequenas nunca tomadas — não defeitos
do domínio. A causa raiz é documental (Parte 3 da auditoria).

---

## 1. OBRIGATORIEDADE DE CAMPOS

### 1.1 — O que é obrigatório e o que não é

**DECIDIDO.**

- **E-mail e senha são obrigatórios.** Sem eles não existe conta.
- **O nome do remédio é obrigatório.** Sempre que a pessoa optar por salvar um
  remédio, o nome tem que vir. Os demais dados do remédio — concentração,
  unidade, forma, dose — não são obrigatórios.
- **Nada mais é obrigatório.** Registrar remédio é opcional; registrar doença é
  opcional. **Não existe "pelo menos um remédio obrigatório".** Conta com zero
  remédios e zero doenças é estado legítimo e permanente.

Criar conta e nunca registrar nada é uso normal: a pessoa não chama o endereço
de remédios, nada é exigido dela, e a resposta do sistema é lista vazia. Quem
não registrou nada **não tem linha nenhuma** — não tem coluna vazia. A
obrigatoriedade do nome só existe dentro da requisição que cria o remédio.

Justificativa de Thaís: um sistema que a pessoa faz para si mesma não pode
exigir preenchimento; baixar um aplicativo, criar conta e não preencher nada
é comportamento normal de usuário.

**Origem:** Thaís, 26/08/2026 — _"O e-mail, senha, isso daí tem que ser
obrigatório. Isso é parte definida do projeto."_ e _"Não precisa ter dosagem,
não precisa ter mais nada, mas precisa ter o nome do remédio."_ A distinção
entre linha nenhuma e coluna vazia vem de
`CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 90.

### 1.2 — Retratação registrada

**ERRO DE CLAUDE, corrigido nesta conversa.** Foi afirmado que "tudo opcional
drena o projeto" e que a opcionalidade poderia matá-lo. **Está errado e a
afirmação é retirada.**

O diagnóstico correto: os dois problemas apontados (data de fim ambígua e
trava de duplicidade) são problemas de **modelagem**, não consequência da
opcionalidade. Ambos têm solução sem obrigar ninguém a preencher nada.

**Alerta para quem retomar:** a auditoria, na linha 202, e a correção da
modelagem, citada na linha 243 da auditoria, empurram na direção de tornar
campos obrigatórios. **Essa direção está descartada.**

### 1.3 — O princípio que substitui a discussão

> **Campo opcional não é problema. Dar significado à ausência do campo é.**

Um campo vazio significa uma coisa só: ninguém preencheu. Se o sistema
precisa saber um estado, esse estado é um dado próprio — nunca uma inferência
sobre o vazio.

### 1.4 — Peso de projeto não vem de obrigar

**CRITÉRIO REGISTRADO.** Três níveis de regra, e só o terceiro pesa:

| Nível                                                               | Exemplo                                                       | Vale como engenharia?          |
| ------------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------ |
| Campo obrigatório                                                   | "nome não pode ser vazio"                                     | Não. É uma linha de serializer |
| Regra entre campos do mesmo registro                                | "fim não pode ser antes do início"                            | Pouco                          |
| **Invariante** — envolve mais de um registro, ou estado, ou o banco | "ninguém enxerga o que não é seu"; "não pode haver duplicata" | **Sim**                        |

---

## 2. ESTADO DO REMÉDIO

**DECIDIDO.** O remédio tem um campo de estado próprio.

Comportamento visível: a pessoa cadastra um remédio e ele **já aparece na
lista como "em uso"**, sem ela ter digitado ou clicado em nada. Quando parar
de tomar, ela marca "suspenso".

Consequências:

- A data de fim volta a ser campo comum e **opcional**, sem significar estado.
- A lista de ativos passa a ser computável sem ambiguidade.
- **Fica revogada** a decisão anterior de que "data de fim vazia = em uso".

Isso encerra o achado AUD-05 da auditoria.

**O estado não é histórico — acrescentado em 26/08/2026.** "Em uso / suspenso"
é **um valor sobrescrito**, não uma linha do tempo. O sistema não guarda em que
dia o remédio mudou de estado, e guardar isso seria histórico versionado, que
está excluído no item 20 da lista do que o projeto não faz. Quem responde
"quando eu tomei" são os períodos de uso, com início e fim, vários por remédio.

**Para que o campo serve, na prática:** a pessoa **suspende em vez de apagar**.
Apagar o remédio levaria junto os períodos de uso dele; suspender guarda tudo, e
voltar a tomar é abrir um período novo.

---

## 3. TRAVA DE DUPLICIDADE — VERSÃO SUPERADA, NÃO LEIA COMO DECISÃO

> ⚠️ **SUPERADA em 24/08/2026. A decisão vigente é a "§3 — TRAVA DE
> DUPLICIDADE — DECIDIDA", mais abaixo neste arquivo**, com as subseções §3.1
> a §3.10. Este texto ficou aqui como registro do estado em 23/08/2026.
> Marcado em 26/08/2026, porque duas seções com o mesmo número, uma dizendo
> ABERTO e a outra DECIDIDO, faziam "§3" não identificar um texto só.

**ABERTO em 23/08/2026 — resolvido no dia seguinte.**

O problema, confirmado nesta conversa: no PostgreSQL dois campos vazios não
são considerados iguais entre si, então dois cadastros incompletos passam
pela trava.

**A saída "obrigar a preencher" está descartada** pela decisão 1.1.
Restam duas:

| Saída                                                | A favor                                                                                                                 | Contra                                                                                            |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Declarar no banco que vazio conta como igual a vazio | resolve sem tocar no usuário                                                                                            | **pista a confirmar na documentação oficial** das versões que serão usadas. Não é fato verificado |
| Aceitar duplicata e declarar no README como decisão  | custo zero; vira argumento de entrevista bom ("preferi aceitar duplicata a obrigar a pessoa a inventar a miligramagem") | a lista pode ter linhas repetidas                                                                 |

**Pendência ligada, não resolvida:** a trava foi decidida sobre a tupla
nome + valor + unidade, antes de o campo "forma" existir. Ela precisa ser
revista de qualquer modo (achado AUD-06).

---

## 4. USUÁRIO — UM SÓ, SEM TIPO

**DECIDIDO.** Existe **um único tipo de conta**.

Ser dono dos próprios registros e ser convidado de terceiro são **situações
simultâneas e reversíveis da mesma conta**, não naturezas diferentes.
Não existe "usuário que registra" e "usuário que só recebe".

Teste que sustenta: quem criou conta só para ver a lista do avô pode, meses
depois, passar a registrar os próprios remédios. Não muda de nada — apenas
passa a ter registros próprios.

Regra transferível registrada: _o que a conta tem vira relação; o que a conta
é vira tipo — e só é tipo se nunca mudar._

### 4.1 — A palavra é "usuário". "Titular" sai de circulação

**DECIDIDO em conversa de 26/08/2026.**

**Palavras de Thaís:** *"Não existe titular. A API vai ter apenas um usuário
que irá se cadastrar e ele poderá registrar seus dados de remédios e doenças e
poderá compartilhar esses dados com um terceiro que também é um usuário
cadastrado e vice e versa."*

| Palavra | O que quer dizer |
| --- | --- |
| **usuário** | quem tem conta, faz login e registra os próprios remédios e doenças. **É o único papel que existe** |
| **dono do dado** | o usuário a quem aquele registro pertence. É como a regra de permissão fala |
| **convidado** | o usuário que recebeu e aceitou acesso de leitura ao dado de outro. **É palavra de conversa, não campo no banco** — ser convidado é ter uma linha de `Compartilhamento` aceita, e é reversível |

**"Titular" está revogada.** Ela sugeria uma categoria de conta que não existe,
e contrariava esta seção 4: um único tipo de conta, sem marca de tipo.

Fecha a proposta de `CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 240, que estava
marcada como PENDENTE DE CONFIRMAÇÃO desde então.

**Onde a palavra sobrevive de propósito:** nas citações literais de Thaís
anteriores a esta data, que não se altera, e nas referências à antiga tabela
`Titular`, que deixou de existir por decisão dela (`CORRECAO...` 71) e é citada
como história, não como desenho.

---

## 5. DOENÇA — VERSÃO SUPERADA, NÃO LEIA COMO DECISÃO

> ⚠️ **SUPERADA em 24/08/2026. A decisão vigente é a "§5 — DOENÇA —
> DECIDIDO", mais abaixo neste arquivo**, com as subseções §5.1 a §5.4. Este
> texto ficou como registro do estado em 23/08/2026, e a pendência estrutural
> que ele declara já foi fechada pela §5.2. Marcado em 26/08/2026.

**DECIDIDO em 23/08/2026, e ampliado depois.**

- Doença é entidade própria, de cadastro **opcional**.
- **Não tem vínculo com remédio.** O sistema não pergunta "este remédio é
  para qual doença".
- Doença é compartilhável, como o remédio.

**Proposta de Claude descartada por Thaís:** ligar cada remédio à doença que
ele trata. Argumento dela, aceito: a pessoa frequentemente não sabe a própria
doença nem sabe dizer qual remédio trata o quê; este não é um sistema de
profissional de saúde, e exigir esse conhecimento devolve a dor ao usuário —
o que contraria o critério C2 da Fase 2.

**Pendência herdada, não resolvida aqui:** se a lista de doenças é tabela no
banco ou lista escrita no código. É decisão **estrutural**, não escolha de
lista (achado AUD-08).

---

## 6. COMPARTILHAMENTO COM ESCOPO — VERSÃO SUPERADA, NÃO LEIA COMO DECISÃO

> ⚠️ **SUPERADA em 24/08/2026. A decisão vigente é a "§6 — COMPARTILHAMENTO —
> DECIDIDO", mais abaixo neste arquivo**, com as subseções §6.1 a §6.11. As
> três perguntas de integridade que este texto declara em aberto estão todas
> fechadas: a §6.2 resolve duas e a §6.10 resolve o autoconvite. Marcado em
> 26/08/2026.

**ABERTO em 23/08/2026 — resolvido no dia seguinte.**

Palavras dela: o titular escolheria o que compartilha — só remédios, só
doenças, ou os dois.

| Saída                | A favor                                                                                                  | Contra                                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Convite com escopo   | permissão deixa de ser filtro e vira regra de negócio real; é o ponto tecnicamente mais forte do projeto | cada consulta verifica duas perguntas; os testes multiplicam (dono, convidado com acesso, convidado sem acesso, estranho) |
| Convite tudo-ou-nada | mais simples, entrega antes                                                                              | perde o ponto mais interessante de permissão                                                                              |

**Pendências de integridade que continuam sem decisão** (achado AUD-09):
uma conta pode convidar a si mesma? pode existir mais de um convite entre as
mesmas duas contas? convite recusado pode ser refeito?

---

## 7. INTEGRAÇÃO EXTERNA — TELEGRAM

### 7.1 — Decisão

**DECIDIDO por Thaís nesta conversa.** A integração externa do projeto é o
**Telegram**, em modo consulta, usado **pelo próprio usuário** — ele manda um
comando ao bot e recebe a sua lista.

Isso satisfaz a restrição de exatamente uma integração externa. O projeto
deixa de estar fora da própria regra.

### 7.2 — Status anterior corrigido

**Os documentos que dizem "Telegram — fora do escopo" estão ERRADOS e
superados.** Segundo a auditoria, essa frase aparece em pelo menos dois
arquivos e nunca foi decisão de Thaís — era proposta de Claude não confirmada
(achado AUD-03).

### 7.3 — O que já estava verificado (Fase 1, §6.2, em 21/08/2026)

- O bot se cria conversando com o BotFather no próprio aplicativo, comando
  `/newbot`, que devolve um token.
- Sem conta empresarial, sem aprovação de terceiro, sem espera.
- Existe biblioteca Python madura (o documento não nomeia qual).
- Bots não podem iniciar conversa: a pessoa fala com o bot primeiro e o
  backend guarda o identificador daquela conversa.

**A pergunta "é possível?" está respondida: é. Não precisa ser repesquisada.**

### 7.4 — Consequência técnica nova, registrada nesta conversa

Um bot funciona de dois modos:

| Modo                             | O que exige                                 | Situação                                                                                 |
| -------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Consulta contínua (long polling) | processo rodando o tempo todo               | **PROIBIDO** — é worker permanente, vedado pela decisão de hospedagem gratuita da Fase 1 |
| **Webhook**                      | o Telegram chama uma URL pública do sistema | **É o caminho** — vira um endpoint da própria API                                        |

Efeito colateral bom: receber webhook é vocabulário de anúncio de vaga, e é a
mesma mecânica que Thaís já usou no Stripe.

### 7.5 — Risco a pesquisar antes da implementação

O serviço gratuito hiberna após 15 minutos sem tráfego e leva 30–60s para
voltar (dado da Fase 1, a reverificar). O Telegram tem limite de espera e
política de reenvio quando a chamada falha.

**A pesquisar, e só isso:** qual o limite de tempo que o Telegram espera de um
webhook, qual a política de reenvio, e se o tempo de retorno da hibernação
cabe dentro disso. Pesquisa **não autorizada ainda**.

---

### 7.6 — O identificador da conversa é guardado, e é dado pessoal

**Registrado em 26/08/2026.**

Para responder, o bot precisa saber **para onde** responder. O Telegram dá um
número à conversa, e esse número fica guardado ligado à conta (§7.3). Sem ele
não há integração.

**Isso é dado pessoal**, porque liga a conta do sistema a uma conta de
Telegram. Por isso passa a estar declarado no item 15 da lista do que o
projeto não faz, que antes dizia que nada além de nome e e-mail seria
guardado.

**Não é telefone.** O sistema não pede, não vê e não guarda número de
telefone. O telefone é exigido pelo Telegram para a pessoa ter conta lá, e
essa relação não passa pelo nosso sistema. A suposição contrária foi levantada
por Thaís e corrigida em `PROMPT_VISIBILIDADE_E_INTEGRACAO_V2.md` 84.

**Quem não usa o Telegram não tem esse dado.** Ele só nasce quando a pessoa
fala com o bot pela primeira vez, porque bot não inicia conversa (§7.3).

**ABERTO, e é o único item que bloqueia a integração já decidida:** como o
backend confirma que a conversa que chegou pertence àquela conta. Nenhum
documento decide o mecanismo (`FASE2_3...` 133,
`PROMPT_VISIBILIDADE_E_INTEGRACAO_V2.md` 82). Provavelmente há coluna ou
tabela nova na modelagem dependendo da resposta.

---

## 8. E-MAIL

**DECIDIDO.**

- E-mail **não é** a integração externa do projeto. É acréscimo posterior,
  se fizer sentido.
- **Nos testes:** backend de memória. Isso é boa prática, não concessão —
  teste que envia e-mail de verdade é lento e instável.
- **Em desenvolvimento local:** backend de console.
- **Em produção:** **console também.** Ninguém recebe e-mail.
- O envio fica atrás de uma abstração, com o backend escolhido por variável
  de ambiente. O código não conhece o provedor.

**Corrigido em 26/08/2026.** Esta linha dizia *"Em produção: em aberto"*, de
23/08/2026. Deixou de valer no dia seguinte: a §6.7 decidiu que **entrega real
de e-mail não vai existir neste projeto**, e o item 5 da lista do que o projeto
não faz registra a mesma coisa. A abstração continua existindo — é ela que
deixa o convite funcionar sem provedor nenhum configurado.

**Pesquisa de custo e camada gratuita: ADIADA por decisão de Thaís**, para a
hora da implementação e do deploy. Motivo dela, aceito: essa informação muda,
e planejar hoje sobre número que expira é o que matou a fonte de dados de
passagens na Fase 2.

**Consequência a vigiar:** se o e-mail um dia passar a enviar de verdade em
produção, o projeto passa a ter **duas** integrações externas, e a restrição
de exatamente uma precisa ser revogada por Thaís, explicitamente. Com a §6.7,
essa hipótese está fechada dentro deste projeto — a vigilância vale para quem
retomar depois.

---

## 9. CRITÉRIO DE AVALIAÇÃO DO PROJETO

Registrado a pedido de Thaís: o que faz um avaliador reconhecer trabalho de
programador júnior competente, em ordem de peso:

1. Está no ar e responde. O link funciona, a documentação da API abre.
2. Roda na máquina dele com um comando, com banco junto e testes passando.
3. Os testes testam algo real — em especial **o usuário B não alcança o dado do
   usuário A**. O código é **404**, e o motivo está na §17.5: o dado não está
   no conjunto dele, e a resposta não revela sequer que existe.
4. A API se comporta como API: códigos de status corretos, erro de validação
   que diz o que está errado, paginação, consistência entre endpoints.
5. O README explica decisões, **incluindo a lista do que o projeto não faz**.
6. Histórico de commits legível e integração contínua que barra merge.

**Nada nessa lista depende de obrigar campo.** Tudo depende de terminar e
publicar.

### O que o projeto dá para defender em entrevista

- Dado de saúde tratado como categoria especial, com ambiente público sem
  dado real.
- Isolamento por dono verificado em toda consulta, com teste de acesso negado.
- Convite como relação com estado, conta com conta.
- Entrega ponta a ponta com ferramental que barra merge.

### O que ele não dá, e é melhor saber antes

Nada sobre algoritmo, desempenho, concorrência ou volume. Se o avaliador
puxar por aí, a resposta é que o projeto trata de isolamento de dado
sensível — e essa resposta é boa desde que seja escolha, não improviso.

---

## 10. REGRA DE COMUNICAÇÃO NOVA

**E6 — Comportamento antes de mecanismo.**

Explicar primeiro o que o usuário vê acontecer, com exemplo concreto; só
depois como funciona por baixo.

> **Erro que gerou:** o estado do remédio foi explicado como "estado vira dado
> próprio com valor padrão". Thaís não tinha como reconhecer nisso a solução
> que ela mesma aceitou em uma linha quando foi dito: _"ela cadastra o remédio
> e ele já aparece como em uso; quando parar, marca suspenso"_. Custou meia
> conversa.

---

## Atualização 24/08/2026

Sobre **"Compare os 16 assuntos do bloco 1 do índice com o estado corrente"**:

**RESOLVIDO** = o estado corrente já fechou o assunto ou já matou a contradição; não volta para o segundo passo.
**PENDENTE** = sobra alguma coisa. Nem toda pendente é pergunta para você — várias se fecham sozinhas pelas cinco regras do segundo passo, sem você decidir nada.

| #   | Assunto                        | Status        | Onde                                                                | O que sobra                                                                                                           |
| --- | ------------------------------ | ------------- | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 1   | Tipo de usuário                | **RESOLVIDO** | §4, reforçado por §1.1                                              | —                                                                                                                     |
| 2   | Telegram                       | **RESOLVIDO** | §7.1, §7.2, §7.4, §7.6                                              | a pesquisa do §7.5, não autorizada; e o vínculo conversa↔conta do §7.6, ABERTO                                        |
| 3   | Trava de duplicidade           | **RESOLVIDO** | §3.1 a §3.6, §3.9, §13.5                                            | o experimento da §3.10, que ainda não rodou                                                                           |
| 4   | Integração externa             | **RESOLVIDO** | §7.1, com §8                                                        | —                                                                                                                     |
| 5   | Compartilhamento               | **RESOLVIDO** | §6.1 a §6.11                                                        | —                                                                                                                     |
| 6   | Obrigatoriedade de campo       | **RESOLVIDO** | §1.1, §12.2, §13.7, §17.4-A                                         | —                                                                                                                     |
| 7   | Doença                         | **RESOLVIDO** | §5.2, §5.3, e §3.9 quanto a "outras"                                | quantas doenças a lista tem — é povoamento do banco, não desenho                                                      |
| 8   | Catálogo de medicamento        | **RESOLVIDO** | §13.1; item 11 da lista do que o projeto não faz                    | —                                                                                                                     |
| 9   | Visibilidade da API            | **RESOLVIDO** | §14                                                                 | —                                                                                                                     |
| 10  | Estimativa de horas            | **RESOLVIDO** | §15                                                                 | não há número; a estimativa se refaz quando o planejamento estiver pronto                                             |
| 11  | Estado do remédio              | **RESOLVIDO** | §2                                                                  | —                                                                                                                     |
| 12  | Dados fictícios × reais        | **RESOLVIDO** | `CORRECAO_MODELAGEM...` §3.3 e `O_QUE_O_PROJETO_NAO_FAZ.md` item 19 | fala de Thaís: _"esse projeto não vai usar dados reais"_                                                              |
| 13  | Prazo                          | **RESOLVIDO** | §15.1                                                               | o prazo é orientação contra inchaço, não muro; o critério de sucesso é terminar                                       |
| 14  | Lista do que o projeto não faz | **RESOLVIDO** | `O_QUE_O_PROJETO_NAO_FAZ.md`, lista única de 19 itens                | —                                                                                                                     |
| 15  | E-mail                         | **RESOLVIDO** | §6.1, §6.7, §6.8 e §8                                               | —                                                                                                                     |
| 16  | Modelagem e endpoints          | **PENDENTE**  | §17 fecha o dono do período de uso                                  | a modelagem final e a lista de endpoints. É a Etapa 3                                                                 |

> **Atualização de 26/08/2026 — a tabela deixou de ser fotografia.**
> A contagem original era de seis mortos e dez restantes, em 24/08/2026, e não
> era atualizada desde então. A coluna de status acima foi refeita hoje contra
> as seções que existem no arquivo agora. **Quinze mortos, um restante:** o
> item 16, que é a Etapa 3.
>
> Corrigido junto, na linha 12, um ponteiro errado: apontava para o **item 18**
> da lista do que o projeto não faz, e a decisão mora no **item 19** — o 18 é o
> limite de compartilhamentos.

> **Correção de 25/08/2026 — os ponteiros quebrados desta tabela.**
> As linhas 10 e 12 apontavam para uma **seção 11 que não está mais no
> arquivo**, e a linha 12 mandava "ver o alerta abaixo", que também não
> existe. A seção foi apagada por Thaís em 24/08/2026, por já estar corrigida
> em decisões posteriores — remoção deliberada, não perda. Os dois ponteiros
> foram refeitos para onde cada decisão mora hoje: a estimativa de horas na
> seção 15, escrita abaixo, e os dados fictícios na correção da modelagem,
> §3.3, com a fala de Thaís que a sustenta.

---

## RESOLVENDO AS PENDENCIAS DA TABELA:

## 3. TRAVA DE DUPLICIDADE — DECIDIDA — **VERSÃO VIGENTE**

**DECIDIDO em conversa de 24/08/2026.**

### 3.1 — A combinação que define "é o mesmo remédio"

A unicidade é declarada sobre: conta + nome + valor da concentração +
unidade da concentração + **forma**.

A forma passa a integrar a combinação. Duas apresentações diferentes do
mesmo remédio são registros diferentes e ambas entram.

Isso revoga a combinação anterior, que era conta + nome + valor + unidade,
decidida antes de o campo forma existir.

### 3.2 — Forma não tem valor padrão

**CORRIGIDO em 26/08/2026.** A redação anterior dizia que a forma recebia o
valor padrão "não informada" quando ninguém escolhia.

**"Não informada" nunca foi decisão de Thaís.** A lista dela, em
`CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 164, tem nove valores e esse não é
um deles (§3.9). O valor padrão veio de uma proposta de Claude — a "opção D" de
uma conversa anterior —, feita como **contorno** para o caso de o banco não
aceitar comparar vazio com vazio. Era plano B do plano B.

**O contorno perdeu a função quando a saída original foi decidida**, na §3.3.

A forma continua opcional e **fica vazia quando ninguém escolhe**: a pessoa não
digita nem clica em nada e o cadastro funciona.

**Condição técnica a não perder de vista:** campo de lista fechada guarda
**texto vazio**, nunca `NULL`. Texto vazio é igual a texto vazio para o banco,
e a forma sozinha nunca fura a trava. Se alguém escrever `null=True` nesse
campo, ele volta a furar. Vale igual para a unidade da concentração.

**Depois das decisões de 26/08/2026, sobrou uma única coluna da combinação da
§3.1 que pode ficar nula:** o **valor da concentração**, que é numérico. Conta
e nome são obrigatórios; unidade e forma são texto. É só para essa coluna que
o `nulls_distinct=False` da §3.3 trabalha.

**Isto pode voltar atrás, e a condição está escrita na §3.10.**

### 3.3 — O vazio da miligramagem deixa de furar a trava

A restrição de unicidade é declarada com `nulls_distinct=False`.

Comportamento visível: dois cadastros do mesmo remédio sem nada preenchido
além do nome — o segundo é recusado como duplicata.

Fato verificado na documentação oficial em 24/08/2026: por padrão o
PostgreSQL não considera dois nulos iguais entre si, e a cláusula
`NULLS NOT DISTINCT` altera esse comportamento. No Django, a opção é
`UniqueConstraint.nulls_distinct`, e é ignorada em bancos que não sejam
PostgreSQL. Ambiente de Thaís: PostgreSQL 17, Django 6.1.

**Leia "verificado" pelo que a palavra diz:** foi verificado na **documentação**
e nunca foi executado. O experimento que transforma isso em fato está na §3.10.

### 3.4 — Nenhum campo obrigatório para fechar a trava

A trava de duplicidade não obriga ninguém a preencher nada, e não existe
obrigatoriedade condicional. A decisão 1.1 continua inteira.

**Precisão acrescentada em 26/08/2026:** o **nome do remédio** é obrigatório
(§1.1, §13.7) e entra nesta combinação. Isso não é exceção à regra acima — o
nome não foi tornado obrigatório para fechar a trava, e sim porque uma linha
de remédio sem nome não representa nada. **Concentração, unidade e forma
continuam todas opcionais**, e é sobre elas que a §3.3 trabalha.

### 3.5 — Posições de reserva, em ordem

**Reescrita em 26/08/2026.** São duas, e a primeira é melhor que a segunda:

1. **Valor padrão na forma.** Se o experimento da §3.10 mostrar que
   `nulls_distinct` não age, a forma passa a receber um valor padrão definido —
   "não informada" — que o banco compara normalmente. É a "opção D" recuperada,
   e ela vira útil de novo exatamente nesse cenário. **Não resolve sozinha:**
   não se aplica ao valor da concentração, que é numérico, e inventar um número
   para significar "não preenchido" é dar significado escondido a um valor,
   contra a §1.3.
2. **Aceitar a duplicata** e registrá-la no README como decisão consciente.

**Obrigar preenchimento continua descartado em todas as hipóteses.**

### 3.6 — Teste obrigatório derivado

A opção `nulls_distinct` é ignorada em silêncio quando o banco não a
suporta. Por isso a definição de pronto inclui um teste que cadastra duas
vezes o mesmo remédio em branco e espera erro de duplicata.

**Acrescentado em 26/08/2026:** o teste precisa verificar também **qual é a
resposta da API** — 400 com mensagem de validação, não 500. Ver §3.10.

### 3.7 — Registro de proposta descartada

Proposta de Thaís nesta conversa: tornar forma e miligramagem obrigatórias
a partir do momento em que o nome fosse preenchido, com validação no
método `clean`. Descartada por ela mesma. Motivos aceitos: não resolveria o
caso do cadastro totalmente em branco, e recusaria a miligramagem — dado
impresso na caixa — por falta da forma.

### 3.8 — Erro de Claude registrado

Claude citou a seção 1.2 deste documento como se fosse decisão de Thaís
para rebater a proposta acima. A seção 1.2 é conclusão de Claude, não fala
dela. A decisão que a proposta contrariava é a 1.1.

---

### 3.9 — A lista de formas

**DECIDIDO em conversa de 26/08/2026.**

A forma é escolhida de uma lista fechada:

**comprimido · cápsula · gota · ml · sachê · adesivo · supositório · pomada ·
outros**

Origem: `CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 164, onde a ideia é de
Thaís, confirmada por ela em 26/08/2026.

O argumento que sustenta o campo (`CORRECAO...` 168): *"o campo não foi
acrescentado; foi movido para onde pertencia"* — era a unidade da dose, que se
repetia em cada período de uso quando é característica da caixa e nunca muda.
É o que permite a dose ser só um número.

São **nove valores, e "não informada" não é um deles** (§3.2). Um décimo valor
só entra se o experimento da §3.10 falhar.

**A palavra a conferir:** Thaís escreveu **"outros"** em 26/08/2026;
`CORRECAO...` 164 escreve **"outra"**. Fica "outros", que é o registro mais
recente e direto dela. Detalhe de redação, não de desenho.

**"Outros" não carrega texto livre — DECIDIDO em 26/08/2026**, e vale para o
projeto inteiro, não só para a forma.

Palavras de Thaís: *"outros/outras nunca é texto livre nesse projeto, apenas
opção a ser marcada. Não tem adição pelo usuário do que seria outros/as."*

**Alcance:** a opção de escape de **toda** lista fechada do projeto é só um
rótulo a marcar. Vale para a forma (§3.9), para a unidade da concentração e
para a doença (§5.1, que já dizia isso). O usuário nunca acrescenta valor a
lista nenhuma; na doença, quem acrescenta é o administrador pelo painel (§5.3).

**Consequência visível:** quem toma um remédio numa forma fora da lista marca
"outros" e a lista dela mostra "outros". O sistema não pergunta qual é.

---

### 3.10 — Experimento a rodar antes do código

**REGISTRADO em 26/08/2026, a pedido de Thaís.**

Toda a §3.3 se apoia em **documentação lida, não em código executado**. A frase
da §3.3 diz *"Fato verificado na documentação oficial"* — e é isso mesmo que
ela diz: documentação. **Ninguém rodou nada.** Não existe projeto Django nem
banco nesta pasta.

Antes de a modelagem ser fechada, rodar um experimento pequeno contra
PostgreSQL 17 e Django 6.1, com um modelo que declare a `UniqueConstraint` da
§3.1 — conta + nome em caixa uniforme + valor + unidade + forma — com
`nulls_distinct=False`. Três perguntas, e cada uma decide uma coisa diferente:

| # | O que provar | O que a resposta decide |
|---|---|---|
| 1 | duas linhas iguais com o **valor da concentração vazio** nas duas — o banco recusa a segunda? | se `nulls_distinct` age mesmo. **Se não agir, entra a reserva 1 da §3.5** — o valor padrão "não informada" volta, e vira o décimo item da §3.9 |
| 2 | a recusa aparece na validação em Python (`full_clean` / serializer), ou só estoura no banco como `IntegrityError`? | se a API devolve **400 ou 500**. A §9, item 4, exige erro de validação que diz o que está errado. É a pergunta que nenhum documento cobria |
| 3 | campo de lista fechada sem escolha guarda `''` ou `NULL`? | confirma a condição técnica da §3.2 |

**O que este experimento fecha de uma vez:** a §3.2, a escolha entre as duas
reservas da §3.5, o teste obrigatório da §3.6, e a ressalva não resolvida da
§13.5 sobre expressões que resultam em `NULL`.

**Quem roda é Thaís**, pela restrição R3 da Fase 1 —
`FASE1_ESCOPO_PROJETO_PORTFOLIO.md` 31: *"Thaís escreve o próprio código e roda
os próprios comandos. IA explica lógica e raciocínio; não entrega código
pronto."*

**Até este experimento rodar, a §3.2 e a §3.9 são a hipótese de trabalho, não
fato verificado.**

---

## 6. COMPARTILHAMENTO — DECIDIDO — **VERSÃO VIGENTE**

**DECIDIDO em conversa de 24/08/2026.**

### 6.1 — Convite interno entre contas

Só se convida quem já tem conta. Quem convida informa o e-mail; o sistema
localiza a conta correspondente e cria o convite no estado pendente. A
pessoa convidada vê o convite dentro da própria aplicação e aceita ou
recusa.

O e-mail é identificador de conta, não canal de entrega.

O `Compartilhamento` liga conta a conta.

### 6.2 — Uma linha por par de contas

Existe no máximo um `Compartilhamento` por par (quem convida, quem é
convidado), garantido por restrição de unicidade.

Consequências, sem regra escrita a mais:

- Convite pendente não pode ser reenviado: a linha já existe.
- Convite recusado pode ser refeito: a mesma linha volta para pendente.
- Pares diferentes são independentes. Pedro→Maria e João→Maria coexistem.

Limite de insistência em convite recusado: fora do escopo.

### 6.3 — Escopo do compartilhamento

O convite carrega o que será compartilhado: só remédios, só doenças, ou os
dois. "Nada" não existe — sem nada a compartilhar não há convite.

A permissão deixa de ser filtro por dono e passa a ter duas perguntas: tem
acesso, e acesso a quê.

### 6.4 — Encerramento pelo dono

O dono encerra o compartilhamento a qualquer momento, sem aceite de
ninguém. Quem recebia volta a receber acesso negado. Encerrar é direito de
quem é dono do dado.

Isso revoga a palavra "revogação" na lista do que o projeto não faz. A
lista passa a excluir "papéis e cuidador externo". Revogação simples está
dentro.

### 6.5 — Escopo congelado após o aceite — fora do escopo por tempo

O escopo não muda enquanto o compartilhamento existe. Para mudar, o dono
encerra e convida de novo.

Mecanismo descartado, com desenho conhecido: a mudança de escopo exigiria
novo aceite de quem recebe, com escopo proposto e escopo vigente
convivendo na mesma linha. Corretamente resolvível; excluído por custo de
tempo, não por objeção de produto.

### 6.6 — Resposta neutra a e-mail não cadastrado

O sistema responde sempre a mesma coisa, exista ou não conta com aquele
endereço. Nem o nome nem a existência da conta são revelados.

Aceito como consequência: quem digita errado não descobre o erro. Quem
compartilha dado de saúde conhece a pessoa o bastante para ter o endereço
certo.

### 6.7 — Aviso por e-mail desacoplado

Ao criar o convite, o sistema solicita o envio de um aviso, através da
abstração da seção 8. Sem provedor configurado, o convite funciona igual.

**Entrega real de e-mail não vai existir neste projeto.** O destino é
console, inclusive em produção. Ninguém recebe e-mail. Vai declarado no
README.

O Telegram continua sendo a única integração externa.

### 6.8 — O que não é possível

Convidar quem não tem conta. Exigiria link de convite com token, excluído,
e entrega real de e-mail, que não vai existir.

### 6.9 — Correção de registro

"Convite com aceite" NÃO está excluído do projeto. O excluído é o **link**
de convite com token (`HANDOFF...` 196, `CORRECAO...` 298). A formulação
sem a palavra "link" em `PROMPT_FASE4...` 65 não tem fala de Thaís
sustentando e não vale.

### 6.10 — Uma conta não pode convidar a si mesma

**DECIDIDO em conversa de 25/08/2026.**

O sistema recusa o convite em que quem convida e quem é convidado são a
mesma conta. A recusa é declarada no banco, não só na validação em Python —
é a mesma classe de garantia da trava de duplicidade da seção 3.

Palavras de Thaís: _"O projeto é para uso pessoal, qual o sentido de uma
conta convidar a si mesma? O usuário se registra no sistema e adiciona seus
remédios e suas doenças para usar a api e ter essa informação para ele
mesmo e se quiser compartilhar com outra pessoa. Não vejo sentido de ele
compartilhar consigo mesmo algo que é para uso pessoal e que ele já tem
acesso de qualquer maneira."_

**Por que precisava de uma linha própria:** a restrição de unicidade da
seção 6.2 não impede isto. Ela garante uma linha por par de contas, e o par
formado pela mesma conta duas vezes é tão único quanto qualquer outro — o
banco aceitaria sem reclamar.

**A consequência que se evita:** com o convite a si mesma aceito, a conta
alcançaria os próprios dados por dois caminhos — como dona, sem restrição, e
como convidada, **com o escopo da seção 6.3**. Duas respostas possíveis para
a mesma pergunta de permissão dentro do mesmo sistema.

Isso encerra o achado 9 da auditoria. Era a única das três perguntas de
integridade que a seção 6.2 não cobria; as outras duas — mais de um convite
por par, e convite recusado refeito — ela já resolvia.

**Registro de procedência:** Thaís informa que já tinha decidido isto antes,
e a decisão não chegou a ser registrada em nenhum documento.

### 6.11 — Não há limite de quantos compartilhamentos uma conta faz

**DECIDIDO em conversa de 25/08/2026.**

Palavras de Thaís: _"Eu não vou por limites de compartilhamento, está fora
do escopo."_

**Sobre a frase "compartilhar com um ou dois familiares"**, que está em
`FASE2_3...` 17 e 47 e em `PROMPT_FASE4...` 35: **está superada.** É de
quando o projeto era pensado como uso compartilhado com familiares. O escopo
mudou depois: o projeto é de **uso pessoal**, com compartilhamento apenas de
leitura para quem o dono escolher. A frase é pensamento anterior à modelagem
real — não é regra do sistema e não descreve o projeto de hoje.

Nenhum número entra no código, e nenhuma contagem de compartilhamentos
existe.

Isso encerra o achado 12 da auditoria. Vai para a lista do que o projeto não
faz.

---

## 5. DOENÇA — DECIDIDO — **VERSÃO VIGENTE**

**DECIDIDO em conversa de 24/08/2026** (itens 5.1 e 5.2 vinham de
23/08/2026).

### 5.1 — A doença é entidade opcional e independente

Continua como decidido: sem vínculo obrigatório com remédio,
compartilhável, lista fechada com opção "outras" sem texto livre.

### 5.2 — A lista mora no banco, não no código

Existe uma tabela de doenças. A ligação entre conta e doença é
muitos-para-muitos.

Isso encerra o achado 8 da auditoria — o que perguntava se a lista seria
tabela ou constante no código.

### 5.3 — Quem acrescenta doenças à lista

Só o administrador, pelo painel administrativo do Django. O usuário comum
escolhe da lista e nunca acrescenta.

Isso não altera a decisão de que o usuário não acrescenta doenças.

### 5.4 — O painel administrativo

Usa o painel embutido do Django. Não é funcionalidade a construir.

Registrar a tabela de doenças no painel está DECIDIDO (ver 5.3).

Quais outros modelos são registrados no painel NÃO foi decidido e não é
assunto deste documento. Decide-se na implementação.

Alerta técnico de Claude, não decisão de Thaís: registrar remédio, uso,
doença de cada conta ou compartilhamento no painel daria a qualquer
administrador acesso ao dado de saúde de todas as contas. Conferir na
hora de montar o painel.

---

## 12. MODELO DE USUÁRIO — DECIDIDO

**DECIDIDO em conversa de 24/08/2026.**

### 12.1 — Modelo de usuário personalizado desde a fatia zero

O projeto define um modelo de usuário próprio, herdando de
`AbstractBaseUser` e `BaseUserManager` do Django, e configura
`AUTH_USER_MODEL` antes da primeira migração.

Motivo: trocar o modelo de usuário depois que existem dados é uma das
migrações mais destrutivas do Django. A documentação oficial recomenda
criar o personalizado no início mesmo quando ele fica idêntico ao padrão.

### 12.2 — Entrada por e-mail

`USERNAME_FIELD` é o e-mail. Não existe nome de usuário.

O e-mail é obrigatório e único: é ele que o convite usa para localizar a
outra conta.

A senha é obrigatória e guardada como hash
(`MODELAGEM_REGISTRO_MEDICACAO.md` 52 e 57, que anota Argon2, já usado no
SkillBridge).

Os campos da conta são **e-mail, senha e nome, e nada além**
(`CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 100).

Entrada por conta do Google ou GitHub (OAuth) está **fora do escopo**.
Seria uma segunda integração externa, e a vaga está ocupada pelo Telegram.
Vai para a lista do que o projeto não faz.

### 12.3 — Uma única tabela de conta

Não existe classe abstrata própria nem tabela separada de administrador.
O administrador é uma conta da mesma tabela com `is_staff` ligado, e não
usa a parte de produto do sistema.

`is_staff` não é tipo de conta: é permissão de operar o sistema por
dentro. A decisão da seção 4 — um único tipo de conta, sem marca de tipo —
continua inteira.

Registro: a arquitetura de três tabelas do SkillBridge (`Client`,
`Freelancer`, `StaffUser`) resolve um problema que não existe aqui. Lá há
dois tipos de usuário genuinamente distintos e classes abstratas, o que
deixa `AUTH_USER_MODEL` sem candidato concreto. Aqui há um tipo só.

---

## 13. NOME DO REMÉDIO — DECIDIDO

**DECIDIDO em conversa de 24/08/2026**, salvo onde outra origem está indicada.

### 13.1 — O nome é texto livre

O nome do remédio é digitado pela pessoa. Não há catálogo externo, base
oficial de medicamentos nem lista de onde escolher.

Origem: `HANDOFF_FASE4_MODELAGEM_REGISTRO_MEDICACAO.md` 84 e
`MODELAGEM_REGISTRO_MEDICACAO.md` 145.

Desambiguação necessária: `FASE2_3_DECISAO_PROJETO_PORTFOLIO.md` 51 chama o
modelo `Medicamento` de "catálogo digitado pela usuária". Ali "catálogo"
significa a tabela de remédios da própria conta, que existe e continua
existindo. O que está fora do escopo é base externa de medicamentos. As duas
afirmações não se contradizem.

### 13.2 — Correção ortográfica está fora do escopo

Origem: `MODELAGEM_REGISTRO_MEDICACAO.md` 145.

### 13.3 — Erro de digitação está fora do escopo

O sistema não tem defesa contra nome escrito errado, e não vai ter. Entra na
lista do que o projeto não faz.

### 13.4 — O nome é gravado exatamente como foi digitado

O sistema não altera a caixa do texto antes de gravar. Não há padronização
para maiúsculas, minúsculas nem primeira letra maiúscula.

### 13.5 — A comparação de duplicidade ignora a caixa

A restrição de unicidade da seção 3 é declarada sobre o nome em caixa
uniforme, e não sobre a coluna crua.

Comportamento visível: cadastra `Dipirona`; depois cadastra `dipirona`, com
o resto igual — o segundo é recusado como duplicata, e a lista continua
mostrando `Dipirona`.

Fato verificado na documentação oficial do Django 6.1 em 24/08/2026:
`nulls_distinct` é argumento nomeado da `UniqueConstraint` e não exige
`fields`; declarar expressões faz o Django criar índice único em vez de
restrição de tabela; a única incompatibilidade documentada com expressões é
`deferrable`, que nesse caso não pode ser usado; restrições com
`nulls_distinct` são ignoradas fora do PostgreSQL. Ambiente de Thaís:
PostgreSQL 17, Django 6.1.

Ressalva registrada, verificada apenas em parte: há registro fechado no
rastreador do Django sobre expressões que resultam em `NULL` combinadas com
`nulls_distinct=False` serem tratadas como distintas na validação em Python,
enquanto o banco recusa. A resolução desse registro NÃO foi verificada. A
garantia mora no banco, e o teste da seção 3.6 é o que a cobre.

### 13.6 — Registro de proposta descartada

Proposta de Claude nesta conversa: guardar uma segunda coluna, escondida,
com o nome em caixa uniforme, para a restrição ser declarada sobre coluna
comum. Descartada. Motivo: foi proposta por desconhecimento da documentação,
não por técnica; verificada a documentação, ela seria dado duplicado a manter
em sincronia sem ganho.

### 13.7 — O nome é obrigatório

**DECIDIDO em conversa de 26/08/2026.**

Sempre que a pessoa optar por salvar um remédio, o nome é obrigatório. Os
demais dados — concentração, unidade, forma, dose — continuam opcionais.
Registrar remédio continua sendo opcional (§1.1).

Palavras de Thaís: _"Não precisa ter dosagem, não precisa ter mais nada, mas
precisa ter o nome do remédio."_

**O que isto conserta:**

1. A §3.3 já descrevia a trava de duplicidade com o exemplo _"sem nada
   preenchido além do nome"_. Com o nome opcional, esse exemplo descrevia um
   caso impossível.
2. A trava é declarada sobre o nome em caixa uniforme, que é uma **expressão**.
   A §13.5 registra que expressão que resulta em `NULL` combinada com
   `nulls_distinct=False` é tratada como distinta na validação em Python
   enquanto o banco recusa, e que a resolução disso **não foi verificada**. Com
   o nome sempre preenchido, a expressão nunca dá `NULL` e a ressalva deixa de
   alcançar o projeto. Com o nome vazio, a API devolveria erro 500 onde a §9,
   item 4, exige erro de validação que diz o que está errado.
3. Sem isto, a combinação da §3.1 aceitaria **exatamente uma** linha em branco
   por conta, e a segunda receberia "você já tem esse remédio" apontando para
   uma linha sem nome.

**Custo:** nenhum. Campo de texto no Django e no DRF já nasce obrigatório; o
trabalho seria escrever o contrário.

**Não há tamanho mínimo para o nome.** Decisão de Thaís em 26/08/2026: *"não
vou pôr mínimo de caracteres obrigatório não."* Um mínimo seria regra de nível
1 pela tabela da §1.4, e não barraria `xx` nem `aaa`.

---

## 14. VISIBILIDADE DA API — DECIDIDO

**DECIDIDO em conversa de 24/08/2026.**

### 14.1 — O projeto publica documentação interativa da API

O endereço publicado do projeto abre uma página única que lista todos os
endpoints, com os campos de cada um e as respostas possíveis, e permite
enviar requisições dali mesmo.

A página é servida pelo próprio Django que já está no ar. Não é serviço
novo, não é processo permanente, e não conflita com a decisão de hospedagem
gratuita da Fase 1.

Origem: `FASE1_ESCOPO_PROJETO_PORTFOLIO.md` 65 — "API sem tela precisa ser
visível; existem soluções baratas e não são escopo novo".

### 14.2 — O README traz um roteiro de verificação

O README traz uma sequência numerada e curta: criar duas contas, obter o
token da primeira, cadastrar um remédio, trocar para o token da segunda,
pedir o mesmo remédio, **receber 404** (§17.5).

O roteiro existe para que quem avalia chegue à recusa sem precisar montar o
teste de cabeça. É esse o item 3 da seção 9 deste documento — a lista do que
faz um avaliador reconhecer trabalho de júnior competente, cujo item 3 é "o
usuário B não alcança o dado do usuário A".

### 14.3 — O Telegram não é a vitrine do projeto

O projeto se demonstra como backend. A integração com o Telegram é
acréscimo e nunca a tela pela qual o projeto é avaliado.

Origem: `PROMPT_VISIBILIDADE_E_INTEGRACAO_V2.md` 46, com fala de Thaís
respondendo se o Telegram poderia servir de vitrine do projeto.

### 14.4 — A pendência deixa de ser órfã

`HANDOFF_FASE4_MODELAGEM_REGISTRO_MEDICACAO.md` 52 e 186 registram a
visibilidade como pendência "órfã", por a solução depender do Telegram, que
estaria fora do escopo. Não há fala de Thaís sustentando essa classificação,
e a premissa dela caiu: o Telegram é a integração externa decidida, na
seção 7. A palavra "órfã" está revogada.

### 14.5 — Fora deste documento

Qual biblioteca gera o documento OpenAPI, e o que o Django REST Framework
já oferece de fábrica, são escolhas de implementação. Decide-se na hora de
instalar, não aqui.

---

## 15. PRAZO E ESTIMATIVA DE HORAS

**Escrita em 25/08/2026, no lugar da seção 11 apagada.** A seção 11 foi
removida por Thaís em 24/08/2026 por já estar corrigida em decisões
posteriores, e as duas linhas da tabela que apontavam para ela ficaram sem
destino. Esta seção assume o que a linha 10 daquela tabela cobria.

### 15.1 — O prazo é orientação contra inchaço, não muro

**DECIDIDO.** Palavras de Thaís, registradas em
`FASE2_3_DECISAO_PROJETO_PORTFOLIO.md` 123: _"não é que esse tempo seja uma
restrição... é só porque eu não quero me perder."_

O critério real de sucesso é **terminar**.

Isso **revoga** a formulação de `FASE1_ESCOPO_PROJETO_PORTFOLIO.md` 30, que
lista o teto de dois meses a três horas por dia entre as restrições _"fixas,
dadas, não negociáveis"_. A emenda é dela, e nunca tinha voltado para a
origem. `PROMPT_FASE2_CANDIDATOS_PROJETO.md` 34 repete a versão dura e
também está superado.

### 15.2 — Não existe estimativa vigente, e isso é fato, não pendência

A estimativa de 105 a 147 horas de `FASE2_3...` 119 **não vale**. Foi
construída sobre o modelo que depois foi invalidado: cinco tabelas incluindo
`Titular`, onze endpoints, e de 8 a 14 horas de integração externa que hoje
tem outro desenho.

Hoje o projeto não tem número, e nenhum documento tem.

### 15.3 — Quando a estimativa se refaz

**DECIDIDO em conversa de 25/08/2026.** Palavras de Thaís: _"Só pode ser
resolvido quando tiver todo planejamento pronto."_

Antes de a modelagem final, a lista de endpoints e a definição de pronto
existirem, não se refaz estimativa. A ausência de número até lá é
deliberada, não esquecimento.

Isso encerra o achado 11 da auditoria.

---

## 16. INTERFACE — SÓ API REST, SEM TELA

**Registrado em 25/08/2026.** A decisão é antiga; o que faltava era estar
neste documento.

### 16.1 — A decisão

O projeto não tem tela. É uma API REST, e só.

Origem: `FASE1_ESCOPO_PROJETO_PORTFOLIO.md` 56, decisão D3, tomada por
Thaís. Reafirmada por ela em 25/08/2026.

**Motivo, nas palavras dela:** _"Eu sou desenvolvedora backend e não
fullstack, e pensando no tempo limite do projeto o frontend foi excluído do
projeto pois não é meu foco."_

Motivo complementar, registrado na Fase 1: interface é o maior multiplicador
de escopo do projeto, estimado em 40 a 50% do tempo total.

**Enquadramento, e ele importa:** a ausência de tela **não é dívida
técnica** — é escopo excluído. Dívida técnica é fazer errado de propósito
para entregar rápido, e cobra juros. Uma API REST sem tela não é uma API
incompleta; é uma API.

**O que resolve o problema de o projeto ser visto:** a seção 14 —
documentação interativa publicada, mais o roteiro de verificação no README.

Isso encerra o achado 2 da auditoria.

---

## 17. O DONO DO PERÍODO DE USO — DECIDIDO

**DECIDIDO em conversa de 26/08/2026.** Fecha o achado 7 da auditoria, o
último dos doze que continuava aberto.

### 17.1 — O período de uso não ganha coluna de dono

O período de uso continua sem coluna própria de dono. Ele aponta para o
remédio, e o remédio é que carrega o carimbo da conta
(`CORRECAO_MODELAGEM...` 219). Quem é o dono do período de uso se descobre
atravessando o remédio.

**Proposta de Thaís, examinada e descartada por ela mesma:** acrescentar ao
período de uso uma coluna com o identificador do usuário, para o dado ficar
vinculado diretamente. Motivo do descarte, aceito por ela: seria guardar a
mesma informação em dois lugares, e nada no banco impediria que as duas
discordassem — seria possível salvar um período de uso com uma conta na
coluna e um remédio de outra conta ao lado. A regra de permissão passaria a
ter duas respostas para "de quem é este dado".

Isso é a aplicação direta de uma decisão que já estava tomada, em
`CORRECAO_MODELAGEM_REGISTRO_MEDICACAO.md` 87, quando a marca de tipo de
conta foi recusada: _"A marca pode mentir. Informação derivável não se
guarda."_

### 17.2 — O filtro por dono mora num ponto único do código

**Comportamento visível para quem programa:** toda consulta de um endpoint
já nasce filtrada pela conta de quem fez a requisição. Ninguém escreve o
filtro à mão em cada lugar; ele mora num ponto por onde todas passam, e cada
endpoint declara apenas **qual é o caminho até o dono** — direto, no caso do
remédio e da doença; atravessando o remédio, no caso do período de uso.

**A propriedade que faz isto valer a pena:** se alguém escrever um endpoint
novo e esquecer de declarar esse caminho, o endpoint **falha na primeira
chamada**, com mensagem dizendo o que falta. Antes, esquecer o filtro
produzia um endpoint que funcionava e vazava dado de outra conta, em
silêncio, passando nos testes escritos com uma conta só.

É a mesma lógica da trava de duplicidade da seção 3: em vez de confiar que
ninguém vai errar, faz-se o erro ser impossível de passar despercebido.

### 17.3 — A escrita é verificada à parte da leitura

O filtro acima protege **leitura** — listar, e buscar por identificador.

**Ele não protege a criação**, e isso fica registrado porque é a metade que
se esquece: nada nele impede uma conta de criar um período de uso apontando
para o remédio de outra pessoa, mandando o identificador daquele remédio. A
verificação de que o remédio pertence a quem está pedindo é escrita
separadamente, na validação da entrada.

A auditoria já dizia isto, e é a frase inteira: _"toda leitura e toda
escrita de uso precisa amarrar no dono do medicamento."_

### 17.4 — O que isto obriga na definição de pronto

Três itens, a verificar um a um quando a definição de pronto for escrita:

1. Conta sem relação nenhuma pedindo o período de uso de outra conta —
   **404**, na listagem e na busca por identificador (§17.5).
2. Conta sem relação nenhuma **criando** um período de uso apontado para o
   remédio de outra conta — recusado na validação da entrada (§17.3).
3. Um endpoint novo que não declare o caminho até o dono **não sobe**. Este
   é o item que impede a regra de se perder com o tempo.

### 17.4-A — Não existe período de uso sem remédio

**DECIDIDO em conversa de 26/08/2026.**

Todo período de uso aponta para um remédio, sempre. Não existe período de uso
solto.

**Comportamento visível:** quem nunca registrou remédio nenhum não tem como
registrar período de uso — não há para onde apontar. Quem registrou pelo menos
um remédio registra períodos de uso dele. Dose, quantas vezes ao dia, início e
fim continuam todos opcionais; o que não é opcional é dizer **de qual remédio**
o período é.

**Palavras de Thaís:** *"toda vez que for registrar período de uso tem que ter
no mínimo um remédio registrado. Não precisa ter dosagem, não precisa ter mais
nada, mas precisa ter o nome do remédio."*

**Custo: nenhum, e não precisa de `clean` nem de restrição nova.** A relação
entre remédio e período de uso é um-para-muitos (`MODELAGEM...` 36): o período
guarda uma chave estrangeira para o remédio, e chave estrangeira no Django já
nasce obrigatória — vira `NOT NULL` no banco.

**O que a chave estrangeira NÃO garante, e continua valendo o que a §17.3
já dizia:** que o remédio apontado seja **seu**. Isso é escrito à mão, na
validação da entrada. Uma restrição no banco para isso exigiria dar ao período
de uso uma coluna de dono — exatamente o que foi descartado na §17.1.

**Por que isto precisava estar escrito:** sem a ligação obrigatória, um período
de uso não teria dono nenhum, porque o dono dele se descobre atravessando o
remédio (§17.1).

### 17.5 — A resposta ao acesso negado — DECIDIDO

**DECIDIDO em conversa de 26/08/2026.** Estava ABERTO desde a decisão da §17.

**A resposta é 404 onde o Django REST Framework a produz naturalmente:** quando
o objeto não está no conjunto já filtrado pela conta de quem pede. Não se
escreve código para forçar 403 ali.

**Palavras de Thaís:** *"pode colocar o 404 quando é esperado (...) não tem
problema nenhum fazer um teste com esse 404 e aí a gente fecha esse erro. (...)
se aparecer outros erros, faz parte a gente adicionar."*

**Por que o 403 estava escrito:** vem da tabela de
`MODELAGEM_REGISTRO_MEDICACAO.md` §7, anterior a várias decisões — entre elas o
filtro em ponto único da §17.2, que é o que produz o 404.

**404 é a resposta mais forte, não a mais fraca.** 403 diz "existe e não é
seu", e revela a existência do dado. 404 não revela nada, e é a mesma escolha
que a §6.6 já tinha feito para o convite: resposta neutra, que não confirma nem
nega. As duas passam a dizer a mesma coisa.

**A tabela de respostas passa a ter três códigos, não um.** Cada linha tem um
motivo diferente:

| Situação | Resposta | Por quê |
|---|---|---|
| sem token | **401** | não se identificou |
| conta sem relação pedindo dado de outra | **404** | o dado não está no conjunto dela |
| convidado com compartilhamento **pendente** | **404** | ainda não tem acesso; o dado não entra no conjunto |
| convidado **aceito**, dentro do escopo, **lendo** | **200** | é o que o convite concede |
| convidado **aceito** tentando **escrever** | **403** | o dado está visível para ele; o que se nega é a **ação** (item 9 da lista do que o projeto não faz) |
| convidado aceito, pedindo o que está **fora do escopo** do convite (§6.3) | **404** | aquela parte não entra no conjunto dele |

**O 403 não desaparece** — ele fica onde é verdade: objeto visível, ação
proibida.

**Fica registrado como aberto por natureza, e não é pendência:** se durante a
implementação aparecerem outras respostas necessárias, elas entram. Palavras
dela: *"se aparecer outros erros, faz parte a gente adicionar."*

**O que isto obriga a corrigir, e já foi corrigido:** a §9 item 3, a §14.2 e o
passo 6 de `docs/migration-sources/FLUXO_CADASTRO_E_ISOLAMENTO_POR_CONTA.md`, que diziam 403.

---
