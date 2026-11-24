# Tastea Boba — Appleton WI — tastea-boba-appleton

- Card: t_abc78b8a (board websites) — PITCH SENT 2026-11-24
- Repo: https://github.com/gnaritas/tastea-boba-appleton (public)
- Railway: project 59f2ef14-6724-43e4-9df4-e402835256fc (tastea-boba-appleton) / service 90b6df3f-6322-4e0b-820a-fb292861740c / ws "Ramon Leon's Projects"
- Preview: https://tastea-boba-appleton-demo.up.railway.app (domain 3b50ad44-eab0-4bf9-a783-25d7183ae64e)
- Final build: 2026-11-24T06:55:00Z (lede-contrast fix deploy; live style.css sha256 == local 51ac489d6140a97e)
- Brevo var: set; live test 303 → /thanks?via=form; Railway log: "MAILSENT Tasteaboballc@gmail.com"
- Pages: 7 core (/ /menu /milk-tea /desserts /visit /contact /privacy) + /404 /thanks (+ /open pixel). v4 4-tier form T1 (7 core pages).
- Design: espresso counter-board / Futura-caps display + Newsreader body; lychee/thai-tangerine/passion accents. Distinct from Boba House Houston sibling.
- Verified facts used (no invented facts): opened Sept 19 2026, 317 E Calumet St, former Little Caesars building, (920) 572-8191, Tasteaboballc@gmail.com, menu styles (taro/Thai/passion fruit teas, bubble waffles, crepes, taro soft-serve twist), LGBTQ+ friendly — all per card body (Post-Crescent 2026-09-30, Yahoo syndication, FB page intro, GBP geo, Broadly listing). Hours deliberately OMITTED (unverified). Map: address pin (no GBP photo license claimed).
- Gates: _verify PASS fail=[]; curl walk 10 URLs green incl /open 302 + X-Robots-Tag; render-sweep 18 shots (9 pages × 2 viewports) DOM gate rc=0; vision battery 18 shots → 1 REAL defect (.lede 1:1 contrast on milk pages) fixed + 4-shot re-verify CLEAN; truncation claims adjudicated false (scrollWidth==clientWidth, skip-link is the only off-screen element, intentional); map-blank = MAP-BLANK timing artifact (visit frame proved tiles@10s).
- lane.db: deploy + service rows set via sites_agency_state.py; export + verify 5/5 IDENTICAL.
- TZ: shop_tz America/Chicago seeded (tz_gate). Send window 07:00–17:00 CT; today's pitch 09:3x CT.
- Pitch: v6 subject arm (coin sha256(slug)%2=0→v6); founder bundle $249 + $39/mo 31-day trial; ladder t2 2026-12-03 / t3 2026-12-10 / t4 2026-12-17 (Thanksgiving-shifted); teardown recheck >= 2026-12-22.
- Kill guards passed at dispatch: re-verified SERP no own-brand domain; tasteaboba.com 500/0-byte parking (Hostinger NS); 43-stem RDAP sweep 42x 404 + 1 parked; FB intro/IG handle stems (tasteaboba, tasteaboballc) all covered.
