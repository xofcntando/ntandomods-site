#!/usr/bin/env python3
"""Builds the Ntandomods brand kit: business cards (front/back, SVG, PNG, print PDF),
social images, Open Graph image, avatars, icons and QR codes.

Run from the repo root:   uv run --with cairosvg --with pillow --with pypdf python3 scripts/build-assets.py
Needs `qrencode` on the PATH and the Sora + Figtree fonts installed (Google Fonts, OFL licence).
Edit config/card.json (name, title, email, phone) and re-run to regenerate the cards.
"""
import base64, io, json, pathlib, re, subprocess, sys
import cairosvg
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
BRAND = PUB / "brand"
SRC = BRAND / "source"
CARDS = BRAND / "cards"
for d in (BRAND, CARDS): d.mkdir(parents=True, exist_ok=True)

cfg = json.loads((ROOT / "config" / "card.json").read_text())
NAVY, COBALT, COBALT_L, GOLD, PAPER = "#0E1330", "#2D4BFF", "#6F86FF", "#FFB400", "#F5F7FC"
SITE = cfg["website"].rstrip("/")


# ---------- helpers ----------
def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def logo_group(dark_bg=True, x=0, y=0, w=609):
    """Wordmark as an inline <g>, transparent background. dark_bg=True gives the white/periwinkle version."""
    f = PUB / ("ntandomods-logo-dark.svg" if dark_bg else "ntandomods-logo.svg")
    s = f.read_text()
    inner = re.sub(r"^<svg[^>]*>", "", s.strip()).rsplit("</svg>", 1)[0]
    inner = re.sub(r'^<rect width="609" height="130"[^>]*/>', "", inner)  # drop solid background
    return f'<g transform="translate({x},{y}) scale({w/609})">{inner}</g>'

def mark_group(x, y, size, colors=None):
    c = colors or (NAVY, COBALT, GOLD)
    k = size / 120
    return (f'<g transform="translate({x},{y}) scale({k})">'
            f'<rect x="8" y="8" width="26" height="104" rx="6" fill="{c[0]}"/>'
            f'<rect x="106" y="8" width="26" height="104" rx="6" fill="{c[0]}"/>'
            f'<path d="M40 8 H66 L100 112 H74 Z" fill="{c[1]}"/>'
            f'<rect x="41" y="90" width="20" height="22" rx="5" fill="{c[2]}"/></g>')

def qr_png(text, fg, bg, path):
    subprocess.run(["qrencode", "-t", "PNG", "-s", "16", "-m", "0", "-l", "M", f"--foreground={fg.lstrip(chr(35))}", f"--background={bg.lstrip(chr(35))}", "-o", str(path), text], check=True)

def render(svg, out_png, w=None, h=None):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out_png), output_width=w, output_height=h)

def write(path, text):
    pathlib.Path(path).write_text(text)

def jpg_cover(path, w, h):
    """Return data URI of the source image cropped to cover w x h (cropping from the right so text space stays on the left)."""
    im = Image.open(path).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    left = im.width - w
    im = im.crop((left, 0, left + w, h)) if left > 0 else im.crop((0, 0, w, h))
    b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

FONT = "font-family=\"Sora, sans-serif\""
BODY = "font-family=\"Figtree, sans-serif\""


# ---------- QR codes ----------
qr_png(SITE + "/card", NAVY, "#FFFFFF", BRAND / "qr-card.png")
qr_png(SITE + "/card", "#FFFFFF", NAVY, BRAND / "qr-card-dark.png")


# ---------- business cards (3.5 x 2 in @ 300 dpi, 0.125 in bleed) ----------
TW, TH, BL = 1050, 600, 38            # trim size and bleed in px
CW, CH = TW + 2 * BL, TH + 2 * BL     # canvas incl. bleed: 1126 x 676
holder = cfg.get("name", "").strip()
title = cfg.get("title", "").strip()

def card_front():
    bg = jpg_cover(SRC / "bg-wide.jpg", CW, CH)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}">
<image href="{bg}" x="0" y="0" width="{CW}" height="{CH}" preserveAspectRatio="xMidYMid slice"/>
<defs><linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{NAVY}" stop-opacity=".96"/><stop offset=".55" stop-color="{NAVY}" stop-opacity=".82"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></linearGradient></defs>
<rect width="{CW}" height="{CH}" fill="url(#fade)"/>
{logo_group(True, BL + 70, CH/2 - 110, 560)}
<text x="{BL + 78}" y="{CH/2 + 70}" {BODY} font-size="30" font-weight="500" fill="#B8C0F0">{cfg["tagline"]}</text>
<rect x="{BL + 78}" y="{CH/2 + 100}" width="64" height="6" rx="3" fill="{GOLD}"/>
</svg>'''

def card_back():
    qr = data_uri(BRAND / "qr-card.png", "image/png")
    left = BL + 78
    lines = []
    y = BL + 215
    if holder:
        lines.append(f'<text x="{left}" y="{y}" {FONT} font-size="54" font-weight="700" fill="{NAVY}">{holder}</text>'); y += 46
        if title:
            lines.append(f'<text x="{left}" y="{y}" {BODY} font-size="27" font-weight="500" fill="#4A5073">{title}</text>'); y += 40
        y += 22
    else:
        lines.append(f'<text x="{left}" y="{y}" {FONT} font-size="46" font-weight="700" fill="{NAVY}">Ntandomods INC</text>'); y += 44
        lines.append(f'<text x="{left}" y="{y}" {BODY} font-size="26" font-weight="500" fill="#4A5073">APIs and modifications</text>'); y += 60
    rows = []
    if cfg.get("email"): rows.append(("E", cfg["email"]))
    if cfg.get("phone"): rows.append(("T", cfg["phone"]))
    if cfg.get("whatsapp"): rows.append(("W", "WhatsApp " + cfg["whatsapp"]))
    rows.append(("W", SITE.replace("https://", "")))
    rows.append(("A", "Ladybug API  /  Ladybug Cloud"))
    icons = {"E": "@", "T": "T", "W": "W", "A": "A"}
    for key, txt in rows:
        lines.append(f'<rect x="{left}" y="{y-24}" width="32" height="32" rx="8" fill="{COBALT}"/>'
                     f'<text x="{left+16}" y="{y-1}" text-anchor="middle" {FONT} font-size="17" font-weight="700" fill="#fff">{icons[key]}</text>'
                     f'<text x="{left+48}" y="{y}" {BODY} font-size="26" font-weight="600" fill="{NAVY}">{txt}</text>')
        y += 48
    qx, qy, qs = CW - BL - 78 - 230, BL + 150, 230
    qy = CH/2 - qs/2 - 18
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}" height="{CH}">
<rect width="{CW}" height="{CH}" fill="{PAPER}"/>
<rect x="0" y="0" width="{CW}" height="{CH}" fill="none"/>
<rect x="0" y="0" width="22" height="{CH}" fill="{COBALT}"/><rect x="0" y="{CH-120}" width="22" height="120" fill="{GOLD}"/>
{mark_group(left, BL + 110, 64)}
{"".join(lines)}
<rect x="{qx-18}" y="{qy-18}" width="{qs+36}" height="{qs+36}" rx="18" fill="#fff" stroke="#DDE2F0" stroke-width="2"/>
<image href="{qr}" x="{qx}" y="{qy}" width="{qs}" height="{qs}"/>
<text x="{qx+qs/2}" y="{qy+qs+58}" text-anchor="middle" {BODY} font-size="22" font-weight="600" fill="#4A5073">Scan to save contact</text>
</svg>'''

for name, svg in (("front", card_front()), ("back", card_back())):
    write(CARDS / f"business-card-{name}.svg", svg)
    render(svg, CARDS / f"business-card-{name}.png")

# print-ready PDF: page 1 front, page 2 back, page size = trim + bleed (3.75 x 2.25 in)
pages = []
for name in ("front", "back"):
    im = Image.open(CARDS / f"business-card-{name}.png").convert("RGB")
    pages.append(im)
pages[0].save(CARDS / "business-card-print.pdf", "PDF", resolution=300.0, save_all=True, append_images=pages[1:])

# mockup sheet of both sides
sheet = Image.new("RGB", (CW * 2 + 180, CH + 120), (230, 234, 246))
sheet.paste(pages[0], (60, 60)); sheet.paste(pages[1], (CW + 120, 60))
sheet.save(CARDS / "business-card-preview.png")


# ---------- social + Open Graph images ----------
def banner(w, h, out, logo_w, tag_size, with_qr=False, scale_logo_x=None):
    bg = jpg_cover(SRC / "bg-wide.jpg", w, h)
    lx = scale_logo_x if scale_logo_x is not None else round(w * 0.06)
    ly = h / 2 - logo_w * 130 / 609 / 2 - tag_size * 0.9
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><linearGradient id="fade" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{NAVY}" stop-opacity=".9"/><stop offset=".5" stop-color="{NAVY}" stop-opacity=".6"/><stop offset=".8" stop-color="{NAVY}" stop-opacity="0"/></linearGradient></defs>
<image href="{bg}" x="0" y="0" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{w}" height="{h}" fill="url(#fade)"/>
{logo_group(True, lx, ly, logo_w)}
<text x="{lx + logo_w*0.04}" y="{ly + logo_w*130/609 + tag_size*1.9}" {BODY} font-size="{tag_size}" font-weight="500" fill="#C9D0F5">{cfg["tagline"]}</text>
<rect x="{lx + logo_w*0.04}" y="{ly + logo_w*130/609 + tag_size*2.5}" width="{tag_size*2.4}" height="{max(4, tag_size*.2)}" rx="3" fill="{GOLD}"/>
</svg>'''
    render(svg, BRAND / out)

banner(1200, 630, "og-image.png", 600, 30)
banner(1500, 500, "social-cover-x.png", 640, 30)
banner(1584, 396, "social-cover-linkedin.png", 600, 28)
banner(1640, 624, "social-cover-facebook.png", 700, 32, scale_logo_x=120)
banner(2560, 1440, "youtube-banner.png", 1000, 46, scale_logo_x=560)  # safe area is the centre 1546 x 423

# square post (1080) with the ladybug art
lad = jpg_cover(SRC / "ladybug.jpg", 1080, 1080)
post = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
<rect width="1080" height="1080" fill="{NAVY}"/>
<image href="{lad}" x="0" y="0" width="1080" height="1080"/>
{logo_group(True, 60, 60, 420)}
<text x="540" y="1000" text-anchor="middle" {FONT} font-size="46" font-weight="700" fill="#fff">Ladybug API &#183; Ladybug Cloud</text>
<text x="540" y="1046" text-anchor="middle" {BODY} font-size="26" font-weight="500" fill="#B8C0F0">{SITE.replace("https://","")}</text>
</svg>'''
render(post, BRAND / "social-post-square.png")

# avatars and icons
av = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"><rect width="512" height="512" fill="{NAVY}"/>{mark_group(112, 116, 288, ("#FFFFFF", COBALT_L, GOLD))}</svg>'
render(av, BRAND / "avatar-dark.png", 1024, 1024)
av2 = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"><rect width="512" height="512" fill="{PAPER}"/>{mark_group(112, 116, 288)}</svg>'
render(av2, BRAND / "avatar-light.png", 1024, 1024)
for size, name in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")):
    render(av, PUB / name, size, size)
Image.open(PUB / "favicon-32.png").save(PUB / "favicon.ico", sizes=[(32, 32)])

# pattern + wide wallpaper copies (web-optimised)
for src, out, w in (("pattern.jpg", "pattern.jpg", 1024), ("bg-wide.jpg", "wallpaper.jpg", 1920), ("ladybug.jpg", "ladybug-illustration.jpg", 1920)):
    Image.open(SRC / src).convert("RGB").save(BRAND / out, "JPEG", quality=86, optimize=True)

# vector copies of the logos for the brand kit
for n in ("ntandomods-logo.svg", "ntandomods-logo-dark.svg", "ntandomods-mark.svg"):
    (BRAND / n).write_bytes((PUB / n).read_bytes())

print("done:", sorted(p.name for p in BRAND.iterdir() if p.is_file()))
