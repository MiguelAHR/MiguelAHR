#!/usr/bin/env python3
"""
Genera los SVG del perfil (banner, terminal y radares) con estética city pop.
Solo usa la librería estándar de Python: no necesita instalar nada.

Uso:
    python scripts/generate.py

Los archivos se escriben en ./assets
"""
import math
import pathlib
import random
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# ── Paleta city pop ────────────────────────────────────────────────
PINK = "#ff71ce"
CYAN = "#01cdfe"
MINT = "#05ffa1"
PURPLE = "#b967ff"
YELLOW = "#fffb96"
NIGHT = "#0d0221"
PANEL = "#050f33"
BLUE = "#3a7bff"       # azul eléctrico (banner)
ICE = "#8ecbff"        # azul hielo (banner)

FONT_TITLE = "'Arial Black','Segoe UI Black',Impact,sans-serif"
FONT_MONO = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"

HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n'


def save(name, svg):
    (OUT / name).write_text(HEAD + svg, encoding="utf-8")
    print("✔", OUT / name)


# ═══════════════════════════════════════════════════════════════════
#  1) BANNER
# ═══════════════════════════════════════════════════════════════════
def banner():
    W, H, HZ = 1000, 340, 250          # ancho, alto, línea del horizonte
    CX = W // 2
    rnd = random.Random(117)

    # estrellas
    stars = []
    for _ in range(70):
        x, y = rnd.randint(8, W - 8), rnd.randint(6, HZ - 70)
        r = rnd.choice([0.7, 1, 1.3, 1.8])
        d = rnd.uniform(0, 4)
        stars.append(
            f'<circle class="tw" cx="{x}" cy="{y}" r="{r}" fill="#fff" '
            f'style="animation-delay:{d:.2f}s"/>'
        )

    # rascacielos (más bajos en el centro para dejar ver el sol)
    buildings, windows = [], []
    x = 0
    while x < W:
        w = rnd.randint(26, 58)
        dist = abs((x + w / 2) - CX) / CX
        h = int(rnd.randint(26, 58) + dist * 85)
        buildings.append(
            f'<rect x="{x}" y="{HZ - h}" width="{w}" height="{h}" fill="#050f33" '
            f'stroke="{CYAN}" stroke-opacity=".4" stroke-width="1"/>'
        )
        for wy in range(HZ - h + 8, HZ - 6, 11):
            for wx in range(x + 6, x + w - 6, 9):
                if rnd.random() < 0.28:
                    col = rnd.choice([CYAN, CYAN, ICE, "#ffffff", PINK])
                    blink = ' class="bk" style="animation-delay:%.2fs"' % rnd.uniform(0, 5) if rnd.random() < 0.2 else ""
                    windows.append(
                        f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="{col}" opacity=".85"{blink}/>'
                    )
        x += w + rnd.randint(0, 4)

    # sol con rayas
    stripes = "".join(
        f'<rect x="0" y="{196 + i * 13}" width="{W}" height="{2 + i * 1.7:.1f}" fill="#000"/>'
        for i in range(6)
    )

    # grilla en perspectiva
    grid = []
    for k in range(-16, 17):
        grid.append(
            f'<line x1="{CX}" y1="{HZ}" x2="{CX + k * 95}" y2="{H}" '
            f'stroke="{BLUE}" stroke-opacity=".8" stroke-width="1"/>'
        )
    for i in range(1, 9):
        y = HZ + (H - HZ) * (i / 8) ** 2
        grid.append(
            f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}" stroke="{CYAN}" '
            f'stroke-opacity=".55" stroke-width="1"/>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Banner de Miguel Angel Huamani Rojas, Ingeniería de Sistemas Computacionales, Frontend y UX">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#01030f"/>
    <stop offset=".45" stop-color="#0a1a5c"/>
    <stop offset=".8" stop-color="#1f4fd1"/>
    <stop offset="1" stop-color="#2fb4ff"/>
  </linearGradient>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#f2fdff"/>
    <stop offset=".5" stop-color="#7be4ff"/>
    <stop offset="1" stop-color="#6a7dff"/>
  </linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0a1a5c"/>
    <stop offset="1" stop-color="{NIGHT}"/>
  </linearGradient>
  <mask id="cut"><rect width="{W}" height="{H}" fill="#fff"/>{stripes}</mask>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3.2" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="blur"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<style>
  .tw {{ animation: tw 3.4s ease-in-out infinite; }}
  .bk {{ animation: bk 4.2s steps(1) infinite; }}
  .pulse {{ animation: pulse 4s ease-in-out infinite; transform-origin: {CX}px {HZ - 20}px; }}
  @keyframes tw {{ 0%,100% {{ opacity: .15 }} 50% {{ opacity: 1 }} }}
  @keyframes bk {{ 0%,100% {{ opacity: .85 }} 50% {{ opacity: .1 }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: .55 }} 50% {{ opacity: .9 }} }}
</style>

<rect width="{W}" height="{H}" fill="url(#sky)"/>
{"".join(stars)}

<circle class="pulse" cx="{CX}" cy="{HZ - 20}" r="120" fill="#3aa0ff" opacity=".6" filter="url(#blur)"/>
<g mask="url(#cut)"><circle cx="{CX}" cy="{HZ - 20}" r="95" fill="url(#sun)"/></g>

{"".join(buildings)}
{"".join(windows)}

<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
<g filter="url(#glow)">{"".join(grid)}</g>
<line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="{CYAN}" stroke-width="2" filter="url(#glow)"/>

<text x="22" y="26" font-family="{FONT_MONO}" font-size="12" fill="{ICE}" letter-spacing="2">LIMA, PERÚ · UTC-5</text>
<text x="{W - 22}" y="26" text-anchor="end" font-family="'Yu Gothic','Meiryo','Noto Sans JP',sans-serif" font-size="14" fill="{ICE}" letter-spacing="3">ミゲル ・ シティポップ</text>

<g font-family="{FONT_TITLE}" font-style="italic" font-size="38" text-anchor="middle">
  <text x="{CX + 4}" y="86" textLength="820" lengthAdjust="spacingAndGlyphs" fill="{BLUE}" opacity=".95" filter="url(#glow)">MIGUEL ANGEL HUAMANI ROJAS</text>
  <text x="{CX}" y="82" textLength="820" lengthAdjust="spacingAndGlyphs" fill="#fff" stroke="{CYAN}" stroke-width="1.2" filter="url(#glow)">MIGUEL ANGEL HUAMANI ROJAS</text>
</g>
<text x="{CX}" y="116" text-anchor="middle" font-family="{FONT_MONO}" font-size="15" fill="{CYAN}" textLength="700" lengthAdjust="spacing" filter="url(#glow)">INGENIERÍA DE SISTEMAS COMPUTACIONALES  ·  FRONTEND &amp; UX</text>
</svg>'''
    save("banner.svg", svg)


# ═══════════════════════════════════════════════════════════════════
#  2) TERMINAL whoami
# ═══════════════════════════════════════════════════════════════════
def terminal():
    W, H = 900, 400
    # (tipo, texto)  cmd = comando, out = salida
    lines = [
        ("cmd", "whoami"),
        ("out", "Miguel Angel Huamani Rojas"),
        ("cmd", "cat estudios.txt"),
        ("out", "Ingeniería de Sistemas Computacionales · 10.º ciclo · Universidad Privada del Norte"),
        ("cmd", "cat enfoque.txt"),
        ("out", "Frontend (React, Three.js) · UX/UI · Redes · Ciberseguridad básica"),
        ("cmd", "cat experiencia.txt"),
        ("out", "Practicante pre-profesional · Dicta SAS (Colombia) · 2025"),
        ("out", "UX Designer Jr · Ciclos Studio (freelance, remoto) · 2021-2022"),
        ("cmd", "echo $UBICACION"),
        ("out", "Lima, Perú"),
    ]
    y = 96
    rows, delay = [], 0.4
    for kind, text in lines:
        if kind == "cmd":
            body = (
                f'<tspan fill="{CYAN}">miguel@lima</tspan><tspan fill="{ICE}">:~$ </tspan>'
                f'<tspan fill="#9fd0ff">{escape(text)}</tspan>'
            )
            delay += 0.5
        else:
            body = f'<tspan fill="#e6f1ff">{escape(text)}</tspan>'
            delay += 0.25
        rows.append(
            f'<text class="ln" x="34" y="{y}" xml:space="preserve" style="animation-delay:{delay:.2f}s">{body}</text>'
        )
        y += 26
    delay += 0.5
    rows.append(
        f'<text class="ln" x="34" y="{y}" xml:space="preserve" style="animation-delay:{delay:.2f}s">'
        f'<tspan fill="{CYAN}">miguel@lima</tspan><tspan fill="{ICE}">:~$ </tspan>'
        f'<tspan class="cur" fill="{CYAN}">█</tspan></text>'
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal con presentación de Miguel Angel Huamani Rojas">
<defs>
  <linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0a1a5c"/><stop offset="1" stop-color="#1f4fd1"/>
  </linearGradient>
  <filter id="glow" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity=".22"/>
  </pattern>
</defs>
<style>
  text {{ font-family: {FONT_MONO}; font-size: 15px; }}
  .ln {{ animation: show .01s backwards; }}
  .cur {{ animation: cur 1s steps(1) infinite; }}
  @keyframes show {{ from {{ opacity: 0 }} }}
  @keyframes cur {{ 50% {{ opacity: 0 }} }}
</style>
<rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="14" fill="{PANEL}" stroke="{BLUE}" stroke-width="2"/>
<path d="M3 17a14 14 0 0 1 14-14h{W - 34}a14 14 0 0 1 14 14v28H3z" fill="url(#bar)"/>
<circle cx="30" cy="24" r="6" fill="{BLUE}"/>
<circle cx="52" cy="24" r="6" fill="{CYAN}"/>
<circle cx="74" cy="24" r="6" fill="{ICE}"/>
<text x="{W / 2}" y="29" text-anchor="middle" fill="{CYAN}" style="font-size:13px;letter-spacing:2px">miguel@lima: ~</text>
<g filter="url(#glow)">{"".join(rows)}</g>
<rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="14" fill="url(#scan)" pointer-events="none"/>
</svg>'''
    save("whoami.svg", svg)


# ═══════════════════════════════════════════════════════════════════
#  3) RADARES
# ═══════════════════════════════════════════════════════════════════
# ⚠ VALORES DE EJEMPLO (autoevaluación 0-10). AJÚSTALOS TÚ: no son datos verificados.
SKILLS = [
    ("Frontend", 7),
    ("UX / UI", 7),
    ("Backend", 5),
    ("Bases de datos", 6),
    ("Redes", 5),
    ("Seguridad", 3),
    ("Datos / BI", 5),
    ("Scrum", 5),
]
LANGS = [
    ("Java", 7),
    ("C#", 5),
    ("JavaScript", 7),
    ("TypeScript", 5),
    ("Python", 6),
    ("PHP", 5),
    ("HTML / CSS", 8),
]


def radar(filename, title, subtitle, axes):
    W, H, CX, CY, R = 600, 520, 300, 275, 150
    n = len(axes)

    def pt(i, v, extra=0.0):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        r = R * v / 10 + extra
        return CX + r * math.cos(ang), CY + r * math.sin(ang), math.cos(ang)

    rings = []
    for lvl in (2, 4, 6, 8, 10):
        pts = " ".join(f"{pt(i, lvl)[0]:.1f},{pt(i, lvl)[1]:.1f}" for i in range(n))
        rings.append(
            f'<polygon points="{pts}" fill="none" stroke="{BLUE}" '
            f'stroke-opacity="{.25 + lvl * .04:.2f}" stroke-width="1"/>'
        )
    spokes = "".join(
        f'<line x1="{CX}" y1="{CY}" x2="{pt(i, 10)[0]:.1f}" y2="{pt(i, 10)[1]:.1f}" '
        f'stroke="{BLUE}" stroke-opacity=".4"/>'
        for i in range(n)
    )
    poly = " ".join(f"{pt(i, v)[0]:.1f},{pt(i, v)[1]:.1f}" for i, (_, v) in enumerate(axes))
    dots = "".join(
        f'<circle cx="{pt(i, v)[0]:.1f}" cy="{pt(i, v)[1]:.1f}" r="4.5" fill="{ICE}" stroke="#fff" stroke-width="1"/>'
        for i, (_, v) in enumerate(axes)
    )
    labels = []
    for i, (name, _) in enumerate(axes):
        x, y, c = pt(i, 10, 26)
        anchor = "middle" if abs(c) < 0.25 else ("start" if c > 0 else "end")
        labels.append(
            f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="{anchor}" fill="#e6f1ff" '
            f'font-size="14" letter-spacing="1">{escape(name)}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)}">
<defs>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="3" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <linearGradient id="fill" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity=".6"/>
    <stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/>
  </linearGradient>
</defs>
<style>
  text {{ font-family: {FONT_MONO}; }}
  .shape {{ animation: breathe 4s ease-in-out infinite; }}
  @keyframes breathe {{ 0%,100% {{ opacity: .8 }} 50% {{ opacity: 1 }} }}
</style>
<rect x="3" y="3" width="{W - 6}" height="{H - 6}" rx="16" fill="{PANEL}" stroke="{BLUE}" stroke-width="2"/>
<text x="{CX}" y="42" text-anchor="middle" fill="{CYAN}" font-size="20" letter-spacing="3" filter="url(#glow)">{escape(title)}</text>
{"".join(rings)}
{spokes}
<polygon class="shape" points="{poly}" fill="url(#fill)" stroke="{CYAN}" stroke-width="2.5" stroke-linejoin="round" filter="url(#glow)"/>
{dots}
{"".join(labels)}
<text x="{CX}" y="{H - 22}" text-anchor="middle" fill="{CYAN}" font-size="12" letter-spacing="2" opacity=".85">{escape(subtitle)}</text>
</svg>'''
    save(filename, svg)


if __name__ == "__main__":
    banner()
    terminal()
    radar("radar-skills.svg", "ÁREAS DE ENFOQUE", "autoevaluación · escala 0-10", SKILLS)
    radar("radar-langs.svg", "LENGUAJES", "autoevaluación · escala 0-10", LANGS)
