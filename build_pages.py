#!/usr/bin/env python3
"""Tastea Boba (Appleton WI) — template v2 T1 build, 2026-11-24, card t_abc78b8a.
Design: espresso counter-board / Futura-caps display + Georgia body / passionfruit-rose + thai-orange accents.
Facts: card-verified only (press Post-Crescent, GBP, FB intro/About, IG bio, Nominatim geo). Hours NOT published -> omitted."""
import os, json, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
ORIGIN = "https://tastea-boba-appleton-demo.up.railway.app"
NAME = "Tastea Boba"
ADDR = "317 E Calumet St, Appleton, WI 54915"
TEL_D = "(920) 572-8191"
TEL_U = "+19205728191"
EMAIL = "Tasteaboballc@gmail.com"
FB = "https://www.facebook.com/profile.php?id=61812325"  # placeholder replaced below
FB = "https://www.facebook.com/profile.php?id=61592082812325"
IG = "https://www.instagram.com/tastea.boballc/"
LAT, LNG = 44.2437915, -88.4003920
MAPQ = "317+E+Calumet+St%2C+Appleton%2C+WI+54915"

def canonical(path="/"):
    return ORIGIN + "/" if path == "/" else ORIGIN + path

def ld(objs):
    return "\n".join('<script type="application/ld+json">' + json.dumps(o, separators=(",", ":"), ensure_ascii=False) + "</script>" for o in objs)

def head(path, title, desc, extra_ld=None):
    lds = []
    if extra_ld:
        lds = extra_ld
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta name="theme-color" content="#2b1a13">
<link rel="canonical" href="{canonical(path)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{canonical(path)}">
<meta property="og:image" content="{ORIGIN}/og.png">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
{ld(lds)}
</head>"""

NAV = [("/", "Home"), ("/menu", "Menu"), ("/milk-tea", "Milk Tea"), ("/desserts", "Waffles & Crepes"), ("/visit", "Visit"), ("/contact", "Contact")]

def nav(cur):
    items = []
    for href, label in NAV:
        on = ' aria-current="page"' if href == cur else ""
        cls = ' class="on"' if href == cur else ""
        items.append(f'<a href="{href}"{on}{cls}>{label}</a>')
    return (f'<header class="top"><div class="wrap bar">'
            f'<a class="brand" href="/"><span class="cupmark" aria-hidden="true"></span>{NAME}</a>'
            f'<nav aria-label="Main">{"".join(items)}</nav>'
            f'<a class="pill call" href="tel:{TEL_U}">Call</a>'
            f'</div></header>')

def foot():
    return f"""<footer class="foot"><div class="wrap footgrid">
<div><p class="fbrand">{NAME}</p><p class="ftag">Sip &bull; Smile &bull; Repeat &mdash; made fresh with love.</p></div>
<div class="footcol"><p>317 E Calumet St<br>Appleton, WI 54915</p><p><a href="tel:{TEL_U}">{TEL_D}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<nav class="footnav" aria-label="Footer">{" ".join(f'<a href="{h}">{l}</a>' for h, l in NAV if h != "/")} <a href="/privacy">Privacy</a></nav>
</div><p class="footline"><span>&copy; 2026 {NAME}, Appleton, Wisconsin</span></p></footer>"""

def page(path, title, desc, body, extra_ld=None, cur="/"):
    skip = '<a class="skip" href="#main">Skip to main content</a>\n'
    return (head(path, title, desc, extra_ld) + "\n<body>\n" + skip + nav(cur) + "\n<main id=\"main\">\n" + body + "\n</main>\n" + foot() + "\n</body>\n</html>\n")

def crumbs(*items):
    nodes = [{"@type": "ListItem", "position": i + 1, "name": n, "item": canonical(p)} for i, (n, p) in enumerate(items)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": nodes}

FAQ_LDS = lambda qs: {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}

BUSINESS = {
    "@context": "https://schema.org", "@type": "CafeOrCoffeeShop", "name": NAME,
    "image": ORIGIN + "/og.png", "url": ORIGIN,
    "address": {"@type": "PostalAddress", "streetAddress": "317 E Calumet St", "addressLocality": "Appleton",
                "addressRegion": "WI", "postalCode": "54915", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
    "telephone": "+" + TEL_U, "sameAs": [FB, IG],
}

# ---------------------------------------------------------------- home
HOME_FAQ = [
    ("What's on the menu at Tastea Boba?",
     "Classic milk and fruit teas with flavors like taro, thai, passion fruit and lychee, plus smoothies, slushies, bubble waffles, crepes and other foods and desserts."),
    ("Where is Tastea Boba in Appleton?",
     "317 E Calumet St, Appleton, WI 54915 — in the former Little Caesars building on East Calumet Street."),
    ("When did Tastea Boba open?",
     "Tastea Boba soft-opened on September 19, 2026."),
    ("What are your hours?",
     "Call (920) 572-8191 and we'll tell you exactly what's on today."),
]
home_ld = [dict(BUSINESS,
                description="A tea and dessert shop in Appleton, Wisconsin serving classic milk and fruit teas, smoothies, slushies, bubble waffles, crepes and other desserts."),
            FAQ_LDS(HOME_FAQ)]

CUP = f'''<div class="artcup" aria-hidden="true"><i class="straw"></i><div class="lid"></div><div class="body"><b class="milk"></b><b class="pearl p1"></b><b class="pearl p2"></b><b class="pearl p3"></b><b class="pearl p4"></b><b class="pearl p5"></b></div></div>'''

home = f"""<section class="hero"><div class="wrap herogrid">
<div class="herotxt"><p class="kicker">Appleton&rsquo;s new boba &amp; dessert counter</p>
<h1>Boba <span class="amp">&bull;</span> Crepes <span class="amp">&bull;</span> Sweet Treats</h1>
<p class="lede">Classic milk tea, shaken fruit tea, bubble waffles and fresh crepes at the corner of Calumet Street. Sip &bull; Smile &bull; Repeat &mdash; made fresh with love.</p>
<p class="herocta"><a class="pill big" href="/menu">See the menu</a> <a class="pill ghost" href="/visit">Find us</a></p>
<p class="openline">Soft-opened September 19, 2026 &bull; Rated <strong>4.6</strong> on Google</p></div>
{CUP}</div></section>

<section class="strip"><div class="wrap stripgrid">
<div><p class="num">01</p><h3>Milk Tea &amp; Fruit Tea</h3><p>Taro, thai, passion fruit, lychee and more — brewed to order, your choice of tea.</p><p><a href="/milk-tea">Sip the lineup &rarr;</a></p></div>
<div><p class="num">02</p><h3>Smoothies &amp; Slushies</h3><p>Blended cold when you want the fruit front and center.</p><p><a href="/menu">Full menu &rarr;</a></p></div>
<div><p class="num">03</p><h3>Bubble Waffles &amp; Crepes</h3><p>The crispy-and-creamy counter, right next to the shake machine.</p><p><a href="/desserts">Waffles &amp; crepes &rarr;</a></p></div>
</div></section>

<div class="wrap"><hr class="pearls" aria-hidden="true"></div>

<section class="wrap two">
<div><h2>A new dessert counter on Calumet Street</h2>
<p>Tastea Boba opened in the former Little Caesars building at 317 E Calumet St, bringing Appleton its own tea-and-dessert counter: tea shaken with milk or cut with fruit, waffles piped into bubbles, crepes folded fresh.</p>
<p>Find the bright counter, place your order, and give it a second at one of the tables. Rated 4.6 by Google reviewers already — come see why.</p>
<p class="mapline"><a class="pill" href="https://www.google.com/maps?q={MAPQ}" target="_blank" rel="noopener">Open in Maps</a> <a class="pill ghost" href="tel:{TEL_U}">Call {TEL_D}</a></p></div>
<figure class="mapframe"><iframe title="Map to Tastea Boba, 317 E Calumet St, Appleton, WI 54915" loading="lazy" src="https://www.google.com/maps?q={MAPQ}&amp;output=embed"></iframe></figure>
</section>

<section class="faqwrap"><div class="wrap two faq">
<div><h2>Questions before you come</h2><p class="muted">Straight answers. Hours move with the menu — a quick call tells you what&rsquo;s on today.</p></div>
<details open><summary>What&rsquo;s on the menu?</summary><p>Classic milk and fruit teas with flavors like taro, thai, passion fruit and lychee, plus smoothies, slushies, bubble waffles, crepes and other foods and desserts.</p></details>
<details><summary>Where are you in Appleton?</summary><p>317 E Calumet St, Appleton, WI 54915 — the former Little Caesars building on East Calumet Street.</p></details>
<details><summary>When did you open?</summary><p>We soft-opened on September 19, 2026.</p></details>
<details><summary>What are your hours?</summary><p>Call <a href="tel:{TEL_U}">{TEL_D}</a> and we&rsquo;ll tell you exactly what&rsquo;s on today.</p></details>
</div></section>

<section class="board-cite"><div class="wrap"><p class="cite">Menu and opening facts as reported by the Appleton Post-Crescent (Sept 30, 2026) and the shop&rsquo;s own Facebook and Instagram pages.</p></div></section>"""

# ---------------------------------------------------------------- menu hub
MENU_SECTIONS = [
    ("Milk &amp; Fruit Teas", "Classic milk teas and shaken fruit teas", "Taro &bull; Thai &bull; Passion Fruit &bull; Lychee &bull; more", "/milk-tea", "Explore teas"),
    ("Smoothies", "Blended fruit, cold", "Shaken or blended — pick your base", "/milk-tea", "Tea &amp; blends"),
    ("Slushies", "Ice, whipped to order", "Frosty cups for slow afternoons", "/menu", "—"),
    ("Bubble Waffles", "Crispy batter, piped in bubbles", "Topped at the counter", "/desserts", "Dessert counter"),
    ("Crepes", "Folded fresh, sweet or savory", "The quiet classic", "/desserts", "Dessert counter"),
    ("More Foods &amp; Desserts", "A rotating counter of treats", "Ask what&rsquo;s on today", "/contact", "Ask us"),
]

def board_rows():
    out = []
    for i, (name, sub, meta, href, cta) in enumerate(MENU_SECTIONS):
        link = "" if href == "/menu" else f'<a class="rowcta" href="{href}">{cta} &rarr;</a>'
        out.append(f'<div class="row"><div class="rn"><span class="rowno">{i+1:02d}</span><div><h3>{name}</h3><p>{sub}</p></div></div><p class="flavors">{meta}</p>{link}</div>')
    return "\n".join(out)

menu_ld = [{"@context": "https://schema.org", "@type": "Menu", "name": f"{NAME} Menu",
            "hasMenuSection": [
                {"@type": "MenuSection", "name": n, "description": s} for n, s, m, _, _ in MENU_SECTIONS],
            "belongsTo": {**BUSINESS, "@id": ORIGIN}},
           crumbs(("Home", "/"), ("Menu", "/menu"))]

menu = f"""<section class="pagehero"><div class="wrap"><p class="kicker">The counter board</p><h1>Menu at {NAME}</h1>
<p class="lede">Teas shaken with milk or cut with fruit, blended cups, and the waffle-and-crepe counter. Prices and the full line-up live at the register — call {TEL_D} for today.</p></div></section>
<section class="wrap"><div class="board" role="list">
{board_rows()}
</div>
<p class="fineprint">Menu categories, flavors and items as reported by the Appleton Post-Crescent and shown on {NAME}&rsquo;s Facebook page. Prices are posted at the counter and not listed here.</p>
<p class="centercta"><a class="pill big" href="/milk-tea">Milk tea &amp; fruit tea</a> <a class="pill ghost big" href="/desserts">Waffles, crepes &amp; desserts</a></p></section>"""

# ---------------------------------------------------------------- milk tea detail
MT_FAQ = [
    ("What milk tea flavors do you have?", "The classics on the board include taro and thai, with more teas on the counter menu."),
    ("What about fruit tea?", "Shaken fruit teas include passion fruit and lychee, listed among the tea flavors on the board."),
    ("Do you have boba in everything?", "It's a boba shop — ask for your tea classic, with the pearls."),
]
milk_ld = [{"@context": "https://schema.org", "@type": "Service", "serviceType": "Boba milk tea & fruit tea",
            "provider": {"@id": ORIGIN}, "areaServed": {"@type": "City", "name": "Appleton", "includedInArea": {"@type": "AdministrativeArea", "name": "Appleton, Wisconsin"}},
            "url": canonical("/milk-tea")},
           crumbs(("Home", "/"), ("Menu", "/menu"), ("Milk Tea & Fruit Tea", "/milk-tea")),
           FAQ_LDS(MT_FAQ)]

milk = f"""<section class="pagehero"><div class="wrap"><p class="kicker">Detail &bull; Tea counter</p><h1>Milk Tea &amp; Fruit Tea in Appleton</h1>
<p class="lede">At {NAME}, tea is the house craft: milk tea shaken smooth, fruit tea shaken bright. Flavors on the board include taro, thai, passion fruit and lychee — plus the rest of what the counter pours.</p>
<p class="herocta"><a class="pill big" href="tel:{TEL_U}">Call to order ahead</a> <a class="pill ghost" href="/menu">See the full board</a></p></div></section>

<section class="wrap two">
<div><h2>Classics, shaken to order</h2>
<p>Taro milk tea is the one people come back for; thai tea brings the orange, aromatic shake. If you like it lighter, the fruit teas cut the sweetness — passion fruit and lychee lead the list the press wrote about, and the board has more.</p>
<p>Smoothies and slushies sit on the same counter when you want the fruit whole — blended, frosted, made after you order.</p>
<h2>With your waffle</h2><p>A milk tea travels well next to a bubble waffle or a folded crepe — the dessert counter is two steps from the tea station. See the <a href="/desserts">waffle &amp; crepe page</a>.</p></div>
<div class="sidecard"><h3>Milk Tea &amp; Fruit Tea</h3><ul class="flavlist"><li>Taro</li><li>Thai</li><li>Passion fruit</li><li>Lychee</li><li>&hellip;and more on the counter board</li></ul><p class="fineprint">Flavors as reported by the Appleton Post-Crescent, Sept 30, 2026.</p><hr class="pearls" aria-hidden="true"><p><a class="pill" href="/visit">Directions</a></p><p><a class="pill ghost" href="tel:{TEL_U}">{TEL_D}</a></p></div>
</section>

<section class="faqwrap"><div class="wrap two faq">
<div><h2>Tea questions</h2></div>
<details open><summary>What milk tea flavors do you have?</summary><p>The classics on the board include taro and thai, with more teas on the counter menu.</p></details>
<details><summary>What about fruit tea?</summary><p>Shaken fruit teas include passion fruit and lychee, listed among the tea flavors on the board.</p></details>
<details><summary>Do you have boba in everything?</summary><p>It&rsquo;s a boba shop — ask for your tea classic, with the pearls.</p></details>
</div></section>"""

# ---------------------------------------------------------------- desserts detail
DS_FAQ = [
    ("Do you make bubble waffles?", "Yes — bubble waffles are piped and crisped at the counter."),
    ("Are the crepes made fresh?", "Crepes are folded fresh at the counter, sweet or savory styles on the board."),
    ("What else do you serve?", "The shop also carries other foods and desserts beyond the teas and waffles — ask at the counter for what's on today."),
]
dess_ld = [{"@context": "https://schema.org", "@type": "Service", "serviceType": "Bubble waffles, crepes & desserts",
            "provider": {"@id": ORIGIN}, "areaServed": {"@type": "City", "name": "Appleton", "includedInArea": {"@type": "AdministrativeArea", "name": "Appleton, Wisconsin"}},
            "url": canonical("/desserts")},
           crumbs(("Home", "/"), ("Menu", "/menu"), ("Waffles, Crepes & Desserts", "/desserts")),
           FAQ_LDS(DS_FAQ)]

dess = f"""<section class="pagehero"><div class="wrap"><p class="kicker">Detail &bull; Dessert counter</p><h1>Bubble Waffles, Crepes &amp; Desserts</h1>
<p class="lede">{NAME} isn&rsquo;t only a tea cup. The dessert counter runs bubble waffles and fresh crepes alongside the teas — the combo Appleton was missing.</p>
<p class="herocta"><a class="pill big" href="/menu">Full menu</a> <a class="pill ghost" href="tel:{TEL_U}">Call {TEL_D}</a></p></div></section>

<section class="wrap two">
<div><h2>The bubble waffle</h2>
<p>Batter piped into its bubble grid, cooked crisp on the outside, soft inside — the ice-cream-shop waffle you order next to your milk tea, not after it.</p>
<h2>Crepes, folded to order</h2><p>Sweet fillings, savory folds — the press called them out beside the smoothies and slushies as part of what the counter makes fresh.</p>
<h2>And the rest of the case</h2><p>The shop serves other foods and desserts beyond tea, waffles and crepes — the counter keeps its own rotation, so ask what&rsquo;s on today, or call ahead.</p></div>
<div class="sidecard"><h3>Dessert counter</h3><ul class="flavlist"><li>Bubble waffles</li><li>Crepes</li><li>Slushies &amp; smoothies</li><li>Other foods &amp; desserts</li></ul><p class="fineprint">Menu categories as reported by the Appleton Post-Crescent, Sept 30, 2026.</p><hr class="pearls" aria-hidden="true"><p><a class="pill" href="/visit">Directions</a></p></div>
</section>

<section class="faqwrap"><div class="wrap two faq">
<div><h2>Dessert questions</h2></div>
<details open><summary>Do you make bubble waffles?</summary><p>Yes — bubble waffles are piped and crisped at the counter.</p></details>
<details><summary>Are the crepes made fresh?</summary><p>Crepes are folded fresh at the counter, sweet or savory styles on the board.</p></details>
<details><summary>What else do you serve?</summary><p>The shop also carries other foods and desserts beyond the teas and waffles — ask at the counter for what&rsquo;s on today.</p></details>
</div></section>"""

# ---------------------------------------------------------------- visit
VISIT_FAQ = [
    ("Where is Tastea Boba?", "317 E Calumet St, Appleton, WI 54915 — the former Little Caesars building."),
    ("What are your hours?", "Call (920) 572-8191 — hours follow the menu, so a quick call gives you today's."),
    ("Can I call ahead?", "Yes — (920) 572-8191 gets your order started before you drive over."),
]
visit_ld = [{**BUSINESS, "@id": canonical("/visit")},
            crumbs(("Home", "/"), ("Visit", "/visit")),
            FAQ_LDS(VISIT_FAQ)]

visit = f"""<section class="pagehero"><div class="wrap"><p class="kicker">Come by</p><h1>Visit {NAME} in Appleton</h1>
<p class="lede">You already know the building — {NAME} runs the counter inside the former Little Caesars at 317 E Calumet St. Look for the tea sign.</p></div></section>

<section class="wrap twoc">
<figure class="mapframe tall"><iframe title="Map to Tastea Boba, 317 E Calumet St, Appleton, WI 54915" loading="lazy" src="https://www.google.com/maps?q={MAPQ}&amp;output=embed"></iframe></figure>
<div class="visitcard">
<h2>Find the counter</h2>
<p class="addr"><strong>{NAME}</strong><br>317 E Calumet St<br>Appleton, WI 54915</p>
<p class="badgerow"><span class="badge">Boba</span> <span class="badge">Crepes</span> <span class="badge">Sweet treats</span> <span class="badge">LGBTQ+ friendly</span></p>
<p><a class="pill big" href="tel:{TEL_U}">Call {TEL_D}</a></p>
<p><a class="pill ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination={MAPQ}" target="_blank" rel="noopener">Directions</a> <a class="pill ghost" href="https://www.google.com/maps?q={MAPQ}" target="_blank" rel="noopener">See the map</a></p>
<p class="fineprint">Address, phone and the LGBTQ+-friendly listing shown on the shop&rsquo;s Google business listing and Facebook page.</p>
<hr class="pearls" aria-hidden="true">
<p><a href="{FB}" target="_blank" rel="noopener">Facebook</a> &bull; <a href="{IG}" target="_blank" rel="noopener">Instagram</a></p>
</div></section>

<section class="faqwrap"><div class="wrap two faq">
<div><h2>Before you drive</h2></div>
<details open><summary>Where exactly?</summary><p>317 E Calumet St, Appleton, WI 54915 — the former Little Caesars building on East Calumet Street.</p></details>
<details><summary>What are your hours?</summary><p>Call <a href="tel:{TEL_U}">{TEL_D}</a> — a quick call gives you today&rsquo;s hours and menu.</p></details>
<details><summary>Can I call ahead?</summary><p>Yes — <a href="tel:{TEL_U}">{TEL_D}</a> gets your cup started before you head over.</p></details>
</div></section>"""

# ---------------------------------------------------------------- contact
CONTACT_FAQ = [("Is there a minimum order?", "No minimum to order at the counter — one cup is a fine order. For anything big, call first."),
               ("How fast do you answer the form?", "Messages go straight to the shop — expect an answer the same day it's open.")]
contact_ld = [{"@context": "https://schema.org", "@type": "ContactPage", "name": f"Contact {NAME}", "url": canonical("/contact"), "mainEntity": {**BUSINESS, "@id": canonical("/contact")}}]

contact = f"""<section class="pagehero"><div class="wrap"><p class="kicker">Say the word</p><h1>Contact {NAME}</h1>
<p class="lede">Catering a party? Curious about today&rsquo;s specials? Call the counter or leave a note here — it lands with the shop.</p></div></section>

<section class="wrap two">
<form class="cform" method="post" action="/contact">
<div class="frow"><label for="f-name">Your name</label><input id="f-name" name="name" type="text" maxlength="120" required autocomplete="name"></div>
<div class="frow"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" maxlength="60" autocomplete="tel"></div>
<div class="frow"><label for="f-email">Email <span class="opt">(optional)</span></label><input id="f-email" name="email" type="email" maxlength="120" autocomplete="email"></div>
<div class="frow"><label for="f-msg">What do you need?</label><textarea id="f-msg" name="message" rows="6" maxlength="4000" required placeholder="e.g. catering for 30 people on Saturday — milk teas and waffles"></textarea></div>
<button class="pill big" type="submit">Send to the shop</button>
</form>
<div class="sidecard"><h3>Or just call</h3><p class="addr"><a href="tel:{TEL_U}"><strong>{TEL_D}</strong></a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>317 E Calumet St<br>Appleton, WI 54915</p>
<hr class="pearls" aria-hidden="true">
<p><a class="pill ghost" href="/menu">Menu</a></p>
<p class="fineprint">The contact form sends your note to the shop&rsquo;s inbox. We don&rsquo;t sell it or spam you — details on the <a href="/privacy">privacy page</a>.</p></div>
</section>"""

# ---------------------------------------------------------------- privacy
privacy = f"""<section class="pagehero"><div class="wrap"><p class="kicker">Fine print</p><h1>Privacy — {NAME}</h1></div></section>
<section class="wrap prose">
<h2>What this site collects</h2>
<p>This is the shop&rsquo;s own website. The only information it collects is what you type into the contact form — your name, and optionally your phone and email, plus your message. The form sends that note to the shop&rsquo;s inbox so the team can answer you.</p>
<h2>Who runs the site</h2>
<p>The site was built for {NAME} of 317 E Calumet St, Appleton, WI 54915. Contact questions about this site: <a href="tel:{TEL_U}">{TEL_D}</a>.</p>
<h2>No trackers</h2>
<p>No advertising pixels, no third-party analytics, no cookies set by this site beyond what a normal web browser keeps. The map preview on the visit page is a Google Maps embed; Google may see your IP when it loads.</p>
<h2>Questions</h2><p>Call the shop at <a href="tel:{TEL_U}">{TEL_D}</a> and ask for whoever handles the website.</p>
</section>"""

# ---------------------------------------------------------------- 404 / thanks
def util(path, title, kicker, h1, body, desc):
    return page(path, title, desc,
        f'<section class="pagehero solo"><div class="wrap"><p class="kicker">{kicker}</p><h1>{h1}</h1>{body}<p class="herocta"><a class="pill big" href="/">Back to home</a> <a class="pill ghost" href="/menu">Menu</a></p></div></section>',
        None, cur=None)

nf = util("/404", f"Page not found — {NAME}", "404", "That cup doesn&rsquo;t exist",
    f"<p class='lede'>The page you asked for isn&rsquo;t on this site. The menu, though, is right where you left it.</p>", f"A page wasn't found on the {NAME} site.")
th = util("/thanks", f"Message sent — {NAME}", "Sent", "Your note is on its way",
    f"<p class='lede'>The shop has your message. If it&rsquo;s urgent, call <a href='tel:{TEL_U}'>{TEL_D}</a>.</p>", f"Thanks for messaging {NAME} in Appleton, Wisconsin.")

# ---------------------------------------------------------------- assets
CSS = """/* Tastea Boba — Appleton WI. Custom design: espresso counter-board, Futura-caps display + Georgia body,
   passionfruit rose / thai orange / lychee coral. Hand-rolled, one sheet, no JS. Built 2026-11-24 (t_abc78b8a). */
:root{
  --espresso:#2b1a13; --espresso2:#38241b; --ink:#33231b; --soft:#6c5a4e;
  --milk:#faf5ec; --card:#fffdf8; --line:#e7ddcc;
  --passion:#c8395f; --passion-deep:#9d2748; --thai:#e0892f; --lychee:#eb9c8f;
  --shadow:6px 6px 0 rgba(43,26,19,.14);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--milk);color:var(--ink);font:17px/1.65 Georgia,"Times New Roman",serif;-webkit-font-smoothing:antialiased}
h1,h2,h3,.brand,.kicker,.pill,.num,.badge,.rowno,.flavors,.badgerow{font-family:Futura,"Century Gothic","Avenir Next","Trebuchet MS","Segoe UI",sans-serif;font-weight:600;letter-spacing:.04em;text-transform:uppercase;line-height:1.15}
h1{font-size:clamp(1.9rem,5vw,3.3rem);letter-spacing:.02em;margin:0 0 .35em}
h2{font-size:clamp(1.25rem,3vw,1.9rem);margin:0 0 .5em}
h3{font-size:1.05rem;margin:0 0 .35em}
p{margin:0 0 1em}
a{color:var(--passion-deep)}
a:hover{color:var(--passion)}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--thai);outline-offset:2px}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;background:var(--espresso);color:var(--milk);padding:8px 14px;border-radius:8px;z-index:9}
/* header — espresso bar */
.top{position:sticky;top:0;z-index:8;background:var(--espresso);border-bottom:3px solid var(--passion)}
.bar{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding-top:10px;padding-bottom:10px}
.brand{display:flex;align-items:center;gap:10px;color:var(--milk);text-decoration:none;font-size:1.05rem}
.cupmark{width:14px;height:18px;border-radius:2px 2px 5px 5px;background:linear-gradient(var(--milk) 0 30%,var(--lychee) 30% 100%);position:relative}
.cupmark::after{content:"";position:absolute;top:-7px;right:-3px;width:3px;height:12px;background:var(--passion);border-radius:2px;transform:rotate(14deg)}
.top nav{display:flex;gap:4px;flex-wrap:wrap;margin-left:auto}
.top nav a{color:var(--milk);opacity:.85;text-decoration:none;font-size:.82rem;padding:8px 10px;border-radius:8px;text-transform:uppercase}
.top nav a:hover{opacity:1;background:rgba(255,255,255,.08)}
.top nav a.on,.top nav a[aria-current="page"]{background:var(--passion);opacity:1;color:#fff}
.pill{display:inline-block;background:var(--passion);color:#fff!important;text-decoration:none;font-size:.85rem;padding:11px 18px;border:2px solid var(--espresso);border-radius:999px;box-shadow:var(--shadow);cursor:pointer}
.pill:hover{background:var(--passion-deep)}
.pill.big{font-size:.95rem;padding:14px 26px}
.pill.ghost{background:transparent;color:var(--ink)!important;border:2px solid var(--ink);box-shadow:none}
.pill.ghost:hover{background:var(--ink);color:var(--milk)!important}
header .pill.call{box-shadow:none;padding:9px 16px;font-size:.78rem}
/* hero — full-bleed espresso */
.hero{background:var(--espresso);color:var(--milk);border-bottom:4px solid var(--thai)}
.hero .kicker{color:var(--lychee)}
.herogrid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(240px,.65fr);gap:44px;align-items:center;padding:64px 22px 70px}
h1{color:inherit}.amp{color:var(--thai)}
.lede{font-size:1.13rem;max-width:36em;color:#efe4d3}
.herotxt .lede{color:#efe4d3}
.kicker{margin:0 0 .8em;font-size:.78rem;color:var(--passion-deep)}
.kicker::before{content:"●  ";color:var(--thai);letter-spacing:0}
.openline{font-family:inherit;font-size:.95rem;color:var(--lychee);letter-spacing:.03em;text-transform:uppercase;margin:1.4em 0 0}
.openline strong{color:#fff;font-size:1.1em}
.herotcta,.herocta{display:flex;gap:14px;flex-wrap:wrap;margin:1.6em 0 0}
.herotxt .pill.ghost{color:var(--milk)!important;border-color:rgba(250,245,236,.6)}.herotxt .pill.ghost:hover{background:var(--milk);color:var(--espresso)!important}
/* css boba cup */
.artcup{position:relative;height:340px;transform:rotate(-2deg)}
.artcup .lid{position:absolute;left:50%;top:38px;transform:translateX(-50%);width:190px;height:20px;background:var(--lychee);border:3px solid var(--ink);border-radius:10px}
.artcup .straw{position:absolute;left:calc(50% + 26px);top:-6px;width:14px;height:120px;background:var(--passion);border:3px solid var(--ink);border-radius:6px;transform:rotate(12deg)}
.artcup .body{position:absolute;left:50%;top:52px;transform:translateX(-50%);width:160px;height:250px;border:3px solid var(--ink);border-radius:12px 12px 26px 26px;overflow:hidden;background:linear-gradient(#f3e7d3 0%,#e9d3b6 100%)}
.artcup .milk{position:absolute;left:0;right:0;top:34%;height:26%;background:#fbf3e6;opacity:.85}
.artcup .pearl{position:absolute;border-radius:50%;background:#17110d;box-shadow:inset -3px -4px 6px rgba(255,255,255,.12)}
.p1{width:26px;height:26px;left:18px;bottom:14px}.p2{width:22px;height:22px;left:58px;bottom:24px}.p3{width:28px;height:28px;left:96px;bottom:10px}.p4{width:20px;height:20px;left:36px;bottom:52px}.p5{width:24px;height:24px;left:80px;bottom:60px}
.p1,.p3,.p5{animation:bob 3.2s ease-in-out infinite alternate}.p2,.p4{animation:bob 2.4s ease-in-out .4s infinite alternate-reverse}
@keyframes bob{from{transform:translateY(0)}to{transform:translateY(-14px)}}
@media (prefers-reduced-motion:reduce){.artcup .pearl{animation:none}}
/* strip cards */
.strip{padding:48px 0 8px}
.stripgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.stripgrid>div{background:var(--card);border:2px solid var(--ink);border-radius:12px;padding:20px 20px 14px;box-shadow:var(--shadow)}
.num{color:var(--passion);font-size:.8rem;margin:0 0 .6em}
.stripgrid h3{font-size:1rem}
.stripgrid p:last-of-type{margin:0}
/* pearl hr */
.pearls{border:0;height:12px;margin:34px auto;background:radial-gradient(circle 5px at 50% 50%,var(--ink) 99%,transparent) repeat-x;background-size:26px 12px;background-position:center;width:min(320px,60%)}
/* two-col generic */
.two{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(240px,.62fr);gap:44px;align-items:start;padding:36px 22px 44px}
.twoc{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(260px,.75fr);gap:30px;align-items:stretch;padding:10px 22px 50px}
.mapframe{margin:0;border:3px solid var(--ink);border-radius:14px;overflow:hidden;box-shadow:var(--shadow);min-height:340px}
.mapframe iframe{width:100%;height:100%;min-height:340px;border:0;display:block}
.mapframe.tall iframe{min-height:430px}
.mapline{display:flex;gap:12px;flex-wrap:wrap}
/* menu board */
.board{background:var(--espresso);color:var(--milk);border:3px solid var(--ink);border-radius:16px;box-shadow:8px 8px 0 rgba(43,26,19,.18);padding:14px 26px 6px;margin:10px 0 22px}
.board .row{display:grid;grid-template-columns:1.35fr 1fr auto;gap:18px;align-items:center;padding:20px 4px;border-bottom:2px dotted rgba(250,245,236,.28)}
.board .row:last-child{border-bottom:0}
.board h3{color:#fff;font-size:1.02rem;margin:0 0 .15em}
.board .row p{margin:0}
.board .rowno{color:var(--thai);font-size:.72rem;display:block;margin-bottom:.35em}
.rn{display:flex;gap:14px;align-items:baseline}
.rn h3+p,.rn div p{font-family:Georgia,serif;text-transform:none;letter-spacing:0;font-weight:400;color:#e8ddca;font-size:.95rem}
.flavors{color:var(--lychee)!important;font-size:.72rem}
.rowcta{white-space:nowrap;color:#fff!important;font-family:Futura,"Century Gothic","Avenir Next",sans-serif;text-transform:uppercase;letter-spacing:.04em;font-size:.72rem;border-bottom:2px solid var(--thai);padding-bottom:2px;text-decoration:none}
.rowcta:hover{border-color:var(--lychee)}
.fineprint{font-size:.85rem;color:var(--soft)}
.centercta{display:flex;gap:14px;flex-wrap:wrap;margin-top:26px}
/* pagehero */
.pagehero{padding:52px 0 18px}
.pagehero.solo{padding:80px 0 60px;text-align:center}
.pagehero.solo .herocta{justify-content:center}
/* sidecard */
.sidecard{background:var(--card);border:2px solid var(--ink);border-radius:14px;padding:22px;box-shadow:var(--shadow)}
.flavlist{list-style:none;margin:0 0 12px;padding:0}
.flavlist li{padding:7px 0 7px 26px;border-bottom:1px dashed var(--line);position:relative}
.flavlist li::before{content:"";position:absolute;left:6px;top:14px;width:10px;height:10px;border-radius:50%;background:var(--passion)}
/* badges */
.badgerow{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 1.2em}
.badge{background:var(--espresso);color:var(--milk);font-size:.68rem;padding:6px 12px;border-radius:999px}
.visitcard{background:var(--card);border:2px solid var(--ink);border-radius:14px;padding:26px;box-shadow:var(--shadow)}
.addr{font-size:1.05rem;line-height:1.5}
/* faq */
.faqwrap{background:#f2e9da;border-top:2px solid var(--line);border-bottom:2px solid var(--line);padding:44px 0 34px;margin-top:44px}
.faq details{background:var(--card);border:2px solid var(--ink);border-radius:12px;padding:0;margin:0 0 12px;box-shadow:var(--shadow)}
.faq summary{cursor:pointer;padding:15px 18px;border-radius:10px}
.faq details p{padding:0 18px 15px;margin:0}
.faq .muted{color:var(--soft)}
/* cite */
.board-cite{padding:26px 0 8px}
.cite{font-size:.85rem;color:var(--soft);border-left:4px solid var(--thai);padding-left:14px}
/* form */
.cform{background:var(--card);border:2px solid var(--ink);border-radius:14px;padding:26px;box-shadow:var(--shadow)}
.frow{display:grid;grid-template-columns:180px 1fr;gap:14px;align-items:start;margin-bottom:18px}
.frow label{font-family:Futura,"Century Gothic",sans-serif;text-transform:uppercase;letter-spacing:.04em;font-size:.72rem;padding-top:12px}
.opt{text-transform:none;letter-spacing:0;color:var(--soft);font-weight:400}
.cform input,.cform textarea{width:100%;padding:12px 14px;font:16px/1.5 Georgia,serif;border:2px solid var(--ink);border-radius:10px;background:#fff;color:var(--ink)}
.cform textarea{resize:vertical}
/* prose */
.prose{max-width:780px;padding:10px 22px 60px}
/* footer */
.foot{background:var(--espresso);color:#e8ddca;margin-top:0;border-top:4px solid var(--passion)}
.footgrid{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:30px;padding:44px 22px 22px}
.fbrand{color:#fff;margin:0 0 .3em}
.ftag{color:var(--lychee);font-size:.9rem;margin:0}
.footcol p{margin:0 0 .8em}
.footcol a{color:var(--lychee)}
.footnav{display:flex;flex-direction:column;gap:6px}
.footnav a{color:#e8ddca;text-decoration:none;font-size:.95rem}
.footnav a:hover{color:#fff;text-decoration:underline}
.footline{max-width:1080px;margin:0 auto;padding:14px 22px 30px;border-top:1px solid rgba(250,245,236,.15);font-size:.85rem;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.footline a{color:#e8ddca}
/* responsive */
@media (max-width:900px){
  .herogrid{grid-template-columns:1fr;padding:44px 22px 54px}
  .artcup{display:none}
  .stripgrid{grid-template-columns:1fr 1fr}
  .two,.twoc{grid-template-columns:1fr}
  .board .row{grid-template-columns:1fr auto;row-gap:6px}
  .flavors{grid-column:1/-1;order:3}
  .footgrid{grid-template-columns:1fr}
}
@media (max-width:620px){
  body{font-size:16px}
  .stripgrid{grid-template-columns:1fr}
  .top nav{margin-left:0;order:3;width:100%}
  .top nav a{padding:7px 9px;font-size:.76rem}
  header .pill.call{margin-left:auto}
  .frow{grid-template-columns:1fr}
  .frow label{padding-top:0}
  .board{padding:8px 16px 2px}
}
"""

SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "".join(f'  <url><loc>{canonical(p)}</loc><lastmod>2026-11-24</lastmod></url>\n' for p in ["/", "/menu", "/milk-tea", "/desserts", "/visit", "/contact", "/privacy"]) + "</urlset>\n"

ROBOTS = f"""User-agent: *
Allow: /
Disallow: /thanks
Disallow: /404

Sitemap: {ORIGIN}/sitemap.xml
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2b1a13"/><path d="M10 11h12l-1.4 14a2 2 0 0 1-2 1.8h-5.2a2 2 0 0 1-2-1.8z" fill="#faf5ec"/><path d="M12 19h8v3.8a2 2 0 0 1-2 1.8h-4a2 2 0 0 1-2-1.8z" fill="#eb9c8f"/><circle cx="13.5" cy="22" r="1.4" fill="#17110d"/><circle cx="18.5" cy="23" r="1.4" fill="#17110d"/><rect x="18" y="4" width="2.6" height="9" rx="1.2" fill="#c8395f" transform="rotate(12 19 8)"/></svg>
"""

def main():
    os.makedirs(OUT, exist_ok=True)
    pages = {
        "index.html": page("/", f"Boba Tea, Crepes &amp; Desserts — {NAME}, Appleton WI".replace("&amp;", "&"),
            f"{NAME} is a tea and dessert shop at 317 E Calumet St in Appleton, Wisconsin — milk tea, shaken fruit tea, smoothies, slushies, bubble waffles, crepes and desserts. Opened September 19, 2026.",
            home, home_ld, cur="/"),
        "menu.html": page("/menu", f"Menu — {NAME}, Appleton WI".replace("&amp;", "&"),
            f"The counter board at {NAME} in Appleton: classic milk and fruit teas (taro, thai, passion fruit, lychee), smoothies, slushies, bubble waffles, crepes and more.",
            menu, menu_ld, cur="/menu"),
        "milk-tea.html": page("/milk-tea", f"Milk Tea &amp; Fruit Tea — {NAME}, Appleton WI".replace("&amp;", "&"),
            "Boba milk tea and shaken fruit tea in Appleton, WI — taro, thai, passion fruit, lychee and more at Tastea Boba on East Calumet Street.",
            milk, milk_ld, cur="/milk-tea"),
        "desserts.html": page("/desserts", f"Bubble Waffles, Crepes &amp; Desserts — {NAME}, Appleton WI".replace("&amp;", "&"),
            f"Bubble waffles, fresh crepes, slushies and other desserts at {NAME}, Appleton&rsquo;s new tea and dessert counter on E Calumet St.",
            dess, dess_ld, cur="/desserts"),
        "visit.html": page("/visit", f"Visit — {NAME}, 317 E Calumet St, Appleton WI".replace("&amp;", "&"),
            f"Find {NAME} at 317 E Calumet St, Appleton, WI 54915 — the former Little Caesars building on East Calumet Street. Call (920) 572-8191.",
            visit, visit_ld, cur="/visit"),
        "contact.html": page("/contact", f"Contact — {NAME}, Appleton WI".replace("&amp;", "&"),
            f"Contact {NAME} in Appleton, Wisconsin by phone at (920) 572-8191 or with the form — catering, specials and anything else for the shop.",
            contact, contact_ld, cur="/contact"),
        "privacy.html": page("/privacy", f"Privacy — {NAME}, Appleton WI".replace("&amp;", "&"),
            f"Privacy notes for the {NAME} website: the contact form, no trackers, and how to reach the shop.",
            privacy, [{"@context": "https://schema.org", "@type": "WebPage", "name": f"Privacy — {NAME}", "url": canonical("/privacy")}], cur=None),
        "404.html": nf, "thanks.html": th,
        "style.css": CSS, "sitemap.xml": SITEMAP, "robots.txt": ROBOTS, "favicon.svg": FAVICON,
    }
    for fn, content in pages.items():
        with open(os.path.join(OUT, fn), "w") as f:
            f.write(content)
    print("wrote", len(pages), "files")

if __name__ == "__main__":
    main()
