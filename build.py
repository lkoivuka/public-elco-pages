#!/usr/bin/env python3
"""Generate the ELCO public support/privacy/terms site (GitHub Pages).

One shared site, one section per app. To add an app: create
apps/<slug>/{meta.json, privacy.md, terms.md, support.md} and an
assets/<slug>-icon.png, then run:  python3 build.py
(only apps present under apps/ are published — nothing else)

meta.json fields: name, tagline, icon, support_email (per-app inbox).
"""
import json, html, pathlib, markdown

ROOT = pathlib.Path(__file__).parent
APPS = ROOT / "apps"
# per-app footer data credit (only where a real upstream source is used)
CREDITS = {
    "evergladestopo": "Elevation data derived from public U.S. Geological Survey (USGS) sources (public domain).",
}

CSS = """
:root{--bg:#020617;--panel:#0b1220;--ink:#e6eef6;--muted:#9fb0c0;--accent:#f5a524;--teal:#2dd4bf;--line:#1e2a3a}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:48px 22px 80px}
header.brand{display:flex;align-items:center;gap:14px;margin-bottom:8px}
header.brand img{width:56px;height:56px;border-radius:13px;box-shadow:0 2px 10px rgba(0,0,0,.4)}
header.brand .t{font-weight:700;font-size:20px;letter-spacing:.2px}
nav{margin:22px 0 34px;padding-bottom:18px;border-bottom:1px solid var(--line);display:flex;gap:20px;flex-wrap:wrap}
nav a{color:var(--teal);text-decoration:none;font-weight:600;font-size:15px}
nav a:hover{text-decoration:underline}
h1{font-size:30px;line-height:1.2;margin:.2em 0 .1em}
h2{font-size:20px;margin:1.8em 0 .4em;color:#fff}
p,li{color:var(--ink)}
.muted{color:var(--muted)}
a{color:var(--accent)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:22px 24px;margin:22px 0;display:flex;gap:18px;align-items:flex-start}
.card img{width:64px;height:64px;border-radius:15px;flex:0 0 auto}
.card .links{margin-top:8px;display:flex;gap:16px;flex-wrap:wrap}
.card .links a{font-weight:600;font-size:14px}
.email{font-size:18px;font-weight:700}
.contact{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:24px 0}
footer{margin-top:54px;padding-top:22px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
"""

def shell(title, brand_name, brand_icon, nav_html, body, footer_html):
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="robots" content="index,follow">
<style>{CSS}</style></head><body><div class="wrap">
<header class="brand"><img src="{brand_icon}" alt="{html.escape(brand_name)} icon"><div class="t">{html.escape(brand_name)}</div></header>
<nav>{nav_html}</nav>
{body}
<footer>{footer_html}</footer>
</div></body></html>"""

def md(path):
    return markdown.markdown(path.read_text().strip(), extensions=["extra","sane_lists"])

def md_titlebody(path):
    lines = path.read_text().splitlines()
    h1 = lines[0][2:].strip() if lines and lines[0].startswith("# ") else ""
    body = markdown.markdown("\n".join(lines[1:]).strip(), extensions=["extra","sane_lists"])
    return h1, body

def appnav(rel, slug):
    return (f'<a href="{rel}">All apps</a>'
            f'<a href="{rel}{slug}/">Support</a>'
            f'<a href="{rel}{slug}/privacy/">Privacy</a>'
            f'<a href="{rel}{slug}/terms/">Terms</a>')

def appfooter(name, email, credit):
    cr = f"<br>{html.escape(credit)}" if credit else ""
    return f'{html.escape(name)} by ELCO · <a href="mailto:{email}">{email}</a>{cr}'

apps = sorted(p.name for p in APPS.iterdir() if p.is_dir())
for slug in apps:
    a = APPS / slug
    meta = json.loads((a/"meta.json").read_text())
    name, icon, email = meta["name"], meta["icon"], meta["support_email"]
    credit = CREDITS.get(slug, "")
    foot = appfooter(name, email, credit)

    # support (depth 1)
    body = f'<h1>Support</h1>\n<p>{html.escape(meta["tagline"])}</p>\n' \
           f'<div class="contact"><p class="muted" style="margin:0 0 6px">Questions, bug reports, or feedback? Email us:</p>' \
           f'<p class="email" style="margin:0"><a href="mailto:{email}">{email}</a></p></div>\n' \
           + md(a/"support.md") + \
           f'\n<h2>Legal</h2><p>See our <a href="privacy/">Privacy Policy</a> and <a href="terms/">Terms of Use</a>.</p>'
    (ROOT/slug).mkdir(exist_ok=True)
    (ROOT/slug/"index.html").write_text(
        shell(f"Support — {name}", name, f"../assets/{icon}", appnav("../", slug), body, foot))

    # privacy + terms (depth 2)
    for kind, fname, ttl in [("privacy","privacy.md","Privacy Policy"),("terms","terms.md","Terms of Use")]:
        h1, b = md_titlebody(a/fname)
        (ROOT/slug/kind).mkdir(exist_ok=True)
        (ROOT/slug/kind/"index.html").write_text(
            shell(f"{ttl} — {name}", name, f"../../assets/{icon}", appnav("../../", slug),
                  f"<h1>{html.escape(h1)}</h1>\n{b}", foot))

# landing (root) — links to each app's support page; no single inbox shown here
cards = ""
for slug in apps:
    meta = json.loads((APPS/slug/"meta.json").read_text())
    cards += (f'<div class="card"><img src="assets/{meta["icon"]}" alt="{html.escape(meta["name"])} icon">'
              f'<div><div style="font-weight:700;font-size:18px">{html.escape(meta["name"])}</div>'
              f'<div class="muted" style="font-size:14px;margin-top:3px">{html.escape(meta["tagline"])}</div>'
              f'<div class="links"><a href="{slug}/">Support</a><a href="{slug}/privacy/">Privacy</a><a href="{slug}/terms/">Terms</a></div>'
              f'</div></div>\n')
landing = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ELCO Apps — Support & Legal</title><meta name="robots" content="index,follow">
<style>{CSS}</style></head><body><div class="wrap">
<header class="brand"><div class="t">ELCO Apps</div></header>
<p class="muted">Support, privacy, and terms for ELCO's iOS apps. Choose an app for its support contact.</p>
{cards}
<footer>ELCO</footer>
</div></body></html>"""
(ROOT/"index.html").write_text(landing)
(ROOT/".nojekyll").write_text("")
print("built site for apps:", ", ".join(apps))
