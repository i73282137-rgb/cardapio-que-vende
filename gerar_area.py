# Gera area.html (área do comprador v2) a partir de ../biblioteca/biblioteca.json
# Uso: python gerar_area.py          (usa o biblioteca.json atual)
#      python gerar_area.py --build  (roda antes o build.py da biblioteca)
import json, pathlib, subprocess, sys
AQUI = pathlib.Path(__file__).parent
BIB = AQUI.parent / "biblioteca"

if "--build" in sys.argv:
    subprocess.run([sys.executable, "build.py"], cwd=BIB, check=True)

dados = json.loads((BIB / "biblioteca.json").read_text(encoding="utf-8"))
for chave in ("ficha", "funcoes", "capitulos", "prompts"):
    assert chave in dados, f"biblioteca.json sem '{chave}'"
for p in dados["prompts"]:
    assert "[" not in "".join(c["k"] for c in p["campos"]), p["titulo"]

modelo = (AQUI / "modelo.html").read_text(encoding="utf-8")
assert "/*DADOS*/null" in modelo
json_seguro = json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
saida = modelo.replace("/*DADOS*/null", json_seguro)
(AQUI / "area.html").write_text(saida, encoding="utf-8")
print("ok", len(dados["prompts"]), "prompts |", len(dados["capitulos"]), "capítulos |",
      sum(p["imagem"] for p in dados["prompts"]), "com imagem |", f"{len(saida):,} bytes")
