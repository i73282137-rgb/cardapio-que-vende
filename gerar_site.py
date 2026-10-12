# Gera versões locais (HTML completo) da página de vendas e da área do comprador.
# Uso: python site/gerar_site.py   (rode depois de gerar_area.py ou de editar pagina/index.html)
import pathlib
RAIZ = pathlib.Path(__file__).resolve().parent.parent
TOPO = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n')
for origem, destino in [("pagina/index.html", "index.html"), ("area-do-comprador/area.html", "area.html")]:
    html = (RAIZ / origem).read_text(encoding="utf-8")
    i = html.find("</style>") + len("</style>")   # título, fontes e CSS vão no <head>
    pagina = TOPO + html[:i] + "\n</head>\n<body>\n" + html[i:] + "\n</body>\n</html>\n"
    (RAIZ / "site" / destino).write_text(pagina, encoding="utf-8")
    print("ok", destino, f"{len(pagina):,} bytes")
