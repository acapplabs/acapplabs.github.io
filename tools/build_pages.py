# Builds every page of the site: home, apps, studio pages, Wayfile, support, legal and licenses.
# Usage: python -I tools/build_pages.py <this repo> <app repo>/tasarim
# Legal texts come from the app repo (tasarim/*.md), the library list from its assets.
import pathlib, sys

ROOT = pathlib.Path(sys.argv[1])
V = "5"  # bump when site.css or site.js change, so browsers drop cached copies

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
<link rel="stylesheet" href="/assets/site.css?v={v}">
</head>
<body>

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="arr" viewBox="0 0 12 12"><path d="M3 9 9 3M4 3h5v5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></symbol>
  <symbol id="left" viewBox="0 0 16 16"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="right" viewBox="0 0 16 16"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
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
{nav}
    </ul>
    <a class="btn btn-blue" href="/support/#contact">Get in touch</a>
    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>

<section class="{hero_cls}">
  <div class="galaxy" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i class="swirl"></i><b></b></div>
  <div class="wrap">
{hero}
  </div>
</section>
{subnav}
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

<script src="/assets/site.js?v={v}"></script>
</body>
</html>
"""

HERE = ' aria-current="page"'
CHEV = '<svg class="chev" viewBox="0 0 10 10" aria-hidden="true"><path d="M1 3l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'


def nav(current):
    def item(href, label, extra=""):
        cur = HERE if current == href or (href != "/" and current.startswith(href)) else ""
        return f'      <li><a href="{href}"{cur}>{label}{extra}</a></li>'
    apps_cur = HERE if current.startswith(("/apps/", "/wayfile/")) else ""
    return "\n".join([
        item("/", "Home"),
        f"""      <li>
        <button aria-expanded="false" aria-controls="mega"{apps_cur}>Apps {CHEV}</button>
        <div class="mega" id="mega">
          <a href="/wayfile/"><img src="/assets/wayfile.png" alt=""><span><b>Wayfile</b><small>File manager for Android</small></span><span class="tag">Soon</span></a>
          <a href="/apps/#game"><span class="slot" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2" y="7" width="20" height="11" rx="5.5"/><path d="M7 10.5v4M5 12.5h4"/><circle cx="16" cy="11.5" r="1"/><circle cx="18" cy="13.8" r="1"/></svg></span><span><b>PC game</b><small>Coming soon on Steam</small></span><span class="tag">In design</span></a>
          <a href="/apps/#android"><span class="slot" aria-hidden="true">+</span><span><b>New Android app</b><small>Design and testing</small></span><span class="tag">In design</span></a>
          <a href="/apps/"><span class="slot" aria-hidden="true">≡</span><span><b>All apps</b><small>Everything we make</small></span><span></span></a>
        </div>
      </li>""",
        item("/about/", "Studio"),
        item("/process/", "How we work"),
        item("/security/", "Security"),
        item("/support/", "Support", ' <span class="badge-new">FAQ</span>'),
    ])


COLUMNS = [
    ("Apps", [("/wayfile/", "Wayfile"), ("/apps/", "All apps")]),
    ("Studio", [("/about/", "About the studio"), ("/process/", "How we work"), ("/security/", "Security"), ("/support/", "Support")]),
    ("Legal", [("/wayfile/privacy/", "Privacy policy"), ("/wayfile/terms/", "Terms of use"), ("/wayfile/licenses/", "Licenses")]),
]


def footer(current):
    out = []
    for title, links in COLUMNS:
        items = "".join(f'<li><a href="{href}"{HERE if href == current else ""}>{label}</a></li>' for href, label in links)
        out.append(f"    <div><h4>{title}</h4><ul>{items}</ul></div>")
    return "\n".join(out)


WAYFILE_TABS = [("/wayfile/", "Overview"), ("/wayfile/privacy/", "Privacy policy"), ("/wayfile/terms/", "Terms of use"), ("/wayfile/licenses/", "Licenses"), ("/support/", "Help")]


def subnav(current):
    if not current.startswith("/wayfile/"):
        return ""
    base = current.replace("/tr/", "/")
    links = "".join(f'<a href="{href}"{HERE if href == base else ""}>{label}</a>' for href, label in WAYFILE_TABS)
    return f'<nav class="subnav" aria-label="Wayfile"><div class="wrap"><span class="subnav-title"><img src="/assets/wayfile.png" alt="" width="24" height="24">Wayfile</span>{links}</div></nav>\n'


def page(path, title, desc, hero, body, lang="en", doc=True, hero_cls="page-hero"):
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    html = HEAD.format(lang=lang, title=title, desc=desc, hero=hero.rstrip(), body=body.strip("\n"), v=V,
                       main_cls=' class="doc"' if doc else "", columns=footer(path), nav=nav(path), hero_cls=hero_cls, subnav=subnav(path))
    out.write_text(html, encoding="utf-8", newline="\n")
    print("wrote", out)


ICONS = {
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
    "pc": '<rect x="2" y="4" width="15" height="11" rx="2"/><path d="M6 19h7M9.5 15v4"/><rect x="16" y="9" width="6" height="11" rx="1.5"/>',
    "nas": '<rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/>',
    "file": '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M11 11h2M11 14h2M11 17h2"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8.4-7 10-4-1.6-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "lang": '<path d="M3 5h18M3 12h18M3 19h12"/><circle cx="19" cy="19" r="2"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "flask": '<path d="M9 3h6M10 3v6L5 19a2 2 0 0 0 1.8 2.9h10.4A2 2 0 0 0 19 19l-5-10V3"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "key": '<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l3 3M15 8l2 2"/>',
    "wifi": '<path d="M5 12.5a10 10 0 0 1 14 0M8 15.5a6 6 0 0 1 8 0"/><circle cx="12" cy="19" r="1"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
    "pen": '<path d="m4 20 4-1 11-11-3-3L5 16z"/><path d="m14 6 3 3"/>',
    "code": '<path d="m8 8-4 4 4 4M16 8l4 4-4 4M14 5l-4 14"/>',
    "rocket": '<path d="M5 15c-1 1-1.5 3.5-1.5 5.5 2 0 4.5-.5 5.5-1.5M9 15l-3-3c1-4 4.5-8.5 12-9-.5 7.5-5 11-9 12z"/><circle cx="15" cy="9" r="1.5"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "game": '<rect x="2" y="7" width="20" height="11" rx="5.5"/><path d="M7 10.5v4M5 12.5h4"/><circle cx="16" cy="11.5" r="1"/><circle cx="18" cy="13.8" r="1"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
}


def ico(name):
    return f'<span class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg></span>'


def cards(items, cls="cards"):
    rows = "\n".join(f'      <article class="card">{ico(i)}<h3>{t}</h3><p>{d}</p></article>' for i, t, d in items)
    return f'    <div class="{cls}">\n{rows}\n    </div>'


def more_cards(items):
    rows = []
    for i, t, short, points in items:
        lis = "".join(f"<li>{p}</li>" for p in points)
        rows.append(f'      <details class="more-card"><summary>{ico(i)}<span><b>{t}</b><small>{short}</small></span></summary>'
                    f'<div class="more-body"><ul>{lis}</ul></div></details>')
    return '    <div class="more-grid">\n' + "\n".join(rows) + "\n    </div>"


def head_center(kicker, title, sub=""):
    sub = f'<p style="max-width:40em;margin:0 auto;color:var(--muted)">{sub}</p>' if sub else ""
    return f'    <div class="head-center"><p class="kicker">{kicker}</p><h2>{title}</h2>{sub}</div>'


ARROW = '<svg class="arrow"><use href="#arr"/></svg>'

# ---------- Home ----------
page("/", "AC App Labs – Independent software studio",
     "AC App Labs is an independent software studio building clear, privacy-friendly apps for phones and computers. Our first app, Wayfile, is coming soon to Google Play.",
     f"""    <span class="pill"><b>New</b>Our first app, Wayfile, is being tested</span>
    <h1>We build <span>clear, reliable apps</span> for phones and computers</h1>
    <p>AC App Labs is an independent software studio. We design, build, translate and test every app ourselves, with privacy as the starting point.</p>
    <div class="actions">
      <a class="btn btn-blue" href="/apps/">Explore our apps</a>
      <a class="btn btn-ghost" href="/about/">About the studio {ARROW}</a>
    </div>
    <ul class="platforms" aria-label="Platforms"><li class="now">Android</li><li>Windows</li><li>macOS</li><li>Linux</li></ul>""",
     f"""
<section class="block" id="apps">
  <div class="wrap">
    <div class="head-row">
      <div><p class="kicker">Our apps</p><h2>What we are building</h2></div>
      <div class="rail-ctrl"><button data-rail="app-rail" data-dir="-1" aria-label="Previous"><svg><use href="#left"/></svg></button><button data-rail="app-rail" data-dir="1" aria-label="Next"><svg><use href="#right"/></svg></button></div>
    </div>
    <div class="rail wide" id="app-rail">
      <a class="slide" href="/wayfile/">
        <div><span class="tagline">Android · Coming soon</span><h3>Wayfile</h3><p>A tidy, private file manager. Browse and clean up your phone, and move files to your computer or NAS over Wi-Fi.</p><span class="btn btn-white">Explore Wayfile {ARROW}</span></div>
        <div class="shot"><img src="/assets/wayfile-home.jpg" alt="" width="540" height="1200"></div>
      </a>
      <a class="slide" href="/apps/#game" style="--glow: rgba(255,61,127,.55)">
        <span class="ribbon">Coming soon on Steam</span>
        <div><span class="tagline">PC game · Design and testing</span><h3>Our first game</h3><p>We are making a game for PC. It is in design and testing now, and it will come to Steam. More to show soon.</p><span class="btn btn-white">Learn more {ARROW}</span></div>
        <div class="art-tile" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS["game"]}</svg></div>
      </a>
      <a class="slide" href="/apps/#android" style="--glow: rgba(35,80,255,.7)">
        <div><span class="tagline">Android · Design and testing</span><h3>A new Android app</h3><p>Our next app for Android is being designed and tested. We will share its name and details when it is ready.</p><span class="btn btn-white">Learn more {ARROW}</span></div>
        <div class="art-tile" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS["phone"]}</svg></div>
      </a>
    </div>
  </div>
</section>

<section class="block soft">
  <div class="wrap">
{head_center("Our goals", "What we aim for")}
{cards([("heart", "Software people trust", "Apps that do what they say, keep data on your device and never surprise you."),
        ("lang", "Clear for everyone", "Plain words and readable screens, in many languages, for experts and first-time users alike."),
        ("clock", "Built to last", "Careful releases, a public changelog and fixes that come before new features.")])}
    <p class="center mt"><a class="more-link" href="/about/">More about the studio {ARROW}</a></p>
  </div>
</section>

<section class="block">
  <div class="wrap">
{head_center("How we work", "From idea to release")}
{cards([("pen", "<span class='num'>01</span>Plan and design", "Screens and words first, decisions written down."),
        ("code", "<span class='num'>02</span>Build and translate", "Native code and every text in 14 languages."),
        ("flask", "<span class='num'>03</span>Test on real devices", "Real phones and many Android versions."),
        ("rocket", "<span class='num'>04</span>Review and release", "A security review, then a careful release.")], "cards four")}
    <p class="center mt"><a class="more-link" href="/process/">See our development process {ARROW}</a></p>
  </div>
</section>

<section class="block dark">
  <div class="wrap">
    <div class="head-row">
      <div><p class="kicker">Security</p><h2>Privacy is where we start</h2></div>
      <a class="btn btn-white" href="/security/">How we keep you safe {ARROW}</a>
    </div>
{cards([("shield", "No account, no server", "Wayfile works without sign-up and has no server of ours to send your files to."),
        ("lock", "Protected transfers", "A one-time PIN and an approval on the phone for every computer."),
        ("key", "Encrypted passwords", "Saved network passwords are locked with Android's hardware-backed key store."),
        ("eye", "Tested like an attacker", "Every release is checked by trying to break it, not only by using it.")], "cards four")}
  </div>
</section>

<section class="block">
  <div class="wrap">
    <div class="stats">
      <div><strong>14</strong><span>languages, including right-to-left Arabic</span></div>
      <div><strong>Android 8+</strong><span>supported, tested on versions 9 to 17</span></div>
      <div><strong>79</strong><span>test steps in Wayfile's test list</span></div>
      <div><strong>3</strong><span>rounds of security review before launch</span></div>
    </div>
  </div>
</section>

<section class="cta" id="contact">
  <div class="wrap">
    <h2>Let's talk</h2>
    <p>Questions, ideas or feedback about our apps. We read every message.</p>
    <a class="btn btn-white" href="/support/">Visit support {ARROW}</a>
  </div>
</section>
""", doc=False, hero_cls="hero home")

# ---------- Apps ----------
page("/apps/", "Apps – AC App Labs",
     "Apps by AC App Labs: Wayfile, a private file manager for Android, and what comes next.",
     """    <p class="eyebrow">AC App Labs</p>
    <h1>Our <span>apps</span></h1>
    <p class="lead">One app on its way to Google Play, a game for Steam and a new Android app in the works.</p>""",
     f"""
<section class="block">
  <div class="wrap">
    <div class="split">
      <div class="collage">
        <div class="pc"><img src="/assets/wayfile-pc.jpg" alt="" width="960" height="600"></div>
        <div class="ph"><img src="/assets/wayfile-home.jpg" alt="" width="540" height="1200"></div>
      </div>
      <div>
        <p class="kicker">Android · Coming soon to Google Play</p>
        <h2>Wayfile</h2>
        <p class="lead">A tidy, private file manager for Android, with Wi-Fi transfer to your computer and NAS.</p>
        <ul class="ticks">
          <li>Browse, search and organize every file</li>
          <li>Free up space with a clear cleanup</li>
          <li>Send files to your computer or NAS over Wi-Fi</li>
          <li>14 languages, Android 8 and up</li>
        </ul>
        <a class="btn btn-blue" href="/wayfile/">Explore Wayfile {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="block soft" id="game">
  <div class="wrap intro">
    <div><span class="status-chip">Coming soon on Steam</span><p class="kicker" style="margin-top:18px">PC game · Design and testing</p><h2>Our first game</h2></div>
    <div>
      <p class="big">We are making a game for PC. It is in the design and testing stage, and it will be released on Steam.</p>
      <p>We are building it with the same care as our apps, tested on real machines before release. Its name, screenshots and Steam page will appear here when they are ready.</p>
    </div>
  </div>
</section>

<section class="block" id="android">
  <div class="wrap intro">
    <div><span class="status-chip">In design</span><p class="kicker" style="margin-top:18px">Android · Design and testing</p><h2>A new Android app</h2></div>
    <div>
      <p class="big">Our next Android app is being designed and tested.</p>
      <p>Like Wayfile, it will be private by default, translated with care and tested on real phones before it reaches Google Play. We will share its name and details when it is ready.</p>
    </div>
  </div>
</section>
""", doc=False)

# ---------- Studio ----------
page("/about/", "About the studio – AC App Labs",
     "AC App Labs is a small, independent software studio. Our goals, values and journey so far.",
     """    <p class="eyebrow">The studio</p>
    <h1>Small studio, <span>full ownership</span></h1>
    <p class="lead">Design, code, testing and translation all happen here, for every app we make.</p>""",
     f"""
<section class="block">
  <div class="wrap intro">
    <div><p class="kicker">Who we are</p><h2>An independent software studio</h2></div>
    <div>
      <p class="big">AC App Labs builds apps for phones and computers that are clear to use and respectful of your data.</p>
      <p>We are small on purpose. Nobody else decides what goes into our apps, so we can keep them simple, private and well tested. Wayfile, our first app, started as the file manager we wanted on our own phones.</p>
    </div>
  </div>
</section>

<section class="block soft">
  <div class="wrap">
{head_center("Our goals", "What we aim for")}
{cards([("heart", "Software people trust", "Apps that do what they say, keep your data on your device and never surprise you."),
        ("lang", "Clear for everyone", "Plain words and readable screens in many languages, for experts and first-time users alike."),
        ("clock", "Built to last", "Careful releases, a public changelog and fixes before new features."),
        ("shield", "Privacy by default", "No account where none is needed, and nothing leaves the device unless you send it."),
        ("game", "Apps and games", "From useful tools for your phone to games for your PC."),
        ("users", "Listening to users", "Your questions and feedback shape what we build next.")])}
  </div>
</section>

<section class="block">
  <div class="wrap">
{head_center("Our journey", "How it started")}
    <ol class="timeline">
      <li><span class="dot">01</span><span class="when">October 2026</span><h3>Wayfile begins</h3><p>A file manager in the style of a desktop explorer: two panes, copy and move with Undo, recycle bin and tags.</p></li>
      <li><span class="dot">02</span><span class="when">October 2026</span><h3>Phone meets computer</h3><p>Transfer to a computer's browser with a one-time PIN, and to NAS and shared folders over the local network.</p></li>
      <li><span class="dot">03</span><span class="when">October 2026</span><h3>14 languages and this website</h3><p>Every screen translated, including right-to-left Arabic; acapplabs.com goes live.</p></li>
      <li><span class="dot">04</span><span class="when">Now</span><h3>Testing and security review</h3><p>Real-device tests and three rounds of security review before the Google Play release.</p></li>
      <li><span class="dot">05</span><span class="when">Next</span><h3>Google Play, Steam and more</h3><p>Wayfile's release on Google Play, our first PC game coming to Steam, and a new Android app now in design and testing.</p></li>
    </ol>
  </div>
</section>
""", doc=False)

# ---------- Process ----------
STEPS = [
    ("Plan", "Every app starts with a written plan: what it must do well, step by step, with each decision recorded and the reason next to it."),
    ("Design", "We sketch the screens and write the words before the code. If a screen needs a manual, it is redesigned."),
    ("Build", "Native code for each platform. Release builds are small and signed, and every change is kept in version control."),
    ("Translate", "Every text exists in all 14 languages before release, checked by a script so none is missing, with right-to-left layout for Arabic."),
    ("Test on real devices", "Each feature is tried on real phones of different brands and on Android versions from 9 to 17, from a written test list."),
    ("Security review", "We read the code looking for weaknesses, then try to break the app from an attacker's side, on the same Wi-Fi and with crafted files."),
    ("Release and support", "Updates go out through Google Play with a public changelog. Security fixes come first, and important ones must be installed when the app opens."),
]
page("/process/", "How we work – AC App Labs",
     "How AC App Labs builds apps: planning, design, native development, translation, real-device testing, security review and release.",
     """    <p class="eyebrow">How we work</p>
    <h1>Our <span>development process</span></h1>
    <p class="lead">Seven steps every app goes through, from the first idea to updates after release.</p>""",
     f"""
<section class="block">
  <div class="wrap">
    <ol class="timeline">
{chr(10).join(f'      <li><span class="dot">{n:02d}</span><h3>{t}</h3><p>{d}</p></li>' for n, (t, d) in enumerate(STEPS, 1))}
    </ol>
  </div>
</section>

<section class="block soft">
  <div class="wrap">
{head_center("In numbers", "Wayfile's road to release")}
    <div class="stats">
      <div><strong>79</strong><span>steps in the written test list</span></div>
      <div><strong>2 + 6</strong><span>real phones and emulated Android versions</span></div>
      <div><strong>31</strong><span>issues logged in testing, each fixed or explained</span></div>
      <div><strong>3</strong><span>security review rounds</span></div>
    </div>
  </div>
</section>
""", doc=False)

# ---------- Security ----------
page("/security/", "Security – AC App Labs",
     "How AC App Labs protects your data: no account or server, protected local transfers, encrypted passwords and regular attacker-view testing.",
     """    <p class="eyebrow">Security</p>
    <h1>Privacy is <span>where we start</span></h1>
    <p class="lead">What we do to keep your files and data safe, in plain words. Tap a card to read the details.</p>""",
     f"""
<section class="block">
  <div class="wrap">
{more_cards([
    ("shield", "No account, no server of ours", "Your files stay on your phone.",
     ["Wayfile works without sign-up or login.", "We do not run a server that receives your files.", "Files leave the phone only when you send them: to your computer, your network storage or an app you choose."]),
    ("lock", "Protected computer transfers", "Your computer has to prove it is allowed in.",
     ["A six-digit PIN that works once.", "Every connection is approved on the phone.", "The session is tied to that computer and ends when the phone locks.", "Too many wrong PINs stop the server.", "Connections over mobile data are refused."]),
    ("wifi", "Careful on open networks", "A warning before you use an open Wi-Fi.",
     ["On Wi-Fi without a password, Wayfile warns before starting a transfer and keeps a warning on screen while it runs (Android 12 and later).", "Outgoing internet traffic is always encrypted (HTTPS)."]),
    ("users", "Safe on shared computers", "Internet cafés, schools and libraries.",
     ["Mark the computer as shared when signing in: the session ends after 2 idle minutes and as soon as the tab closes.", "The page signs out and clears itself after a while without activity.", "After disconnecting, it reminds you to delete downloaded files."]),
    ("key", "Encrypted passwords", "Network passwords can't be read off the phone.",
     ["Saved NAS and PC passwords are encrypted with Android's hardware-backed key store and can't be decrypted on another device.", "They are left out of backups and device transfers.", "Editing a network location never shows the saved password."]),
    ("file", "Safe with untrusted files", "Archives and file names can't trick the app.",
     ["ZIP entries that try to write outside the target folder are skipped, and free space is checked first.", "File names with hidden direction characters can't pass an app off as a document.", "Other apps can't make Wayfile open or copy its private data."]),
    ("eye", "Tested like an attacker", "Three rounds of review before launch.",
     ["A code review for weaknesses, a deep review of every file operation, and a hands-on attempt to break the app from the same Wi-Fi.", "Every finding is fixed and re-tested before release."]),
    ("bolt", "Fast security updates", "Fixes reach you quickly.",
     ["Security fixes are released through Google Play.", "Important updates are offered as soon as you open the app and must be installed to continue.", "Every change is listed in a public changelog."]),
])}
  </div>
</section>

<section class="block soft">
  <div class="wrap intro">
    <div><p class="kicker">Found a problem?</p><h2>Report a security issue</h2></div>
    <div>
      <p class="big">If you think you have found a security problem in one of our apps, please tell us privately first.</p>
      <p>Our security contact address will be listed here soon. Until then, see <a class="more-link" href="/support/">Support</a>. The full details of what Wayfile does with data are in the <a class="more-link" href="/wayfile/privacy/">privacy policy</a>.</p>
    </div>
  </div>
</section>
""", doc=False)

# ---------- Wayfile ----------
SHOWCASE = """<div class="wrap showcase" id="closer">
  <div class="stage">
    <div class="stage-head">
      <div class="stage-title"><img src="/assets/wayfile.png" alt="" width="44" height="44"><div><b>A closer look at Wayfile</b><small>Tap a number to see what it does</small></div></div>
      <div class="seg" role="tablist">
        <button role="tab" aria-selected="true" data-view="v-phone">Phone</button>
        <button role="tab" aria-selected="false" data-view="v-pc">Computer</button>
      </div>
    </div>
    <div class="view phone" id="v-phone">
      <ol class="notes left">
        <li><button data-i="1"><span class="n">01</span><span><b>Ready for your PC</b><span class="t">Send files over Wi-Fi. No cable, no account.</span></span></button></li>
        <li><button data-i="2"><span class="n">02</span><span><b>Added today</b><span class="t">Downloads, saves and shares from today in one place.</span></span></button></li>
      </ol>
      <div class="screen">
        <img src="/assets/wayfile-home.jpg" alt="Wayfile home screen" width="540" height="1200">
        <button class="hot" data-i="1" style="left:57%;top:6.3%" aria-label="1">1</button>
        <button class="hot" data-i="2" style="left:4%;top:21%" aria-label="2">2</button>
        <button class="hot" data-i="3" style="left:27%;top:52%" aria-label="3">3</button>
        <button class="hot" data-i="4" style="left:5%;top:72.5%" aria-label="4">4</button>
      </div>
      <ol class="notes left">
        <li><button data-i="3"><span class="n">03</span><span><b>Storage at a glance</b><span class="t">Real sizes, read from the disk itself.</span></span></button></li>
        <li><button data-i="4"><span class="n">04</span><span><b>Every file by type</b><span class="t">Images, videos, documents, archives and apps.</span></span></button></li>
      </ol>
      <ol class="notes all">
        <li><button data-i="1"><span class="n">01</span><span><b>Ready for your PC</b><span class="t">Send files over Wi-Fi. No cable, no account.</span></span></button></li>
        <li><button data-i="2"><span class="n">02</span><span><b>Added today</b><span class="t">Downloads, saves and shares from today in one place.</span></span></button></li>
        <li><button data-i="3"><span class="n">03</span><span><b>Storage at a glance</b><span class="t">Real sizes, read from the disk itself.</span></span></button></li>
        <li><button data-i="4"><span class="n">04</span><span><b>Every file by type</b><span class="t">Images, videos, documents, archives and apps.</span></span></button></li>
      </ol>
    </div>
    <div class="view wide" id="v-pc" hidden>
      <div class="screen">
        <img src="/assets/wayfile-pc.jpg" alt="Wayfile transfer page in a computer's browser" width="960" height="600">
        <button class="hot" data-i="1" style="left:61%;top:13%" aria-label="1">1</button>
        <button class="hot" data-i="2" style="left:33%;top:46%" aria-label="2">2</button>
        <button class="hot" data-i="3" style="left:33%;top:57%" aria-label="3">3</button>
        <button class="hot" data-i="4" style="left:33%;top:73%" aria-label="4">4</button>
      </div>
      <ol class="notes">
        <li><button data-i="1"><span class="n">01</span><span><b>Your language</b><span class="t">The page follows the browser's language.</span></span></button></li>
        <li><button data-i="2"><span class="n">02</span><span><b>One-time PIN</b><span class="t">Six digits from the phone, valid once.</span></span></button></li>
        <li><button data-i="3"><span class="n">03</span><span><b>Approved on the phone</b><span class="t">Every connection is confirmed there.</span></span></button></li>
        <li><button data-i="4"><span class="n">04</span><span><b>Direct, no server</b><span class="t">Same network only; files never go to a server.</span></span></button></li>
      </ol>
    </div>
  </div>
</div>"""

page("/wayfile/", "Wayfile – File manager for Android",
     "Wayfile is a file manager for Android: browse and organize files, free up space, and send files to your computer or NAS over Wi-Fi. Your files stay on your device.",
     f"""    <img class="app-icon" src="/assets/wayfile.png" alt="" width="88" height="88">
    <h1>Wayfile</h1>
    <p class="lead">A tidy, private file manager for Android, with Wi-Fi transfer to your computer and NAS.</p>
    <span class="status">Coming soon to Google Play</span>""",
     f"""
{SHOWCASE}

<section class="block" id="features">
  <div class="wrap">
{head_center("What it does", "Everything your files need, in one clear app", "Tap a card to see the details.")}
{more_cards([
    ("folder", "Browse and organize", "Every file and folder, the way a computer shows them.",
     ["Two panes side by side for copying and moving.", "Undo after copy, move, rename and delete.", "Tags, a file basket for collecting files, and a recycle bin you can restore from.", "Go straight to any folder by typing its address."]),
    ("search", "Find anything", "Search names, and the text inside documents.",
     ["Search the text of PDF, Word and Excel files, right on the phone.", "Categories for images, videos, audio, documents, archives and apps.", "\"Added today\" lists everything that arrived today."]),
    ("trash", "Free up space", "See what fills your phone and clear it.",
     ["Large files, duplicates and app caches.", "The camera copy is kept as the original when duplicates look alike.", "Shrink photos and videos before sharing them."]),
    ("pc", "Computer over Wi-Fi", "Send files both ways from any browser.",
     ["Nothing to install on the computer.", "A one-time PIN and approval on the phone.", "Download a whole folder as one ZIP; live progress with speed and time left."]),
    ("nas", "NAS and shared folders", "Work with your network storage.",
     ["Browse, upload and download on SMB network locations.", "Back up your phone's photos, documents and messaging media.", "Keep a folder in sync with one-way sync; transfers resume after a dropped connection."]),
    ("box", "Archives and contact cards", "ZIP files and .vcf cards open inside the app.",
     ["Open, extract and create ZIP files, including old Windows ZIPs with Turkish names.", "See the people in a .vcf file and add one or several to your contacts."]),
])}
  </div>
</section>

<section class="block soft" id="tested">
  <div class="wrap">
{head_center("How it is tested", "Tried on real phones before you get it")}
    <div class="stats">
      <div><strong>79</strong><span>steps in the written test list</span></div>
      <div><strong>31</strong><span>issues logged, each fixed or explained</span></div>
      <div><strong>9–17</strong><span>Android versions checked</span></div>
      <div><strong>3</strong><span>security review rounds</span></div>
    </div>
    <ul class="devices" aria-label="Test devices">
      <li>Xiaomi <span>· Android 16, HyperOS</span></li>
      <li>General Mobile GM 24 Plus</li>
      <li>Emulators <span>· Android 9, 10, 11, 12, 13, 17</span></li>
      <li>Phones and tablets</li>
    </ul>
    <div class="cards mt">
      <article class="card">{ico("flask")}<h3>Every feature, step by step</h3><p>Install, start-up time, file operations, cleanup, PC and NAS transfer, languages and permissions, each with an expected result.</p></article>
      <article class="card">{ico("eye")}<h3>Attacks tried on purpose</h3><p>Wrong PINs, requests from another computer, crafted ZIP files and misleading file names are all refused.</p></article>
      <article class="card">{ico("bolt")}<h3>Real-world conditions</h3><p>Locked screens, dropped Wi-Fi, open networks, battery savers and very large files.</p></article>
    </div>
  </div>
</section>

<section class="block" id="tips">
  <div class="wrap">
{head_center("Usage tips", "Get more out of Wayfile", "Small things that make a big difference.")}
{more_cards([
    ("eye", "Not sure what a tile does?", "Every home screen tile has an ⓘ button.",
     ["Tap ⓘ to read what the tile is for and how to use it, with a shortcut to open it."]),
    ("pc", "Send files to your computer", "Same Wi-Fi, a browser and a PIN.",
     ["Open PC transfer in Wayfile.", "Type the address it shows into the computer's browser.", "Enter the PIN and approve on the phone."]),
    ("users", "On a shared computer?", "Tick \"This is a shared computer\" when signing in.",
     ["The session ends after 2 idle minutes and when the tab closes.", "Delete what you downloaded before you leave."]),
    ("clock", "Changed your mind?", "Undo is right there.",
     ["After copying, moving, renaming or deleting, tap Undo in the address bar.", "Deleted items go to the recycle bin first, so you can restore them."]),
    ("bolt", "Transfers stop in the background?", "Some phones pause apps to save battery.",
     ["Settings has a battery guide with the exact steps for Xiaomi, Samsung, Huawei, OPPO, vivo and others."]),
    ("nas", "NAS only at home", "Keep network locations to Wi-Fi.",
     ["Each network location can be set to connect only over Wi-Fi, so it never uses mobile data."]),
])}
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
      <div class="actions" style="display:flex;flex-wrap:wrap;gap:12px">
        <a class="btn btn-blue" href="/wayfile/privacy/">Privacy policy {ARROW}</a>
        <a class="btn btn-line" href="/security/">Security</a>
      </div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
{head_center("Details", "Good to know")}
    <div class="facts-row">
      <div><strong>Android 8.0 or newer</strong><span>Phones and tablets.</span></div>
      <div><strong>14 languages</strong><span>Including right-to-left Arabic.</span></div>
      <div><strong>Free with small ads</strong><span>A one-time Pro purchase removes them.</span></div>
    </div>
    <div class="doc-links" style="justify-content:center">
    </div>
  </div>
</section>

<section class="block soft" id="legal">
  <div class="wrap">
{head_center("Privacy and terms", "The rules, in plain words", "Wayfile's privacy policy and terms of use, in English and Turkish.")}
    <div class="cards">
      <a class="card link-card" href="/wayfile/privacy/">{ico("shield")}<h3>Privacy policy</h3><p>What Wayfile does with data: files stay on your phone, what ads collect, permissions and why.</p><span class="more-link">Read {ARROW}</span></a>
      <a class="card link-card" href="/wayfile/terms/">{ico("file")}<h3>Terms of use</h3><p>The agreement for using Wayfile: your responsibilities, Pro, liability and how to reach us.</p><span class="more-link">Read {ARROW}</span></a>
      <a class="card link-card" href="/wayfile/licenses/">{ico("box")}<h3>Open-source licenses</h3><p>The libraries Wayfile is built with, and their licenses.</p><span class="more-link">Read {ARROW}</span></a>
    </div>
    <div class="doc-links" style="justify-content:center">
      <a class="btn btn-line" href="/wayfile/privacy/tr/">Gizlilik politikası (Türkçe)</a>
      <a class="btn btn-line" href="/wayfile/terms/tr/">Kullanım koşulları (Türkçe)</a>
      <a class="btn btn-line" href="/support/">Support</a>
    </div>
  </div>
</section>
""", doc=False, hero_cls="page-hero tall")

# ---------- Support ----------
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
  <p>Tap the ⓘ button on a home screen tile to see what it does and how to use it. More tips are on the <a href="/wayfile/#tips">Wayfile page</a>.</p></details>

  <h2 id="contact">Contact</h2>
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
