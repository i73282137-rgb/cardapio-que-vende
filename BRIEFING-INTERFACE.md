# Briefing — Área do Comprador v2 (Cardápio que Vende)

Você é dono SÓ da pasta `C:\MAESTRO\produto-cardapio-que-vende\area-do-comprador\`.
NÃO edite `biblioteca/` (é do Claude Code, que está escrevendo os prompts agora).

## Fonte de dados
`C:\MAESTRO\produto-cardapio-que-vende\biblioteca\biblioteca.json`. Ele cresce enquanto você trabalha: hoje tem 23 prompts e chegará a 207.
Rode `python build.py` dentro de `biblioteca/` sempre que quiser a versão mais nova.
Estrutura:
- `ficha[]`: 8 campos globais do negócio `{k, rotulo, exemplo, tipo: texto|longo|opcoes, opcoes?}`
- `funcoes[]`: `{id, nome, descricao}` (11 funções: escrever, post, vender, responder, calcular, planejar, imagem, equipe, organizar, analisar, grande)
- `capitulos[]`: `{id, nome, descricao, total}`
- `prompts[]`: `{n, id, titulo, capitulo, funcoes[], resumo, imagem: bool, imagem_dica, campos[] (mesmo formato da ficha), usa_ficha[] (chaves da ficha usadas), texto}`
- No `texto`, os campos aparecem como `{{chave}}`. Nada de [colchetes].

`gerar_area.py` deve embutir o JSON no HTML, como já faz hoje com o conteudo.py. Reescreva-o para ler o biblioteca.json.

## O público
Donos de restaurante, lanchonete ou delivery. Pouca intimidade com tecnologia, uso pelo celular, ChatGPT GRATUITO.
Tudo precisa ser óbvio sem explicação.

## Requisitos (em ordem de prioridade)
1. **Preencher campos (o principal, hoje está ruim).**
   - Abrir um prompt mostra um painel de preenchimento: formulário de um lado e prévia ao vivo do prompt final do outro. No celular, fica empilhado e o botão de copiar fica fixo embaixo.
   - Campos com rótulo claro, exemplo como placeholder, `textarea` para `longo` e escolha rápida para `opcoes` (chips ou select), sempre com a opção "Outro: escrever".
   - Contador "3 de 5 campos preenchidos" e destaque na prévia: campos preenchidos em verde e vazios em amarelo, com o nome do campo.
   - Os campos da ficha do negócio aparecem num bloco recolhido "Dados do seu negócio (ficha)", já preenchidos, com um link para editar a ficha.
   - "Copiar prompt pronto" copia o texto com os valores. Se faltar campo, avisa na própria página (sem alert/confirm) e oferece "copiar mesmo assim".
   - Valores de campos específicos com a mesma chave são reaproveitados entre prompts. Tudo persiste em localStorage, sempre com try/catch.
2. **Ficha do negócio:** tela "Comece aqui" com os 8 campos e o progresso da ficha. Preenchida uma vez, serve para todos os prompts.
3. **Busca por função:** chips das 11 funções, filtro por capítulo, filtro "Com imagem" e busca por texto, todos combináveis. Mostrar a contagem de resultados.
4. **"O que você quer fazer?":** campo em linguagem natural (ex.: "responder cliente bravo", "post para sexta") que sugere os prompts mais úteis, por palavras-chave e sinônimos sobre titulo, resumo e funções. Incluir também botões de objetivos prontos.
5. **Prompts com imagem:** selo visível "Anexe uma foto" e, no painel, o passo a passo para o ChatGPT gratuito: "toque no + ou no clipe, anexe {imagem_dica}, cole o prompt e envie".
6. **Exportar:**
   - Selecionar prompts (por card, "selecionar todos do filtro", por capítulo) e gerar um arquivo `.txt` organizado para o ChatGPT ler de uma vez.
   - O arquivo tem: instrução inicial para o ChatGPT ("esta é minha biblioteca; quando eu pedir, use o prompt Nº X com os dados da minha ficha"), ficha preenchida, índice e os prompts. Opção "com meus dados preenchidos" ou "modelos em branco".
   - Exportação extra "Navegador da biblioteca": um índice compacto (Nº, título, resumo, funções, se precisa de imagem) com instrução para o ChatGPT recomendar qual prompt usar para o objetivo do usuário. É o arquivo leve, ideal para o plano gratuito.
   - Mostrar o tamanho em caracteres e avisar quando passar de cerca de 60 mil caracteres, sugerindo exportar por capítulo.
   - Download por Blob funciona em hospedagem normal, mas o preview do Artifact bloqueia downloads. Carregue a skill `artifact-capabilities` e use a capacidade de entregar arquivo ao usuário, se existir. Senão, mostre o texto num textarea com "Copiar tudo".
7. **Extras:** favoritos, "já usei" com progresso e lista paginada ou carregada aos poucos (207 cards com texto grande).

## Visual
Manter a identidade "comanda": Archivo (display), IBM Plex Mono (prompts e rótulos) e Source Serif 4 (texto), paleta tomate #C8372D, manjericão #2E5E3A, mostarda #F2C230, papel #FBF8F1 e tinta #1D1A16, com tokens light e dark como no `modelo.html` atual.
Antes de escrever, carregue a skill `artifact-design` (contrato de Artifact: título, tokens, sem `alert`, gutter de 16px, funcionar em 400px).

## Publicar
Publique no mesmo artifact: `url` = https://claude.ai/artifact/RuMyHYnHCTRjditeubGHrp (faça `action: read` antes). Verifique com um screenshot desktop e outro celular (Chrome headless em `C:/Program Files/Google/Chrome/Application/chrome.exe`).
Quando terminar, rode: `maestri ask "Claude Code" "<resumo do que fez + o que testou + o que não deu>"`.
Se faltar algo nos dados, peça pelo mesmo comando, sem editar `biblioteca/`.
