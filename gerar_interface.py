import webbrowser
import os
from datetime import datetime
import markdown


def gerar_interface(resultado_markdown: str,
                     titulo: str = "Análise Econômica",
                     abrir_navegador: bool = True) -> str:
    """
    Gera um arquivo HTML estilizado a partir de um texto em Markdown.

    Parâmetros:
        resultado_markdown : texto em markdown
        titulo             : título exibido no HTML
        abrir_navegador    : abre automaticamente no navegador

    Retorna:
        Caminho absoluto do HTML gerado
    """

    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    # Converte markdown para HTML
    conteudo_html = markdown.markdown(
        resultado_markdown,
        extensions=[
            "extra",
            "tables",
            "fenced_code",
            "nl2br"
        ]
    )

    # Métricas
    palavras = len(resultado_markdown.split())
    paragrafos_count = len([
        linha for linha in resultado_markdown.split("\n")
        if linha.strip()
    ])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{titulo}</title>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet" />

  <style>

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    :root {{
      --bg:        #0f1117;
      --surface:   #181c27;
      --card:      #1e2333;
      --border:    rgba(255,255,255,0.07);
      --accent:    #3b7dd8;
      --accent2:   #5ba3f5;
      --gold:      #c9a84c;
      --text:      #e8eaf0;
      --muted:     #8a90a2;
      --heading:   #ffffff;
      --radius:    14px;
    }}

    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh;
    }}

    /* HEADER */

    .header {{
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      padding: 2rem 2.5rem 1.5rem;
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--gold);
      border: 1px solid rgba(201,168,76,0.35);
      border-radius: 99px;
      padding: 4px 12px;
      margin-bottom: 10px;
    }}

    .badge::before {{
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--gold);
    }}

    h1 {{
      font-family: 'Lora', serif;
      font-size: clamp(1.5rem, 3vw, 2.2rem);
      color: var(--heading);
      margin-bottom: 0.4rem;
    }}

    .meta {{
      font-size: 12px;
      color: var(--muted);
    }}

    /* METRICS */

    .metrics {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .metric-pill {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 16px;
      text-align: center;
    }}

    .metric-pill .val {{
      font-size: 20px;
      font-weight: 700;
      color: var(--accent2);
      display: block;
    }}

    .metric-pill .lbl {{
      font-size: 11px;
      color: var(--muted);
      margin-top: 2px;
    }}

    /* LAYOUT */

    .layout {{
      max-width: 900px;
      margin: 2.5rem auto;
      padding: 0 1.5rem 4rem;
    }}

    .analysis-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 2rem 2.5rem;
      overflow: hidden;
      position: relative;
    }}

    .analysis-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(
        90deg,
        var(--accent),
        var(--gold)
      );
    }}

    .card-label {{
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .card-label::after {{
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }}

    /* MARKDOWN STYLING */

    .analysis-body {{
      line-height: 1.9;
      font-size: 16px;
    }}

    .analysis-body p {{
      margin-bottom: 1rem;
      font-family: 'Lora', serif;
    }}

    .analysis-body h1,
    .analysis-body h2,
    .analysis-body h3 {{
      margin-top: 2rem;
      margin-bottom: 1rem;
      color: var(--accent2);
      font-family: 'DM Sans', sans-serif;
    }}

    .analysis-body h1 {{
      font-size: 2rem;
    }}

    .analysis-body h2 {{
      font-size: 1.5rem;
    }}

    .analysis-body h3 {{
      font-size: 1.2rem;
    }}

    .analysis-body ul,
    .analysis-body ol {{
      padding-left: 1.5rem;
      margin-bottom: 1rem;
    }}

    .analysis-body li {{
      margin-bottom: 0.5rem;
    }}

    .analysis-body strong {{
      color: #ffffff;
    }}

    .analysis-body blockquote {{
      border-left: 3px solid var(--accent);
      padding-left: 1rem;
      color: #cfd6e6;
      margin: 1rem 0;
      font-style: italic;
    }}

    .analysis-body code {{
      background: rgba(255,255,255,0.08);
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 14px;
    }}

    .analysis-body pre {{
      background: #11151f;
      padding: 1rem;
      border-radius: 10px;
      overflow-x: auto;
      margin-bottom: 1rem;
    }}

    .analysis-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
    }}

    .analysis-body th,
    .analysis-body td {{
      border: 1px solid var(--border);
      padding: 12px;
      text-align: left;
    }}

    .analysis-body th {{
      background: rgba(255,255,255,0.05);
    }}

    /* BOTÃO */

    .copy-btn {{
      margin-top: 2rem;
      padding: 0.65rem 1.25rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: transparent;
      color: var(--text);
      cursor: pointer;
      transition: 0.2s;
    }}

    .copy-btn:hover {{
      border-color: rgba(255,255,255,0.2);
      color: var(--accent2);
    }}

    /* FOOTER */

    .footer {{
      text-align: center;
      padding: 2rem;
      font-size: 12px;
      color: var(--muted);
      border-top: 1px solid var(--border);
    }}

  </style>
</head>

<body>

<div class="header">

  <div>
    <div class="badge">análise econômica</div>
    <h1>{titulo}</h1>
    <p class="meta">Gerado em {agora}</p>
  </div>

  <div class="metrics">

    <div class="metric-pill">
      <span class="val">{palavras}</span>
      <span class="lbl">palavras</span>
    </div>

    <div class="metric-pill">
      <span class="val">{paragrafos_count}</span>
      <span class="lbl">blocos</span>
    </div>

  </div>

</div>

<div class="layout">

  <div class="analysis-card">

    <div class="card-label">
      análise completa
    </div>

    <div class="analysis-body" id="analysis-body">
      {conteudo_html}
    </div>

    <button class="copy-btn"
            id="copy-btn"
            onclick="copiarTexto()">
      ⎘ Copiar markdown
    </button>

  </div>

</div>

<div class="footer">
  Gerado automaticamente a partir da análise econômica — {agora}
</div>

<script>

const markdownOriginal = {repr(resultado_markdown)};

function copiarTexto() {{

  navigator.clipboard.writeText(markdownOriginal)
    .then(() => {{

      const btn = document.getElementById('copy-btn');

      btn.innerHTML = '✓ Copiado!';
      btn.style.color = '#5ba3f5';

      setTimeout(() => {{
        btn.innerHTML = '⎘ Copiar markdown';
        btn.style.color = '';
      }}, 2000);

    }});

}}

</script>

</body>
</html>
"""

    caminho = os.path.abspath("analise_economica.html")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Interface gerada: {caminho}")

    if abrir_navegador:
        webbrowser.open(f"file://{caminho}")

    return caminho