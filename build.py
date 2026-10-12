# Junta os capítulos e gera biblioteca.json (fonte única para a área do comprador e a exportação).
import json, importlib, pathlib, re
from base import FICHA, FUNCOES, PRECO, montar
from conhecimento import CONHECIMENTO
AQUI = pathlib.Path(__file__).parent
caps = []
for arq in sorted(AQUI.glob("cap*.py")):
    m = importlib.import_module(arq.stem)
    caps.append(m.CAP)
prompts, n = [], 1
for cid, nome, desc, lista in caps:
    for p in lista:
        texto = montar(p, p["ficha"], CONHECIMENTO[cid])
        usados = re.findall(r"\{\{(\w+)\}\}", texto)
        ficha_k = [f["k"] for f in FICHA if f["k"] in usados]
        prompts.append({"n": n, "id": f"p{n:03d}", "titulo": p["titulo"], "capitulo": cid, "funcoes": p["funcoes"],
                        "resumo": p["resumo"], "imagem": bool(p["imagem"]), "imagem_dica": p["imagem"],
                        "campos": p["campos"], "usa_ficha": ficha_k, "texto": texto})
        n += 1
dados = {"versao": 2, "preco": PRECO, "total": len(prompts), "ficha": FICHA,
         "funcoes": [{"id": k, "nome": v[0], "descricao": v[1]} for k, v in FUNCOES.items()],
         "capitulos": [{"id": c[0], "nome": c[1], "descricao": c[2], "total": len(c[3])} for c in caps],
         "prompts": prompts}
# checagens
ids = {f["k"] for f in FICHA}
for p in prompts:
    ks = {c["k"] for c in p["campos"]}
    assert not (ks & ids), (p["titulo"], ks & ids)
    for f in p["funcoes"]: assert f in FUNCOES, (p["titulo"], f)
(AQUI / "biblioteca.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
print("prompts:", len(prompts), {c[1]: len(c[3]) for c in caps})
print("com imagem:", sum(p["imagem"] for p in prompts), "| média de caracteres:", sum(len(p["texto"]) for p in prompts)//max(1,len(prompts)))
