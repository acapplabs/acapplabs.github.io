# Builds the Wayfile, legal, licenses and support pages.
# Usage: python -I tools/build_pages.py <this repo> <app repo>/tasarim
# Legal texts come from the app repo (tasarim/*.md), the library list from its assets.
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])

HEAD = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#08104a">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/studio-logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="arr" viewBox="0 0 12 12"><path d="M3 9 9 3M4 3h5v5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
</svg>

<div class="infobar">
  <div class="wrap">
    <span><span class="dot"></span>Wayfile is coming soon to Google Play · <a href="/wayfile/">Learn more</a></span>
    <ul><li><a href="/support/">Support</a></li><li><a href="/wayfile/privacy/">Privacy</a></li></ul>
  </div>
</div>

<header class="nav">
  <div class="wrap">
    <a class="brand" href="/"><img src="/assets/studio-logo.svg" alt="" width="34" height="34">AC App Labs</a>
    <ul class="menu" id="menu">
      <li><a href="/">Home</a></li>
      <li>
        <button aria-expanded="false" aria-controls="mega">Apps <svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg></button>
        <div class="mega" id="mega">
          <a href="/wayfile/"><img src="/assets/wayfile.png" alt=""><span><b>Wayfile</b><small>File manager for Android</small></span><span class="tag">Soon</span></a>
          <a href="/#apps"><span class="slot" aria-hidden="true">+</span><span><b>Next project</b><small>Desktop app, in planning</small></span><span class="tag">Planning</span></a>
        </div>
      </li>
      <li><a href="/#process">How we work</a></li>
      <li><a href="/#studio">Studio</a></li>
      <li><a href="/support/"{support_current}>Support <span class="badge-new">FAQ</span></a></li>
    </ul>
    <a class="btn btn-blue" href="/#contact">Get in touch</a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>

<section class="page-hero">
  <div class="wrap">
{hero}
  </div>
</section>

<main{main_cls}>
{body}
</main>

<footer>
  <div class="wrap fgrid">
    <div>
      <a class="brand" href="/"><img src="/assets/studio-logo.svg" alt="" width="34" height="34">AC App Labs</a>
      <p>An independent software studio building clear, privacy-friendly apps for phones and computers.</p>
    </div>
{columns}
  </div>
  <div class="wrap fbottom">© <span id="y">2026</span> AC App Labs. All rights reserved.</div>
</footer>

<script src="/assets/site.js"></script>
</body>
</html>
"""

COLUMNS = [
    ("Apps", [("/wayfile/", "Wayfile"), ("/#apps", "Next project")]),
    ("Studio", [("/#process", "How we work"), ("/#studio", "Our promise"), ("/support/", "Support")]),
    ("Legal", [("/wayfile/privacy/", "Privacy policy"), ("/wayfile/terms/", "Terms of use"), ("/wayfile/licenses/", "Licenses")]),
]


def footer(current):
    out, here = [], ' aria-current="page"'
    for title, links in COLUMNS:
        items = "".join(
            f'<li><a href="{href}"{here if href == current else ""}>{label}</a></li>'
            for href, label in links)
        out.append(f"    <div><h4>{title}</h4><ul>{items}</ul></div>")
    return "\n".join(out)


def page(path, title, desc, hero, body, lang="en", doc=True):
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = HEAD.format(lang=lang, title=title, desc=desc, hero=hero.rstrip(), body=body.strip("\n"),
                       main_cls=' class="doc"' if doc else "", columns=footer(path),
                       support_current=' aria-current="page"' if path == "/support/" else "")
    out.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", out)


def icon(paths):
    return f'<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{paths}</svg></span>'


FEATURES = [
    ('<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
     "Browse and organize", "Every file and folder, with tags, a file basket and a recycle bin you can restore from."),
    ('<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
     "Find inside documents", "Search the text of PDF, Word and Excel files, right on the phone."),
    ('<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
     "Free up space", "Find large files, duplicates and app caches, and see what fills your phone."),
    ('<rect x="2" y="4" width="15" height="11" rx="2"/><path d="M6 19h7M9.5 15v4"/><rect x="16" y="9" width="6" height="11" rx="1.5"/>',
     "Computer over Wi-Fi", "Send files to any browser on your computer, protected by a one-time PIN."),
    ('<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/>',
     "NAS and shared folders", "Browse your NAS or a shared PC folder, back up your phone and keep folders in sync."),
    ('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M11 11h2M11 14h2M11 17h2"/>',
     "Archives and contact cards", "Open and extract ZIP files, and add people from .vcf contact cards to your contacts."),
]

page("/wayfile/", "Wayfile – File manager for Android",
     "Wayfile is a file manager for Android: browse and organize files, free up space, and send files to your computer or NAS over Wi-Fi. Your files stay on your device.",
     """    <img class="app-icon" src="/assets/wayfile.png" alt="" width="88" height="88">
    <h1>Wayfile</h1>
    <p class="lead">A tidy, private file manager for Android, with Wi-Fi transfer to your computer and NAS.</p>
    <span class="status">Coming soon to Google Play</span>""",
     f"""
<section class="block">
  <div class="wrap">
    <div class="head-center"><p class="kicker">What it does</p><h2>Everything your files need,<br>in one clear app</h2></div>
    <div class="features">
{chr(10).join(f'      <article class="feature">{icon(p)}<h3>{t}</h3><p>{d}</p></article>' for p, t, d in FEATURES)}
    </div>
  </div>
</section>

<section class="block soft">
  <div class="wrap split">
    <div class="collage">
      <div class="pc"><img src="/assets/wayfile-pc.jpg" alt="Wayfile's transfer page in a computer's browser" width="960" height="600"></div>
      <div class="ph"><img src="/assets/wayfile-home.jpg" alt="Wayfile home screen on a phone" width="540" height="1200"></div>
    </div>
    <div>
      <p class="kicker">Private by design</p>
      <h2>Your files stay on your phone</h2>
      <ul class="ticks">
        <li>No account or sign-up.</li>
        <li>Transfers go straight to your own computer or NAS on your local network.</li>
        <li>Every computer connection is approved on the phone, with a PIN that works once.</li>
        <li>Wayfile never reads your contacts; it only hands a contact card to your phone's Contacts app when you ask.</li>
      </ul>
      <a class="btn btn-blue" href="/wayfile/privacy/">Read the privacy policy <svg class="arrow"><use href="#arr"/></svg></a>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="head-center"><p class="kicker">Details</p><h2>Good to know</h2></div>
    <div class="facts-row">
      <div><strong>Android 8.0 or newer</strong><span>Phones and tablets.</span></div>
      <div><strong>14 languages</strong><span>Including right-to-left Arabic.</span></div>
      <div><strong>Free with small ads</strong><span>A one-time Pro purchase removes them.</span></div>
    </div>
    <div class="doc-links" style="justify-content:center">
      <a class="btn btn-line" href="/wayfile/terms/">Terms of use</a>
      <a class="btn btn-line" href="/wayfile/licenses/">Open-source licenses</a>
      <a class="btn btn-line" href="/support/">Support</a>
    </div>
  </div>
</section>
""", doc=False)

page("/support/", "Support – AC App Labs",
     "Help and contact for AC App Labs apps, including Wayfile.",
     """    <p class="eyebrow">AC App Labs</p>
    <h1>Support</h1>
    <p class="lead">Answers to common questions, and how to reach us.</p>""",
     """
  <h2>Wayfile: common questions</h2>
  <details class="faq" open><summary>How do I send files to my computer?</summary>
  <p>Connect the phone and the computer to the same Wi-Fi. In Wayfile, open <em>PC transfer</em>, type the address it shows into the computer's browser and enter the PIN. Nothing needs to be installed on the computer.</p></details>
  <details class="faq"><summary>Does Wayfile upload my files anywhere?</summary>
  <p>No. Files only move when you send them, and only to your own computer or NAS on your local network.</p></details>
  <details class="faq"><summary>Not sure what a feature does?</summary>
  <p>Tap the ⓘ button on a home screen tile to see what it does and how to use it.</p></details>

  <h2>Contact</h2>
  <div class="notice">
    <p>Our support email address is coming soon. It will be listed here and on the Google Play page.</p>
  </div>
""")

import html as H, re

def inline(t):
    t = H.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"(https://[^\s<]+)", r'<a href="\1">\1</a>', t)
    return t

def md(src):
    lines = src.split("\n---\n")[1].strip().split("\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip(): i += 1; continue
        if l.startswith("## "):
            out.append(f"  <h2>{inline(l[3:])}</h2>"); i += 1
        elif l.startswith("- "):
            out.append('  <ul class="ticks">')
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"    <li>{inline(lines[i][2:])}</li>"); i += 1
            out.append("  </ul>")
        elif l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
            out.append('  <div class="table-wrap"><table>')
            out.append("    <tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>")
            for r in rows[2:]:
                out.append("    <tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("  </table></div>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("## ", "- ", "|")):
                para.append(inline(lines[i])); i += 1
            out.append("  <p>" + "<br>\n  ".join(para) + "</p>")
    return "\n".join(out)

TASARIM = pathlib.Path(sys.argv[2])
DATE_EN, DATE_TR = "28 October 2026", "28 Ekim 2026"
en = (TASARIM / "GIZLILIK_POLITIKASI_EN.md").read_text(encoding="utf-8").replace("[publication date]", DATE_EN)
tr = (TASARIM / "GIZLILIK_POLITIKASI_TASLAK.md").read_text(encoding="utf-8").split("\n## Kullanıcının metninde")[0].replace("[yayın tarihi]", DATE_TR)
en_body = md(en).replace("<p><strong>PRIVACY POLICY</strong><br>\n  ", "<p class=\"meta\">", 1)
tr_body = md(tr + "\n---\n").replace("<p><strong>GİZLİLİK POLİTİKASI</strong><br>\n  ", "<p class=\"meta\">", 1)
en_note = en.split("\n---\n")[2].strip()
page("/wayfile/privacy/", "Wayfile – Privacy policy",
     "Privacy policy for Wayfile, the file manager for Android by AC App Labs.",
     """  <p class="eyebrow">Wayfile</p>
  <h1>Privacy policy</h1>
  <p class="lead"><a class="lang-link" href="/wayfile/privacy/tr/" hreflang="tr" lang="tr">Türkçe</a></p>""",
     en_body + f'\n  <p class="meta">{inline(en_note)}</p>')
page("/wayfile/privacy/tr/", "Wayfile – Gizlilik politikası",
     "AC App Labs tarafından geliştirilen Android dosya yöneticisi Wayfile'ın gizlilik politikası.",
     """  <p class="eyebrow">Wayfile</p>
  <h1>Gizlilik politikası</h1>
  <p class="lead"><a class="lang-link" href="/wayfile/privacy/" hreflang="en" lang="en">English</a></p>""",
     tr_body + '\n  <p class="meta">Bu Türkçe metin kolaylık için sunulan bir çeviridir; İngilizce metinle farklılık olursa <a href="/wayfile/privacy/">İngilizce metin</a> geçerlidir.</p>',
     lang="tr")


ten = (TASARIM / "KULLANIM_KOSULLARI_EN.md").read_text(encoding="utf-8").replace("[publication date]", DATE_EN)
ttr = (TASARIM / "KULLANIM_KOSULLARI_TASLAK.md").read_text(encoding="utf-8").replace("[yayın tarihi]", DATE_TR)
page("/wayfile/terms/", "Wayfile – Terms of use",
     "Terms of use for Wayfile, the file manager for Android by AC App Labs.",
     """  <p class="eyebrow">Wayfile</p>
  <h1>Terms of use</h1>
  <p class="lead"><a class="lang-link" href="/wayfile/terms/tr/" hreflang="tr" lang="tr">Türkçe</a></p>""",
     md(ten).replace("<p><strong>TERMS OF USE</strong><br>\n  ", "<p class=\"meta\">", 1)
     + f'\n  <p class="meta">{inline(ten.split(chr(10) + "---" + chr(10))[2].strip())}</p>')
page("/wayfile/terms/tr/", "Wayfile – Kullanım koşulları",
     "AC App Labs tarafından geliştirilen Android dosya yöneticisi Wayfile'ın kullanım koşulları.",
     """  <p class="eyebrow">Wayfile</p>
  <h1>Kullanım koşulları</h1>
  <p class="lead"><a class="lang-link" href="/wayfile/terms/" hreflang="en" lang="en">English</a></p>""",
     md(ttr).replace("<p><strong>KULLANIM KOŞULLARI</strong><br>\n  ", "<p class=\"meta\">", 1)
     + '\n  <p class="meta">Bu Türkçe metin kolaylık için sunulan bir çeviridir; İngilizce metinle farklılık olursa <a href="/wayfile/terms/">İngilizce metin</a> geçerlidir.</p>',
     lang="tr")


import json
libs = json.loads((TASARIM.parent / "app/src/main/assets/licenses/libraries.json").read_text(encoding="utf-8"))
rows = []
for l in libs:
    lic = H.escape(l["license"])
    if l.get("licenseUrl"):
        lic = f'<a href="{H.escape(l["licenseUrl"])}">{lic}</a>'
    name = H.escape(l["id"])
    if l.get("url"):
        name = f'<a href="{H.escape(l["url"])}">{name}</a>'
    rows.append(f"    <tr><td>{name}</td><td>{H.escape(l['version'])}</td><td>{lic}</td></tr>")
notices = [l for l in libs if l.get("notice") or l.get("copyright")]
notice_html = "\n".join(
    f"  <h3>{H.escape(l['id'])}</h3>\n  <pre>{H.escape(chr(10).join(x for x in (l.get('copyright'), l.get('notice')) if x))}</pre>"
    for l in notices)
page("/wayfile/licenses/", "Wayfile – Open-source licenses",
     "Open-source libraries used in Wayfile and their licenses.",
     """  <p class="eyebrow">Wayfile</p>
  <h1>Open-source licenses</h1>
  <p class="lead">Wayfile is built with these libraries. Thanks to their authors.</p>""",
     f"""  <p>{len(libs)} libraries, generated from the app's build. The same list, with the full license texts, is in the app under Settings &gt; About &gt; Open-source licenses.</p>
  <div class="table-wrap"><table class="lib-table">
    <tr><th>Library</th><th>Version</th><th>License</th></tr>
{chr(10).join(rows)}
  </table></div>
  <h2>Notices</h2>
{notice_html}
  <h2>License texts</h2>
  <p><a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a> · <a href="https://opensource.org/license/mit">MIT License</a> · <a href="https://opensource.org/license/bsd-3-clause">BSD 3-Clause License</a></p>
""")
