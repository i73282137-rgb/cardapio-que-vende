# Base da biblioteca: monta o texto completo de cada prompt a partir de uma ficha curta.
# Placeholders no texto: {{chave}}. Campos globais (ficha do negócio) ficam em FICHA.

PRECO = "9,99"

FICHA = [
    {"k": "nome", "rotulo": "Nome do negócio", "exemplo": "Ex.: Cantina da Rosa", "tipo": "texto"},
    {"k": "tipo", "rotulo": "Tipo de negócio", "exemplo": "Escolha ou escreva", "tipo": "opcoes",
     "opcoes": ["Restaurante", "Lanchonete", "Padaria", "Pizzaria", "Hamburgueria", "Marmitaria / delivery", "Doceria / confeitaria", "Açaí / sorveteria", "Bar / boteco", "Food truck"]},
    {"k": "cidade", "rotulo": "Cidade e bairro", "exemplo": "Ex.: Niterói, Icaraí", "tipo": "texto"},
    {"k": "publico", "rotulo": "Público principal", "exemplo": "Ex.: trabalhadores no almoço e famílias no fim de semana", "tipo": "texto"},
    {"k": "preco_medio", "rotulo": "Faixa de preço", "exemplo": "Ex.: pratos de R$ 25 a R$ 45", "tipo": "texto"},
    {"k": "diferenciais", "rotulo": "Diferenciais reais", "exemplo": "Ex.: tempero caseiro, entrega em 30 min", "tipo": "longo"},
    {"k": "tom", "rotulo": "Tom de voz", "exemplo": "Escolha ou escreva", "tipo": "opcoes",
     "opcoes": ["Próximo e bem-humorado", "Simples e direto", "Acolhedor e familiar", "Elegante e sofisticado", "Jovem e descontraído"]},
    {"k": "canais", "rotulo": "Onde você vende", "exemplo": "Ex.: balcão, WhatsApp, iFood, Instagram", "tipo": "texto"},
]

FUNCOES = {
    "escrever": ("Escrever textos", "Descrições, legendas, mensagens e anúncios"),
    "post": ("Criar posts", "Instagram, Reels, stories e carrosséis"),
    "vender": ("Vender mais", "Combos, ofertas, ticket médio e conversão"),
    "responder": ("Responder clientes", "Avaliações, reclamações e dúvidas"),
    "calcular": ("Calcular e precificar", "Preço, custo, margem, CMV e metas"),
    "planejar": ("Planejar", "Calendários, campanhas e planos de ação"),
    "imagem": ("Analisar imagens", "Prompts em que você anexa uma foto"),
    "equipe": ("Treinar equipe", "Manuais, roteiros e checklists"),
    "organizar": ("Organizar a operação", "Estoque, compras, rotinas e processos"),
    "analisar": ("Analisar e decidir", "Diagnósticos, comparações e relatórios"),
    "grande": ("Projetos grandes", "Entregas completas em várias partes"),
}

CAPITULOS = []   # preenchido por cada capXX.py: (id, nome, descricao, [prompts])

REGRAS_GERAIS = [
    "Escreva em português do Brasil, com linguagem simples, como um dono de negócio fala no balcão.",
    "Use somente as informações que eu passei. Não invente preços, ingredientes, prêmios, números, avaliações ou depoimentos.",
    "Se faltar alguma informação importante, escreva [CONFIRMAR: o que falta] no lugar, em vez de inventar.",
    "Evite exageros vazios como \"o melhor da cidade\", \"incrível\", \"imperdível\" e \"sabor inesquecível\".",
]

def _lista(itens, num=False):
    return "\n".join((f"{i}. " if num else "- ") + x for i, x in enumerate(itens, 1))

def montar(p, ficha_usada, conhecimento=()):
    partes = [f"Você vai agir como {p['papel']}. Leia tudo antes de responder e siga as instruções na ordem."]
    partes.append("## CONTEXTO DO MEU NEGÓCIO\n" + "\n".join(
        f"- {f['rotulo']}: {{{{{f['k']}}}}}" for f in FICHA if f["k"] in ficha_usada))
    partes.append("## OBJETIVO\n" + p["objetivo"])
    if conhecimento:
        partes.append("## O QUE UM ESPECIALISTA SABE (use como referência)\n" + _lista(conhecimento))
    if p["campos"]:
        partes.append("## INFORMAÇÕES PARA ESTA TAREFA\n" + "\n".join(
            f"- {c['rotulo']}: {{{{{c['k']}}}}}" for c in p["campos"]))
    if p.get("imagem"):
        partes.append("## IMAGEM ANEXADA\nAnexei a esta mensagem: " + p["imagem"] + ".\n"
                      "Antes de qualquer coisa, descreva em até 4 linhas o que você vê na imagem. "
                      "Use apenas o que está visível. Se a imagem estiver escura, cortada ou ilegível, diga o que não conseguiu ver e peça outra foto antes de continuar.")
    partes.append("## COMO FAZER (siga as etapas na ordem)\n" + _lista(p["etapas"], num=True))
    partes.append("## FORMATO DA RESPOSTA\n" + p["formato"])
    regras = REGRAS_GERAIS + p.get("regras", [])
    if p.get("grande"):
        regras.append("Esta é uma entrega grande. Se a resposta ficar longa demais, entregue em partes numeradas e pare ao fim de cada parte esperando eu escrever CONTINUAR.")
    partes.append("## REGRAS\n" + _lista(regras))
    conferir = p.get("conferir", []) + [
        "Todas as informações do meu negócio que eu passei foram usadas corretamente.",
        "Nada foi inventado. O que faltou está marcado com [CONFIRMAR].",
    ]
    partes.append("## ANTES DE ENTREGAR, CONFIRA\n" + _lista(conferir))
    partes.append("No final, pergunte se eu quero ajustar o tom, o tamanho ou alguma informação, e sugira 1 próximo passo prático.")
    return "\n\n".join(partes)

def campo(spec):
    """'chave|Rótulo|Exemplo'  · sufixo * na chave = texto longo · exemplo 'a;b;c' com chave iniciada por ? = opções"""
    k, rot, ex = (spec.split("|") + ["", ""])[:3]
    if k.startswith("?"):
        return {"k": k[1:], "rotulo": rot, "exemplo": "Escolha ou escreva", "tipo": "opcoes", "opcoes": ex.split(";")}
    if k.endswith("*"):
        return {"k": k[:-1], "rotulo": rot, "exemplo": ex, "tipo": "longo"}
    return {"k": k, "rotulo": rot, "exemplo": ex, "tipo": "texto"}

def P(titulo, funcoes, papel, objetivo, campos, etapas, formato, regras=(), conferir=(), imagem=None,
      ficha=("nome", "tipo", "cidade", "publico", "preco_medio", "diferenciais", "tom", "canais"), grande=False, resumo=None):
    return dict(titulo=titulo, funcoes=list(dict.fromkeys(list(funcoes) + (["imagem"] if imagem else []) + (["grande"] if grande else []))),
                papel=papel, objetivo=objetivo, campos=[campo(c) for c in campos], etapas=list(etapas),
                formato=formato, regras=list(regras), conferir=list(conferir), imagem=imagem,
                ficha=list(ficha), grande=grande, resumo=resumo or objetivo.split(". ")[0].rstrip(".") + ".")
