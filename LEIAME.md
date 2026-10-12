# Cardápio que Vende

Mega biblioteca com 207 prompts de IA (10 capítulos, 36 com foto anexada, 18 projetos grandes) para restaurantes, lanchonetes, padarias e deliveries, feita para o ChatGPT gratuito. Preço: R$ 9,99.

Fonte única dos prompts: `biblioteca/` (`capXX_*.py` + `base.py` + `conhecimento.py`). Rode `python build.py` para gerar `biblioteca.json`, que alimenta a área do comprador (o produto em si: um site, sem PDF).

| Pasta | Conteúdo |
|---|---|
| pagina/ | `index.html`, a página de vendas (publicada em https://claude.ai/artifact/V1PEXCyVcfjHs9jdcpprL8) |
| area-do-comprador/ | `area.html`, a área interna do comprador (prévia privada em https://claude.ai/artifact/RuMyHYnHCTRjditeubGHrp). Regerar: `python gerar_area.py` |
| anuncios/ | 3 criativos PNG, `ANUNCIOS.md` (textos, público, orçamento), `gerar_criativos.py` |

Versões locais (HTML completo): `python site/gerar_site.py` gera `site/index.html` (vendas) e `site/area.html` (o produto).

## O que falta (depende do dono: conta, CPF, banco ou cartão)
1. **Checkout:** criar o produto na Kiwify (ou Hotmart) como acesso a área de membros/link externo, preço R$ 9,99 e garantia de 7 dias.
2. **Hospedar a área do comprador:** publicar `site/area.html` num endereço que só compradores recebam (ex.: Netlify, Vercel ou a área de membros da plataforma).
3. **Link na página:** colar o link do checkout em `CHECKOUT_URL` no `pagina/index.html` e republicar.
4. **Página pública:** abrir a página e usar o menu Compartilhar para liberar o link público, ou usar a página de vendas da própria Kiwify.
5. **Meta Ads:** conta de anúncios com forma de pagamento. Subir os anúncios A e B de `anuncios/ANUNCIOS.md` com R$ 20/dia cada.
