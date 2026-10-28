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
<meta name="theme-color" content="#4f5bea">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/studio-logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>

<header class="topbar" id="top">
  <nav class="nav">
    <a class="brand" href="/"><img class="brand-mark" src="/assets/studio-logo-white.svg" alt="" width="34" height="34">AC App Labs<span>.</span></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="menu">
      <span></span><span></span><span></span>
    </button>
    <ul class="menu" id="menu">
      <li><a href="/">Home</a></li>
      <li><a href="/#apps">Apps</a></li>
      <li><a href="/#about">About</a></li>
      <li><a href="/support/">Support</a></li>
      <li><a class="btn btn-outline" href="/wayfile/">Get Wayfile</a></li>
    </ul>
  </nav>
</header>

<section class="page-hero">
{hero}
  <svg class="wave" viewBox="0 0 1440 140" preserveAspectRatio="none" aria-hidden="true">
    <path class="wave-back" d="M0,70 C260,10 520,120 820,70 C1080,28 1260,40 1440,80 L1440,140 L0,140 Z"/>
    <path class="wave-front" d="M0,96 C240,140 500,40 760,74 C1020,108 1220,128 1440,84 L1440,140 L0,140 Z"/>
  </svg>
</section>

<main class="doc">
{body}
</main>

<footer class="footer">
  <div class="footer-inner">
    <a class="brand brand-dark" href="/"><img class="brand-mark" src="/assets/studio-logo.svg" alt="" width="30" height="30">AC App Labs<span>.</span></a>
    <ul class="footer-links">
{links}
    </ul>
    <p class="copy">© <span id="y">2026</span> AC App Labs</p>
  </div>
</footer>

<script src="/assets/site.js"></script>
</body>
</html>
"""

LINKS = [("/wayfile/", "Wayfile"), ("/wayfile/privacy/", "Privacy"), ("/wayfile/terms/", "Terms"), ("/wayfile/licenses/", "Licenses"), ("/support/", "Support")]


def footer(current):
    rows = []
    for href, label in LINKS:
        cls = ' class="current" aria-current="page"' if href == current else ""
        rows.append(f'      <li><a href="{href}"{cls}>{label}</a></li>')
    return "\n".join(rows)


def page(path, title, desc, hero, body, lang="en"):
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = HEAD.format(lang=lang, title=title, desc=desc, hero=hero.rstrip(), body=body.strip("\n"), links=footer(path))
    out.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", out)


page("/wayfile/", "Wayfile – File manager for Android",
     "Wayfile is a file manager for Android: browse and organize files, free up space, and send files to your computer or NAS over Wi-Fi. Your files stay on your device.",
     """  <img class="app-icon" src="/assets/wayfile.png" alt="" width="88" height="88">
  <h1>Wayfile</h1>
  <p class="lead">A tidy, private file manager for Android, with Wi-Fi transfer to your computer and NAS.</p>""",
     """
  <div class="shots">
    <img src="/assets/wayfile-pc.jpg" alt="Wayfile's transfer page in a computer's browser" width="960" height="600">
    <img src="/assets/wayfile-home.jpg" alt="Wayfile home screen on a phone" width="540" height="1200">
  </div>

  <h2>What it does</h2>
  <ul class="ticks">
    <li>Browse, search and organize every file, with tags, a file basket and a trash you can restore from.</li>
    <li>Free up space: find large files, duplicates and app caches.</li>
    <li>Send files to your computer over Wi-Fi from any browser, protected by a one-time PIN.</li>
    <li>Use your NAS or a shared PC folder: browse, back up your phone, and keep folders in sync.</li>
    <li>Open and extract ZIP files, and add people from contact cards (.vcf) to your contacts.</li>
  </ul>

  <h2>Private by design</h2>
  <ul class="ticks">
    <li>No account or sign-up.</li>
    <li>Your files stay on your phone. Transfers go straight to your own computer or NAS on your local network.</li>
    <li>Wayfile never reads your contacts; it only hands a contact card to your phone's Contacts app when you ask.</li>
  </ul>

  <h2>Details</h2>
  <ul class="ticks">
    <li>Android 8.0 or newer, phones and tablets.</li>
    <li>14 languages, including right-to-left Arabic.</li>
    <li>Free with small ads; a one-time Pro purchase removes them.</li>
  </ul>
  <p><span class="badge">Coming soon to Google Play</span></p>

  <div class="doc-links">
    <a class="btn" href="/wayfile/privacy/">Privacy policy</a>
    <a class="btn" href="/wayfile/terms/">Terms of use</a>
    <a class="btn" href="/support/">Support</a>
  </div>
""")

PENDING = """  <div class="notice">
    <p><strong>This page is being prepared.</strong> The full {what} for Wayfile will be published here before the app is released on Google Play.</p>
    <p>Questions in the meantime? See <a href="/support/">Support</a>.</p>
  </div>
"""

page("/support/", "Support – AC App Labs",
     "Help and contact for AC App Labs apps, including Wayfile.",
     """  <p class="eyebrow">AC App Labs</p>
  <h1>Support</h1>
  <p class="lead">Answers to common questions, and how to reach us.</p>""",
     """
  <h2>Wayfile: common questions</h2>
  <p><strong>How do I send files to my computer?</strong><br>
  Connect the phone and the computer to the same Wi-Fi. In Wayfile, open <em>PC transfer</em>, type the address it shows into the computer's browser and enter the PIN. Nothing needs to be installed on the computer.</p>
  <p><strong>Does Wayfile upload my files anywhere?</strong><br>
  No. Files only move when you send them, and only to your own computer or NAS on your local network.</p>
  <p><strong>Not sure what a feature does?</strong><br>
  Tap the ⓘ button on a home screen tile to see what it does and how to use it.</p>

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
