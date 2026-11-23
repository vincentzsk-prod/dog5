#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
# COLLAR, the DØG-5 manual (the Driver Manual), as a web page: docs/manual/index.html, from dog5-docs/manual/ (Parts 0-2B and Parts 3-4, the
# player-facing parts; Part 5, the internal voicing notes, stays in the Project). The brand comes from ../play/brand/.
#   python3 tools/make_manual_page.py            write docs/manual/index.html
#   python3 tools/make_manual_page.py --check    fail if the page would change
# Needs Python-Markdown (pip install markdown).
import html, re, sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("make_manual_page: needs Python-Markdown (pip install markdown)")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dog5-docs/manual"
OUT = ROOT / "docs/manual/index.html"
FEEDBACK = "https://github.com/vincentzsk-prod/dog5/issues/new?template=feedback.md"

def listfix(text):
    """Python-Markdown wants a blank line before a list; the docs (written for GitHub) often have none."""
    out, prev = [], ""
    for line in text.split("\n"):
        if re.match(r"\s{0,3}([-*+]|\d+\.) ", line) and prev.strip() and not re.match(r"\s*([-*+]|\d+\.) ", prev) and not prev.startswith("  "):
            out.append("")
        out.append(line); prev = line
    return "\n".join(out)

def part(name, start):
    t = (SRC / name).read_text(encoding="utf-8")
    i = t.find(start)
    if i < 0:
        sys.exit(f"make_manual_page: {name} has no '{start}'")
    return t[i:]

PARTS = {   # the h2 headings of the manual -> (badge, title)
    "0. WHAT DØG-5 IS": ("0", "What DØG-5 is"),
    "PART 1 — THE PANEL": ("1", "The panel"),
    "PART 2 — THE VOICING DICTIONARY": ("2", "The voicing dictionary"),
    "PART 2B — TALKING IN NUMBERS": ("2B", "Talking in numbers"),
    "PART 3 — THE 32 PATCHES": ("3", "The 32 patches"),
    "PART 4 — ABOUT THE GEAR INSPIRATIONS": ("4", "About the gear inspirations"),
}
CHAP = {"I": 1, "II": 2, "III": 3, "IV": 4}

def esc(t):
    return html.escape(t, quote=True)

def sec_label(name):
    """'1.1 Buttons / the grid' -> ('1.1', 'Buttons / the grid'); 'CHAPTER II — BEE-TCH' -> ('II', 'Bee-tch')."""
    name = html.unescape(name)
    m = re.match(r"(\d+\.\d+)\s+(.*)", name)
    if m:
        return m.group(1), m.group(2)
    m = re.match(r"CHAPTER (I{1,3}|IV) — (.*)", name)
    if m:
        return m.group(1), m.group(2).capitalize().replace("Acid can", "Acid Can")
    return "", name

def nav(tokens):
    out = []
    for t in tokens:
        badge, title = PARTS.get(t["name"], ("", t["name"]))
        out.append(f'<details class="grp" data-id="{t["id"]}"><summary><span class="pn">{esc(badge)}</span>'
                   f'<a href="#{t["id"]}">{esc(html.unescape(title))}</a></summary>' + ("<ul>" if t["children"] else ""))
        for c in t["children"]:
            num, title = sec_label(c["name"])
            if c["name"].startswith("CHAPTER "):
                ch = CHAP[num]
                out.append(f'<li class="chap ch-{ch}"><a href="#{c["id"]}"><span class="sn">{num}</span>{esc(title)}</a>'
                           '<ol class="patches">')
                for k in c["children"]:
                    m = re.match(r"(\d\d) · (.*)", html.unescape(k["name"]))
                    nn, pn = (m.group(1), m.group(2)) if m else ("", k["name"])
                    out.append(f'<li><a href="#{k["id"]}" title="{esc(nn + " " + pn)}"><span class="nn">{nn}</span>{esc(pn)}</a></li>')
                out.append("</ol></li>")
            else:
                out.append(f'<li><a href="#{c["id"]}">' + (f'<span class="sn">{esc(num)}</span>' if num else "") + f'{esc(title)}</a></li>')
        out.append(("</ul>" if t["children"] else "") + "</details>")
    return "\n".join(out)

def shape(content):
    """Part banners, numbered section heads, chapter colours, and each patch as a card."""
    def h2(m):
        attrs, text = m.group(1), m.group(2)
        badge, title = PARTS.get(html.unescape(re.sub(r"<[^>]+>", "", text)), ("", None))
        if title is None:
            return m.group(0)
        return f'<h2{attrs} class="part"><span class="pn">Part {esc(badge)}</span>{esc(title)}</h2>'
    content = re.sub(r"<h2([^>]*)>(.*?)</h2>", h2, content)
    def h3(m):
        attrs, text = m.group(1), m.group(2)
        num, title = sec_label(html.unescape(re.sub(r"<[^>]+>", "", text)))
        if text.startswith("CHAPTER "):
            return f'<h3{attrs} class="chap ch-{CHAP[num]}"><span class="sn">Chapter {num}</span>{esc(title)}</h3>'
        return f'<h3{attrs}>' + (f'<span class="sn">{esc(num)}</span>' if num else "") + f'{esc(title)}</h3>'
    content = re.sub(r"<h3([^>]*)>(.*?)</h3>", h3, content)
    # each patch (an h4 inside Part 3) becomes a card, coloured by its chapter
    parts = re.split(r"(?=<h[234][ >])", content)
    out, ch, open_card = [], 0, False
    for p in parts:
        m3 = re.match(r'<h3[^>]*class="chap ch-(\d)"', p)
        if p.startswith("<h2") or p.startswith("<h3"):
            if open_card:
                out.append("</section>"); open_card = False
            ch = int(m3.group(1)) if m3 else (ch if not p.startswith("<h2") else 0)
            out.append(p)
        elif p.startswith("<h4") and ch:
            if open_card:
                out.append("</section>")
            nm = re.match(r'<h4([^>]*)>(\d\d) · (.*?)</h4>', p)
            if nm:
                p = f'<h4{nm.group(1)}><span class="nn">{nm.group(2)}</span>{nm.group(3)}</h4>' + p[nm.end():]
            out.append(f'<section class="patch ch-{ch}">{p}'); open_card = True
        else:
            out.append(p)
    if open_card:
        out.append("</section>")
    content = "".join(out)
    content = content.replace("<p><strong>Sound design notes</strong></p>", '<p class="lbl">Sound design notes</p>')
    content = content.replace("<p><strong>Gear inspirations</strong></p>", '<p class="lbl">Gear inspirations</p>')
    return content

def render():
    body = part("DOG-5-driver-manual.md", "## 0. WHAT DØG-5 IS") + "\n\n" + part("DOG-5-driver-manual-patches.md", "## PART 3")
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc"], extension_configs={"toc": {"toc_depth": "2-4"}},
                           output_format="html")
    content = md.convert(listfix(body))
    content = re.sub(r"<a\b[^>]*href=\"(?!https?://|#)[^\"]*\"[^>]*>(.*?)</a>", r"\1", content, flags=re.S)   # repo-relative links
    if re.search(r"<(script|iframe|style)\b", content, re.I):
        sys.exit("make_manual_page: the manual carries markup the page does not take")
    toc = nav(md.toc_tokens)
    content = shape(content)
    return TEMPLATE.replace("{FEEDBACK}", FEEDBACK).replace("{TOC}", toc).replace("{CONTENT}", content)

TEMPLATE = """<!doctype html>
<!-- SPDX-License-Identifier: GPL-3.0-only -->
<!-- Generated by tools/make_manual_page.py from dog5-docs/manual/. Edit those, not this. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>COLLAR — the DØG-5 manual</title>
<meta name="description" content="COLLAR, the DØG-5 manual: the panel, the screen, saving, installing, the voicing words and the 32 patches.">
<link rel="icon" href="../play/brand/dog5-favicon-240.png">
<link rel="stylesheet" href="../play/brand/brand.css">
<style>
* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 14px; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body { margin: 0; background: var(--black); color: var(--white); font: 400 19px/1.6 var(--body); }
a { color: var(--acid); }
.c1 { --ch: var(--yellow); } .c2 { --ch: var(--turq); } .c3 { --ch: var(--white); } .c4 { --ch: var(--acid); }
.ch-1 { --ch: var(--yellow); } .ch-2 { --ch: var(--turq); } .ch-3 { --ch: var(--white); } .ch-4 { --ch: var(--acid); }
.top { max-width: 1240px; margin: 0 auto; padding: 20px 16px 6px; text-align: center; }
.draft { max-width: 760px; margin: 14px auto 4px; padding: 10px 14px; text-align: left; font-size: 17px; border: 2px solid var(--black);
  border-left: 6px solid var(--acid); background: var(--plum); box-shadow: 5px 5px 0 var(--violet); }
.links { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin: 14px 0 4px; }
.links a { padding: 8px 16px; border: 2px solid var(--violet); text-decoration: none; color: var(--white); font: 700 13px var(--mono); background: var(--black); }
.links a:hover, .links a.cta { border-color: var(--acid); color: var(--acid); }
.wrap { max-width: 1240px; margin: 0 auto; padding: 8px 16px 40px; display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 34px; align-items: start; }

/* the contents: one card per part; numbers in mono, words in the body face, so the eye finds the groups */
nav.toc { position: sticky; top: 12px; max-height: calc(100vh - 24px); overflow: auto; padding: 0 4px 12px 0;
  scrollbar-width: thin; scrollbar-color: var(--violet) transparent; }
.navhead { display: flex; align-items: center; justify-content: space-between; margin: 0 0 8px; font: 700 11px var(--mono);
  letter-spacing: .14em; text-transform: uppercase; color: var(--olive); }
.find { width: 100%; margin: 0 0 12px; padding: 8px 10px; background: var(--black); color: var(--white); border: 2px solid var(--violet);
  font: 400 13px var(--mono); }
.find:focus { outline: none; border-color: var(--acid); }
.grp { margin: 0 0 8px; background: var(--plum); border: 2px solid var(--violet); }
.grp[open] { box-shadow: 4px 4px 0 var(--violet); }
.grp > summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 10px; padding: 9px 10px; }
.grp > summary::-webkit-details-marker { display: none; }
.grp > summary::after { content: "+"; margin-left: auto; font: 700 16px var(--mono); color: var(--olive); }
.grp[open] > summary::after { content: "–"; color: var(--acid); }
.grp > summary a { color: var(--white); text-decoration: none; font: 400 17px/1.2 var(--display); }
.grp > summary:hover a, .grp.on > summary a { color: var(--acid); }
.pn { flex: none; min-width: 28px; padding: 2px 5px; text-align: center; font: 700 12px var(--mono); color: var(--black); background: var(--acid); }
.grp ul { list-style: none; margin: 0; padding: 2px 10px 10px 12px; border-top: 1px solid var(--violet); }
.grp li { margin: 0; }
.grp li > a { display: flex; gap: 8px; align-items: baseline; padding: 4px 6px; color: #d9cfe0; text-decoration: none; font: 400 16px/1.3 var(--body);
  border-left: 3px solid transparent; }
.grp li > a:hover { color: var(--white); background: rgba(255,255,255,.04); }
.grp li > a.on { color: var(--white); border-left-color: var(--acid); background: rgba(222,244,2,.07); }
.sn { flex: none; font: 700 11px var(--mono); color: var(--olive); min-width: 26px; }
.grp li.chap { margin-top: 6px; }
.grp li.chap > a { font: 400 15px var(--display); color: var(--ch); text-transform: uppercase; letter-spacing: .04em; }
.grp li.chap > a .sn { color: var(--ch); opacity: .8; }
.patches { list-style: none; margin: 2px 0 4px; padding: 0 0 0 6px; display: grid; grid-template-columns: 1fr 1fr; gap: 2px 6px; }
.patches a { display: flex; gap: 5px; padding: 2px 4px; font: 400 14px/1.25 var(--body); color: #cbbfd4; text-decoration: none;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; border-left: 2px solid transparent; }
.patches a:hover { color: var(--white); }
.patches a.on { color: var(--white); border-left-color: var(--ch); background: rgba(255,255,255,.05); }
.nn { flex: none; font: 700 10px/1.9 var(--mono); color: var(--ch, var(--olive)); }
.toc-mobile { display: none; }

/* the text */
article { min-width: 0; max-width: 820px; }
article h2.part { display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; font: 400 34px/1.15 var(--display); color: var(--acid);
  margin: 56px 0 16px; padding: 14px 16px 12px; background: var(--plum); border: 2px solid var(--violet); box-shadow: 6px 6px 0 var(--violet); }
article h2.part:first-child { margin-top: 18px; }
article h2.part .pn { font-size: 13px; letter-spacing: .1em; text-transform: uppercase; padding: 3px 8px; }
article h3 { display: flex; align-items: baseline; gap: 10px; font: 400 23px/1.25 var(--display); color: var(--yellow); margin: 34px 0 10px;
  padding-left: 12px; border-left: 4px solid var(--yellow); }
article h3 .sn { font: 700 13px var(--mono); color: var(--olive); }
article h3.chap { color: var(--ch); border-left-color: var(--ch); font-size: 28px; margin-top: 44px; }
article h3.chap .sn { color: var(--ch); opacity: .8; text-transform: uppercase; letter-spacing: .08em; }
article h4 { font: 700 13px/1.3 var(--mono); color: var(--turq); margin: 18px 0 6px; text-transform: uppercase; letter-spacing: .06em; }
article p, article li { max-width: 72ch; }
article ul { padding-left: 1.2em; }
article li { margin: 4px 0; }
article li::marker { color: var(--violet); }
article code { font: 13px var(--mono); color: var(--glow); }
article pre { background: var(--plum); border: 2px solid var(--violet); padding: 10px; overflow: auto; }
article table { border-collapse: collapse; margin: 12px 0 18px; font-size: 16px; display: block; overflow-x: auto; }
article th, article td { border: 1px solid var(--violet); padding: 5px 9px; vertical-align: top; text-align: left; }
article th { font: 700 12px var(--mono); color: var(--acid); background: var(--plum); text-transform: uppercase; letter-spacing: .05em; }
article tr:nth-child(even) td { background: rgba(50,4,68,.45); }
article strong { font-weight: 600; color: #fff; }
article em { color: #e9e1ee; }
article blockquote { margin: 10px 0; padding: 6px 14px; border-left: 4px solid var(--violet); color: var(--olive); }

/* a patch is a card in its chapter's colour */
section.patch { margin: 18px 0 22px; padding: 4px 18px 10px; background: rgba(50,4,68,.55); border: 2px solid var(--violet);
  border-top: 4px solid var(--ch); }
section.patch h4 { display: flex; align-items: baseline; gap: 10px; font: 700 27px/1.2 var(--body); color: var(--ch);
  text-transform: none; letter-spacing: 0; margin: 12px 0 6px; }
section.patch h4 .nn { font-size: 13px; line-height: 1; padding: 3px 6px; color: var(--black); background: var(--ch); }
section.patch .lbl { margin: 14px 0 4px; font: 700 11px var(--mono); letter-spacing: .14em; text-transform: uppercase; color: var(--ch); }
section.patch > p:first-of-type { font-size: 20px; }

.totop { position: fixed; right: 16px; bottom: 16px; padding: 8px 12px; font: 700 12px var(--mono); color: var(--black); background: var(--acid);
  text-decoration: none; box-shadow: 3px 3px 0 var(--violet); opacity: 0; pointer-events: none; transition: opacity .2s; }
.totop.show { opacity: 1; pointer-events: auto; }
footer { max-width: 1240px; margin: 0 auto; padding: 16px; font: 400 12px/1.6 var(--mono); color: var(--olive); text-align: center; }
@media (max-width: 900px) {
  .wrap { grid-template-columns: 1fr; gap: 10px; }
  nav.toc { position: static; max-height: none; overflow: visible; }
  nav.toc .navbody { display: none; } nav.toc.open .navbody { display: block; }
  .toc-mobile { display: block; width: 100%; padding: 10px; font: 700 13px var(--mono); color: var(--black); background: var(--acid); border: 0; cursor: pointer; }
  .navhead { display: none; }
  article h2.part { font-size: 27px; }
}
</style>
</head>
<body>
<header class="top">
  <div class="lockup">
    <img class="mark" src="../play/brand/dog5-favicon-240.png" width="120" height="120" alt="">
    <div>
      <h1 class="word"><img src="../play/brand/dog5-wordmark-pixel.png" width="370" height="122" alt="DØG-5"></h1>
      <p class="tagline">the runt bastard no one wanted</p>
      <p class="what">COLLAR · the manual · M-VAVE FM-1</p>
    </div>
  </div>
  <p class="draft" role="note"><b>COLLAR</b> is the DØG-5 manual, for v0.5: the panel, the screen, saving and installing, the
    words for sound, and all 32 patches. Built and tested on an FM-1 with the older flash chip (Puya P25Q80, <code>0x856014</code>);
    newer units with the UC25HQ80 (<code>0xB36014</code>) have never run DØG-5.</p>
  <p class="links"><a href="../play/">Play it in your browser</a> <a href="../install/">Install on your FM-1</a>
    <a class="cta" href="{FEEDBACK}" target="_blank" rel="noopener">Send feedback</a>
    <a href="https://github.com/vincentzsk-prod/dog5">Source code</a></p>
</header>
<div class="wrap">
<nav class="toc" id="toc" aria-label="Contents">
  <button class="toc-mobile" id="tocbtn" aria-expanded="false" aria-controls="toc">Contents</button>
  <div class="navbody">
  <div class="navhead"><span>Contents</span><span id="where"></span></div>
  <input class="find" id="find" type="search" placeholder="Find a section or a patch…" aria-label="Find a section or a patch">
  {TOC}
  </div>
</nav>
<article>
{CONTENT}
</article>
</div>
<a class="totop" id="totop" href="#">↑ Top</a>
<footer>DØG-5 by ZIGGY (DØGS) · GPL-3.0-only · a fork of OberVave v1.5.3 (zvenson), on Dinghy (zvenson), Felucca (Leo Kuroshita,
  Hügelton Instruments) and SLOOP (isod89). Fonts: Yatra One, Cormorant Garamond, Space Mono (SIL OFL 1.1). Art hand-painted by ZIGGY.
  Gear names are inspirations only; their trademarks belong to their owners. Not affiliated with M-VAVE.</footer>
<script>
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll("nav.toc a[href^='#']"));
  var byId = {}; links.forEach(function (a) { (byId[a.getAttribute("href").slice(1)] = byId[a.getAttribute("href").slice(1)] || []).push(a); });
  var heads = Array.prototype.slice.call(document.querySelectorAll("article h2[id], article h3[id], article h4[id]"));
  var groups = Array.prototype.slice.call(document.querySelectorAll("nav.toc details.grp"));
  var first = groups[0]; if (first) first.open = true;
  var current = null, searching = false;
  function mark(id) {
    if (id === current) return; current = id;
    links.forEach(function (a) { a.classList.remove("on"); });
    groups.forEach(function (g) { g.classList.remove("on"); });
    (byId[id] || []).forEach(function (a) {
      a.classList.add("on");
      var g = a.closest("details.grp");
      if (g) { g.classList.add("on"); if (!searching) { groups.forEach(function (o) { if (o !== g) o.open = false; }); g.open = true; } }
      if (a.closest(".grp li") && a.scrollIntoView && window.innerWidth > 900) {
        var nav = document.getElementById("toc"), r = a.getBoundingClientRect(), n = nav.getBoundingClientRect();
        if (r.top < n.top + 40 || r.bottom > n.bottom - 20) nav.scrollTop += r.top - n.top - n.height / 3;
      }
    });
  }
  function spy() {
    var y = window.scrollY + 90, id = heads.length ? heads[0].id : null;
    for (var i = 0; i < heads.length; i++) { if (heads[i].offsetTop <= y) id = heads[i].id; else break; }
    if (id) mark(id);
    document.getElementById("totop").classList.toggle("show", window.scrollY > 900);
  }
  var t = null; window.addEventListener("scroll", function () { if (!t) t = setTimeout(function () { t = null; spy(); }, 80); }, { passive: true });
  spy();
  var find = document.getElementById("find");
  find.addEventListener("input", function () {
    var q = find.value.trim().toLowerCase(); searching = !!q;
    groups.forEach(function (g) {
      var any = false;
      g.querySelectorAll("li").forEach(function (li) {
        var hit = !q || li.textContent.toLowerCase().indexOf(q) >= 0;
        li.style.display = hit ? "" : "none"; if (hit) any = true;
      });
      var self = !q || g.querySelector("summary").textContent.toLowerCase().indexOf(q) >= 0;
      g.style.display = (any || self) ? "" : "none";
      if (q) g.open = any; 
    });
  });
  var btn = document.getElementById("tocbtn"), nav = document.getElementById("toc");
  btn.addEventListener("click", function () { var o = nav.classList.toggle("open"); btn.setAttribute("aria-expanded", o); });
  nav.addEventListener("click", function (e) { if (e.target.closest("a") && window.innerWidth <= 900) { nav.classList.remove("open"); btn.setAttribute("aria-expanded", false); } });
})();
</script>
</body>
</html>
"""

page = render()
if "--check" in sys.argv:
    if not OUT.exists() or OUT.read_text(encoding="utf-8") != page:
        sys.exit("make_manual_page: docs/manual/index.html is out of date (run tools/make_manual_page.py)")
    print("in sync: docs/manual/index.html")
else:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"page     {OUT.relative_to(ROOT)}  {len(page.encode())} B")
