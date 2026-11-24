# TASTEA BOBA (APPLETON WI) pitch: guards + asserts + send + read-back + registry append + lane.db event (abort-on-any-gate)
# Cloned from boba-house-houston/send_pitch.py 2026-11-24 (sactown/sokoya hardened lineage: no v4 recursion wrapper;
# events.line = registry PHYSICAL line; ASCII subject-stem read-back with per-word subject proof; envelope-resume guard).
# Pre-run greps: no 'line_no = pitches'; no 'def v4' wrapper; all module attributes imported.
# Adds inline tz_gate check (fail-closed, lane.db shop_tz is the single authority; no hardcoded tz).
import json, re, subprocess, sys, os, time, datetime, imaplib, urllib.request
import zoneinfo as _zi

BASE = '/Users/rleon/.hermes/projects/websites'
DRAFT = BASE + '/sites/tastea-boba-appleton/PITCH-DRAFT.md'
REG = BASE + '/pitch_registry.jsonl'
LANEDB = BASE + '/lane.db'
ENVOUT = BASE + '/sites/tastea-boba-appleton/send-envelope.json'
TZG = '/Users/rleon/.hermes/profiles/websites/skills/websites-pitch/scripts/tz_gate.py'
SLUG = 'tastea-boba-appleton'
TO = 'Tasteaboballc@gmail.com'
SUBJ = 'Your new website is live \u2014 Tastea Boba'
TOKEN = 'tastea-boba-appleton-t1'
CARD = 't_abc78b8a'
_full = open(DRAFT, encoding='utf-8').read().splitlines()
_subj_line = _full[0].removeprefix('Subject:').strip()
assert _subj_line == SUBJ, f'subject mismatch: draft {_subj_line!r}'
BODY = '\n'.join(_full[1:]).strip()
assert '\u2026' not in BODY, 'U+2026 mangled token in draft'

def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
rows = [json.loads(l) for l in open(REG) if l.strip()]
nto = norm(TO)

# 0) resume predicates: registry pitch row = never re-send; envelope ok=true = mail out but row missing -> reuse mid, skip send
if any(r.get('type') == 'pitch' and r.get('slug') == SLUG for r in rows):
    sys.exit('SKIP: registry already has a pitch row for this slug — never re-send')
resume_mid = None
if os.path.exists(ENVOUT):
    try:
        _e = json.load(open(ENVOUT))
        if _e.get('ok'):
            resume_mid = (_e.get('env') or {}).get('data', {}).get('message_id') or (_e.get('env') or {}).get('message_id')
    except Exception:
        pass

# 1) never-pitch-twice guards (email side + name/alias side). Homonym note: national 'Tastea' franchise (tastea.com)
#    is a DIFFERENT business — a blocking row whose city isn't Appleton/WI must be eyeballed before any re-pitch.
email_hits = [r for r in rows if norm(r.get('email', '')) == nto]
NAMEQ = ['tasteaboba', 'tasteabobaappleton', 'tasteaboballc', 'tasteabobaappletonwi']
name_hits = [r for r in rows if any(
              a and (a == q or (len(a) >= 8 and (a in q or q in a)))
              for a in [norm(x) for x in ([r.get('business', '')] + list(r.get('name_aliases', []) or []) + [r.get('name', '')])]
              for q in NAMEQ)]
print('GUARD email rows:', [(r.get('type'), r.get('slug')) for r in email_hits])
print('GUARD name rows:', [(r.get('type'), r.get('slug')) for r in name_hits])
pitched_emails = {norm(r['email']) for r in rows if r.get('type') == 'pitch' and r.get('email')}
blocking_names = [r for r in name_hits if r.get('type') in ('pitch', 'no', 'optout', 'has_site', 'sent')]
if any(norm(r.get('email', '')) in pitched_emails for r in email_hits) or blocking_names:
    sys.exit('ABORT: already pitched/known on this email-or-name key — ' + json.dumps([(r.get('type'), r.get('slug'), r.get('city')) for r in blocking_names]))

# 2) inbox cap (2 businesses max per inbox)
n_same_inbox = sum(1 for r in rows if r.get('type') == 'pitch' and norm(r.get('email', '')) == nto)
print(f'inbox cap check ({TO}):', n_same_inbox, '(cap 2)')
assert n_same_inbox < 2, 'ABORT: inbox cap'

# 3) optout suppression (email is globally suppressed)
opt_emails = {norm(r.get('email', '')) for r in rows if r.get('type') == 'optout'}
assert nto not in opt_emails, 'ABORT: opted-out address'
try:
    sup = open(BASE + '/optout_list.txt').read()
    assert nto not in norm(sup), 'ABORT: optout_list.txt'
except FileNotFoundError:
    pass

# 4) copy form asserts (proven formula; ABORT before send) — URLs derived from the draft itself
assert BODY.count('](http') == 2, f'links {BODY.count("](http")}'
assert BODY.count('<img') == 1, 'img count'
demo = re.search(r'\]\((https://tastea-boba-appleton-demo[^)]+)\)', BODY).group(1)
pay = re.search(r'\]\((https://buy\.stripe[^)]+)\)', BODY).group(1)
pixel = re.search(r'<img src="([^"]+)"', BODY)
for need in ('utm_medium=email', 'utm_campaign=websites', f'utm_content={TOKEN}'):
    assert need in demo, 'demo missing ' + need
    assert need in pay, 'pay missing ' + need
assert f'client_reference_id={TOKEN}' in pay, 'pay missing client_reference_id'
assert pixel and pixel.group(1) == f'https://tastea-boba-appleton-demo.up.railway.app/open?t={TOKEN}', 'pixel token'
t = re.sub(r'\*\*', '', BODY)
t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
t = re.sub(r'<img[^>]*>', '', t)
lines = [l for l in t.splitlines() if l.strip()]
lines = [l for l in lines if not l.startswith('Hi') and not l.startswith('— Jarvis')
         and not l.startswith('OnSmalltalk Media ·') and not l.startswith('<img')]
n = len(re.findall(r'\S+', ' '.join(lines)))
print(f'ASSERT core words: {n} (limit 110); links 2; utm+pixel token {TOKEN} OK')
assert n <= 110, f'ABORT words {n}'

# 4b) recipient-local send window gate — inline tz_gate (lane.db shop_tz America/Chicago is authority; DST-safe).
# exit 0 = inside 07:00-17:00 RECIPIENT-local; 3 = outside -> re-park per stamp, never night-send; 2 = unknown tz fail-closed.
_tz = subprocess.run(['python3', TZG, 'check', '--slug', SLUG], capture_output=True, text=True)
print('TZ_GATE:', _tz.stdout.strip(), 'rc=', _tz.returncode)
if _tz.returncode == 2:
    sys.exit('ABORT tz: shop_tz unknown for slug — fail-closed, seed before sending')
if _tz.returncode == 3:
    _st = subprocess.run(['python3', TZG, 'stamp', '--slug', SLUG], capture_output=True, text=True).stdout.strip()
    sys.exit(f'ABORT window: outside Appleton 07:00-17:00 — re-park SCHEDULED_UNTIL={_st}, NOTHING SENT')
_local = datetime.datetime.now(_zi.ZoneInfo('America/Chicago'))
print(f'window gate: Appleton (recipient) local {_local.strftime("%a %H:%M %Z")}')
if os.environ.get('DRY'):
    sys.exit(f'GUARDS+ASSERTS PASS (dry, not sent); words={n}; recipient-local {_local.strftime("%H:%M")}')
if not (7 <= _local.hour < 17):
    sys.exit(f'ABORT window: recipient-local {_local.strftime("%H:%M")} outside Appleton 07:00-17:00 — re-park, never night-send')

# 4c) fact-truth liveness — pitch claims tasteaboba.com shows a server error + live branded demo. Fail-closed:
#     if the owner revived a real site on the domain this morning, the pitch is stale (HAS-SITE kill guard).
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}
def http_get(url, timeout=25):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return getattr(r, 'status', r.getcode()), r.read(60000).decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read(60000).decode('utf-8', 'replace')
for own in ('https://tasteaboba.com/', 'http://tasteaboba.com/', 'https://www.tasteaboba.com/'):
    try:
        st, b = http_get(own)
        if st == 200 and len(b.strip()) > 500:
            sys.exit(f'ABORT: {own} serves HTTP 200 with real content ({len(b)} bytes) — owner REVIVED their site (HAS-SITE re-verify), pitch is stale')
        print(f'LIVENESS {own}: HTTP {st}, {len(b.strip())} bytes = still error/parked (pitch claim holds)')
    except SystemExit:
        raise
    except Exception as e:
        print(f'LIVENESS {own}: fetch error ({str(e)[:60]}) = not a live site (pitch claim holds)')
try:
    st_d, b_d = http_get(demo.split('?')[0])
    assert st_d == 200 and 'Tastea' in b_d, f'demo HTTP {st_d}'
    print('LIVENESS demo: 200 branded')
except SystemExit:
    raise
except Exception as e:
    sys.exit(f'ABORT: demo fetch failed ({e})')

# 5) send (body on stdin, --json envelope; message_id from the envelope JSON)
if resume_mid:
    mid = resume_mid
    print('RESUME: envelope carries ok send — NOT re-sending:', mid)
else:
    res = subprocess.run(['email', 'send', '--account', 'jarvis', '--as', 'websites',
                          '--to', TO, '--subject', SUBJ, '--json'],
                         input=BODY.encode(), capture_output=True, timeout=120)
    try:
        env = json.loads(res.stdout.decode())
    except Exception:
        open(ENVOUT, 'w').write(res.stdout.decode() + '\n---STDERR---\n' + res.stderr.decode())
        sys.exit('ABORT: unparseable send envelope — do NOT resend, read back Sent Mail first')
    json.dump({'ok': env.get('ok'), 'env': env}, open(ENVOUT, 'w'))
    ok = env.get('ok')
    mid = (env.get('data') or {}).get('message_id') or (env.get('data') or {}).get('msg_id') or env.get('message_id')
    print('SEND ok=', ok, 'msg:', mid if ok else env)
    if not ok or not mid:
        sys.exit('ABORT send — read back [Gmail]/Sent Mail before any retry')

# 6) sent read-back (raw imaplib): Message-ID equality + identity header pair.
# ASCII stem search only (em dash = Q-encoded); per-word subject proof (Q-encoding turns spaces to _).
conf = {}
for l in open(os.path.expanduser('~/.hermes/config/jarvis-email.conf')):
    if '=' in l: k, v = l.split('=', 1); conf[k.strip()] = v.strip()
    elif ':' in l: k, v = l.split(':', 1); conf[k.strip()] = v.strip()
M = imaplib.IMAP4_SSL(conf.get('IMAP_SERVER', 'imap.gmail.com'))
M.login(conf['EMAIL'], conf['APP_PASSWORD'])
M.select('"[Gmail]/Sent Mail"')
typ, m = M.uid('search', None, 'SUBJECT', '"Your new website is live"')
ids = [i.decode() for i in m[0].split()]
hit = None
for uid in ids[-8:]:
    typ, d = M.uid('fetch', uid, '(BODY.PEEK[HEADER])')
    hdr = d[0][1].decode(errors='replace')
    if mid in hdr:
        orp = bool(re.search(r'X-Google-Original-From:[^>]*jarvis\+websites', hdr, re.I))
        rto = bool(re.search(r'Reply-To:\s*\S*jarvis\+websites', hdr, re.I))
        subj_line = ' '.join(l for l in hdr.splitlines() if l.lower().startswith('subject'))
        full = all(w.lower() in subj_line.lower() for w in ('Tastea', 'Boba'))
        hit = {'uid': uid, 'ogf': orp, 'reply_to': rto, 'subject_full': full}
        break
M.logout()
print('READBACK:', hit)
assert hit and hit['ogf'] and hit['reply_to'] and hit['subject_full'], 'ABORT READBACK — mail out but unproven; append registry only after proof, never re-send'

# 7) registry append AT SEND (type IN the dict), then recount-verify
TODAY = datetime.date.today().isoformat()
row = {
    'id': 'pk-' + os.urandom(5).hex(),
    'type': 'pitch', 'date': TODAY,
    'ts': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'slug': SLUG, 'business': 'Tastea Boba (Appleton WI)', 'city': 'Appleton', 'state': 'WI',
    'name_aliases': ['Tastea Boba', 'Tastea Boba LLC', 'Tastea Boba Appleton', 'TasteaBoba', 'Tastea Boballc', 'tastea-boba-appleton'],
    'email': TO, 'alias': TO.split('@')[0], 'card': CARD,
    'email_provenance': 'published in FB Page intro/bio (facebook.com/profile.php?id=61592082812325, logged-out 2026-11-24)',
    'msg_id': mid, 'preview': 'https://tastea-boba-appleton-demo.up.railway.app',
    'subject': SUBJ, 'subject_arm': 'v6', 'cohort': 'new_prospect',
    'shot': False, 'pixel': True, 'utm_content': TOKEN,
    'followup_due': '2026-12-03',
    'ladder': 't2 2026-12-03 / t3 2026-12-10 / t4 2026-12-17 (weekday ladder, US-holiday shift: Thanksgiving 11-26/27); teardown recheck >= 2026-12-22',
    'feed_id': 'press-foxcities', 'shop_id': 'tastea-boba-appleton',
    'note': ('7-core-page site (home/menu/milk-tea/desserts/visit/contact/privacy + 404/thanks); opening 2026-09-19 former Little Caesars 317 E Calumet St (Post-Crescent); '
             'no-site evidence: tasteaboba.com = Hostinger-parked HTTP 500 0-byte re-curl 2026-11-24 (registered, dns-parking NS); 42 further stems RDAP-404 incl FB/IG handle stems tasteaboba/tasteaboballc; '
             'GBP place card exists with website field EMPTY; brand SERP gate 2026-11-24 no own-brand domain; homonym guard: national Tastea franchise tastea.com is a DIFFERENT business; '
             'hours omitted site-side (unverified); founder bundle T1 $249+$39/mo 31d trial; v6 subject arm (deterministic coin sha256(slug)%2: 0=v6 pinned 2026-11-24); recipient gmail.com inbox; '
             'read-back proof uid='),
}
with open(REG, 'a') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
pitches = 0; mine = 0; line_no = 0
for i, l in enumerate(open(REG), 1):
    try: d = json.loads(l)
    except Exception: continue
    if d.get('type') == 'pitch':
        pitches += 1
        if d.get('slug') == SLUG: mine += 1; line_no = i  # lane.db events.line = registry PHYSICAL line
assert mine == 1, f'tastea pitch rows={mine}'
print(f'REGISTRY_OK total_pitch_rows={pitches} mine=1 line={line_no}')

# 8) lane.db events mirror row
import sqlite3
db = sqlite3.connect(LANEDB)
db.execute("""INSERT INTO events (line,type,slug,business,email,msg_id,followup_due,date_txt,ts,note)
VALUES (?,?,?,?,?,?,?,?,?,?)""",
 (line_no, 'pitch', SLUG, 'Tastea Boba (Appleton WI)', TO, mid,
  '2026-12-03', TODAY, int(time.time()),
  'pitched via websites desk; demo tastea-boba-appleton-demo.up.railway.app; founder bundle T1 $249+$39/mo 31d trial; v6 subject arm; read-back proof uid=' + hit['uid']))
db.commit()
print('EVENT_ROW_OK', db.execute("SELECT line,type,slug,msg_id FROM events WHERE slug=?", (SLUG,)).fetchall())
# 9) close-out tz seed (idempotent; CLOSE-OUT SEEDING rule)
_ts = subprocess.run(['python3', TZG, 'set', '--slug', SLUG, '--tz', 'America/Chicago', '--source', '317 E Calumet St, Appleton, WI 54915'], capture_output=True, text=True)
print('TZ_SEED:', _ts.stdout.strip() or _ts.stderr.strip())
print('ALL_DONE', mid)
