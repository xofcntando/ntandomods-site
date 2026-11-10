logos=[
("Primary logo","ntandomods-logo.svg","paper","Light backgrounds","ntandomods-logo.svg","ntandomods-logo.png"),
("Reversed logo","ntandomods-logo-dark.svg","dark","Dark backgrounds","ntandomods-logo-dark.svg","ntandomods-logo-dark.png"),
("Mark","ntandomods-mark.svg","chk","Icon, favicon, avatar","ntandomods-mark.svg","ntandomods-mark.png"),
]
def logo_tile(t,svg,cls,use,a,b):
    return f'<div class="tile"><div class="pv {cls}"><img src="/brand/{svg}" alt="{t}"></div><div class="meta"><div><b>{t}</b><br><span style="color:var(--ink-2);font-size:14px">{use}</span></div><div class="dl"><a href="/brand/{a}" download>SVG</a><a href="/{b}" download>PNG</a></div></div></div>'
def img_tile(t,f,size):
    return f'<div class="tile"><div class="pv"><img src="/brand/{f}" alt="{t}" loading="lazy"></div><div class="meta"><div><b>{t}</b><br><span style="color:var(--ink-2);font-size:14px">{size}</span></div><div class="dl"><a href="/brand/{f}" download>Download</a></div></div></div>'
sw=[("Midnight","#0E1330","Text, dark backgrounds"),("Cobalt","#2D4BFF","Buttons, links, accents"),("Periwinkle","#6F86FF","Highlights on dark"),("Amber","#FFB400","Focus rings, small accents"),("Paper","#F5F7FC","Page background"),("Slate","#4A5073","Secondary text")]
swh="".join(f'<button class="sw" data-hex="{h}" type="button"><i style="background:{h}"></i><div><b>{n}</b><code>{h}</code><br><span style="color:var(--ink-2);font-size:14px">{u}</span></div></button>' for n,h,u in sw)
def sec(title,sub,body,first=False):
    pad='' if first else ' style="padding-top:0"'
    return f'<section class="bk"{pad}><div class="wrap"><h2>{title}</h2><p class="sub">{sub}</p>{body}</div></section>'
gal=lambda items:'<div class="gallery">'+"".join(items)+'</div>'
sections=[
 sec("Logos","Use the primary logo on light backgrounds and the reversed logo on dark ones. The mark works on its own where space is tight.",'<div class="logos">'+"".join(logo_tile(*t) for t in logos)+'</div>',True),
 sec("Colours","Click a swatch to copy its code.",f'<div class="swatches">{swh}</div>'),
 sec("Typography","Both fonts are free from Google Fonts.",'<div class="type"><div><p class="big" style="font-family:Sora,sans-serif;font-weight:700">Aa Sora</p><b>Headlines</b><p style="margin:6px 0 0;color:var(--ink-2)">Sora Bold, tight letter spacing (-0.02em).</p></div><div><p class="big" style="font-family:Figtree,sans-serif;font-weight:500">Aa Figtree</p><b>Body text</b><p style="margin:6px 0 0;color:var(--ink-2)">Figtree Regular, Medium and SemiBold at 17px with 1.6 line height.</p></div></div>'),
 sec("Business card",'Standard 3.5 x 2 inch card with 0.125 inch bleed, 300 dpi. Send the PDF (page 1 front, page 2 back) to any printer. The same card lives online at <a href="/card">/card</a>.',gal([
   img_tile("Card front","cards/business-card-front.png","1126 x 676 px, includes bleed"),
   img_tile("Card back","cards/business-card-back.png","1126 x 676 px, includes bleed"),
   '<div class="tile"><div class="pv"><img src="/brand/cards/business-card-preview.png" alt="Both sides of the business card" loading="lazy"></div><div class="meta"><div><b>Print-ready PDF</b><br><span style="color:var(--ink-2);font-size:14px">2 pages, front and back</span></div><div class="dl"><a href="/brand/cards/business-card-print.pdf" download>PDF</a><a href="/brand/cards/business-card-front.svg" download>Front SVG</a><a href="/brand/cards/business-card-back.svg" download>Back SVG</a></div></div></div>'])).replace('<section class="bk"','<section id="assets" class="bk"',1),
 sec("Social and sharing images","Sized for the main platforms. Open Graph is what link previews show.",gal([
   img_tile("Open Graph / link preview","og-image.png","1200 x 630 px"),
   img_tile("X / Twitter header","social-cover-x.png","1500 x 500 px"),
   img_tile("LinkedIn banner","social-cover-linkedin.png","1584 x 396 px"),
   img_tile("Facebook cover","social-cover-facebook.png","1640 x 624 px"),
   img_tile("YouTube banner","youtube-banner.png","2560 x 1440 px, keep text in the centre"),
   img_tile("Square post","social-post-square.png","1080 x 1080 px"),
   img_tile("Profile picture, dark","avatar-dark.png","1024 x 1024 px"),
   img_tile("Profile picture, light","avatar-light.png","1024 x 1024 px")])),
 sec("Artwork","Use for headers, slides and backgrounds.",gal([
   img_tile("Wallpaper","wallpaper.jpg","1920 x 1080 px, text space on the left"),
   img_tile("Ladybug illustration","ladybug-illustration.jpg","1920 x 1080 px"),
   img_tile("Pattern tile","pattern.jpg","1024 x 1024 px"),
   img_tile("Business card QR","qr-card.png","Links to /card")])),
 sec("Using the logo","A few simple rules keep the brand looking right.",'<div class="rules"><div><h3>Give it room</h3><p>Leave clear space around the logo at least equal to the width of the vertical bar in the mark.</p></div><div><h3>Keep the colours</h3><p>Do not recolour, outline, stretch or rotate it. Pick the primary or reversed version for contrast.</p></div><div><h3>Minimum size</h3><p>Wordmark: 120 px wide on screen. Mark alone: 16 px. Below that, use the mark.</p></div><div><h3>One accent at a time</h3><p>Amber is a small highlight, never a background for body text.</p></div></div>'),
]
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brand kit | Ntandomods INC</title>
<meta name="description" content="Ntandomods INC brand kit: logos, colours, fonts, social covers, business card and usage rules.">
<link rel="canonical" href="https://ntandomods.mywire.org/brand">
<meta property="og:title" content="Ntandomods INC brand kit">
<meta property="og:description" content="Logos, colours, fonts, social covers and the print-ready business card.">
<meta property="og:image" content="https://ntandomods.mywire.org/brand/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E1330">
<link rel="manifest" href="/site.webmanifest"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="Ntandomods INC home"><img src="/ntandomods-logo.svg" alt="Ntandomods INC"></a>
  <nav class="nav" aria-label="Main"><a href="/">Home</a><a href="/card">Business card</a><a class="btn solid sm" href="#assets">Downloads</a></nav>
</div></header>
<section class="bk-hero"><div class="wrap"><h1>Brand kit</h1><p>Logos, colours, fonts and ready-made images for anyone who writes about, links to or works with Ntandomods INC.</p></div></section>
<main>
'''
tail='''
</main>
<footer><div class="wrap legal" style="margin:0;border:0;padding:0;display:flex!important;justify-content:space-between;gap:16px;flex-wrap:wrap"><span>&copy; <span id="yr"></span> Ntandomods INC</span><span><a href="/">Home</a> &nbsp;&middot;&nbsp; <a href="/card">Business card</a></span></div></footer>
<script src="/brand.js"></script>
</body>
</html>
'''
open(__import__("pathlib").Path(__file__).resolve().parent.parent/"public"/"brand.html","w").write(head+"\n".join(sections)+tail)
