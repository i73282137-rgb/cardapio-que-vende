# Gera os criativos (HTML) e renderiza PNG com Chrome headless.
import subprocess, pathlib
AQUI = pathlib.Path(__file__).parent
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
FONTES = '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@800;900&family=IBM+Plex+Mono:wght@400;600;700&family=Source+Serif+4:wght@400;600&display=swap" rel="stylesheet">'
BASE = """*{box-sizing:border-box}body{margin:0;width:%dpx;height:%dpx;overflow:hidden;font-family:'Source Serif 4',Georgia,serif;-webkit-font-smoothing:antialiased}
.mono{font-family:'IBM Plex Mono',monospace}.disp{font-family:'Archivo','Arial Black',sans-serif;font-weight:900;text-transform:uppercase;letter-spacing:-.02em;line-height:.92}
.ticket{background:#FBF8F1;color:#1D1A16;font-family:'IBM Plex Mono',monospace;box-shadow:0 14px 0 rgba(0,0,0,.2)}
.ticket hr{border:0;border-top:3px dashed #1D1A16;margin:22px 0}
.ph{background:#FCEBB0;padding:0 6px}
.preco{white-space:nowrap;background:#F2C230;color:#1D1A16;font-family:'Archivo',sans-serif;font-weight:900}"""

CRIATIVOS = {
"feed-comanda": (1080, 1080, """
<div style="background:#C8372D;color:#FBF8F1;width:100%;height:100%;padding:80px;display:flex;flex-direction:column;justify-content:space-between">
 <div class="mono" style="font-size:30px;font-weight:600;letter-spacing:.12em">PARA RESTAURANTES E DELIVERIES</div>
 <div style="display:flex;gap:50px;align-items:center">
  <div class="ticket" style="width:470px;flex-shrink:0;padding:36px 34px;font-size:24px;line-height:1.65;transform:rotate(-3deg)">
   COMANDA Nº 207<hr>1x Cardápio que dá fome<br>1x Mês de posts<br>1x Resposta pro iFood<br>1x Preço calculado<br>36x Análise de foto<hr>CHATGPT GRÁTIS</div>
  <div class="disp" style="font-size:76px">207<br>prompts<br>de IA</div>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:flex-end">
  <div style="font-size:40px;line-height:1.25;max-width:640px">Mega biblioteca para restaurantes. Funciona no ChatGPT grátis.</div>
  <div class="preco" style="font-size:60px;padding:14px 28px;transform:rotate(3deg)">R$ 9,99</div>
 </div>
</div>"""),

"feed-ifood": (1080, 1080, """
<div style="background:#1D1A16;color:#FBF8F1;width:100%;height:100%;padding:80px;display:flex;flex-direction:column;justify-content:space-between">
 <div class="disp" style="font-size:78px;color:#F2C230">Cliente bravo<br>no iFood?</div>
 <div class="ticket" style="padding:40px 44px;font-size:29px;line-height:1.6;border-left:12px solid #F2C230">
  Um cliente deixou esta avaliação: <span class="ph">[cole]</span>. Escreva uma resposta pública educada, que reconheça o problema sem culpar ninguém e convide a pedir de novo.</div>
 <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:40px">
  <div style="font-size:38px;line-height:1.3">Esse é 1 dos <b>207 prompts</b> da biblioteca <b>Cardápio que Vende</b>.</div>
  <div class="preco" style="font-size:56px;padding:14px 26px;white-space:nowrap">R$ 9,99</div>
 </div>
</div>"""),

"stories-semana": (1080, 1920, """
<div style="background:#2E5E3A;color:#FBF8F1;width:100%;height:100%;padding:140px 90px 260px;display:flex;flex-direction:column;justify-content:space-between">
 <div>
  <div class="mono" style="font-size:32px;font-weight:600;letter-spacing:.12em;color:#F2C230">DONO DE RESTAURANTE</div>
  <div class="disp" style="font-size:118px;margin-top:30px">Os posts<br>da semana<br>em 20 min</div>
 </div>
 <div class="ticket" style="padding:50px;font-size:36px;line-height:1.9">
  SEG  Prato da semana<br>TER  Reels de preparo<br>QUA  Enquete<br>QUI  Carrossel<br>SEX  Promoção<br>SÁB  Bastidores<hr>207 PROMPTS PRONTOS DE IA</div>
 <div style="display:flex;justify-content:space-between;align-items:center">
  <div style="font-size:46px;line-height:1.25">Biblioteca de prompts<br><b>Cardápio que Vende</b></div>
  <div class="preco" style="font-size:72px;padding:16px 32px">R$ 9,99</div>
 </div>
</div>"""),
}

for nome, (w, h, corpo) in CRIATIVOS.items():
    html = AQUI / f"{nome}.html"
    html.write_text(f'<!doctype html><meta charset="utf-8">{FONTES}<style>{BASE % (w, h)}</style>{corpo}', encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=6000",
                    f"--window-size={w},{h + 300}", f"--screenshot={AQUI / (nome + '.png')}", html.as_uri()],
                   capture_output=True)
    from PIL import Image
    png = AQUI / (nome + '.png'); Image.open(png).crop((0, 0, w, h)).save(png)
    print(nome, (AQUI / f"{nome}.png").exists())
