"""Make an offline, dependency-free HTML report from pytest's JUnit XML."""
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "reports" / "results.xml"
DST = ROOT / "reports" / "report.html"
if not SRC.exists():
    print(f"No JUnit XML found: {SRC}. Run pytest first.")
    raise SystemExit(0)

root = ET.parse(SRC).getroot()
cases = root.findall(".//testcase")
rows = []
counts = Counter()
for case in cases:
    status = "PASSED"
    fail = case.find("failure")
    err = case.find("error")
    skip = case.find("skipped")
    if fail is not None or err is not None:
        status = "FAILED"
    elif skip is not None:
        status = "SKIPPED"
    counts[status] += 1
    label = escape(case.attrib.get("name", ""))
    classname = escape(case.attrib.get("classname", ""))
    details = escape(((fail if fail is not None else err).text or "")[:2000]) if fail is not None or err is not None else ""
    rows.append(f'<tr><td>{classname}</td><td>{label}</td><td><span class="{status.lower()}">{status}</span></td><td><pre>{details}</pre></td></tr>')

html_doc = f'''<!doctype html><html lang="fr"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>ReturnGuard AI — Test report</title>
<style>
:root{{--navy:#10224a;--blue:#1d67ab;--gray:#e8edf5}}
body{{font:15px/1.5 system-ui,Arial,sans-serif;background:#f5f8fd;color:#1e2942;margin:0}}
header{{background:linear-gradient(110deg,#152d60,#2075ac);color:white;padding:42px max(5vw,24px)}}
main{{max-width:1200px;margin:auto;padding:26px 20px}}
.stats{{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}}
.stat{{background:white;box-shadow:0 4px 18px #1a315010;border-radius:12px;padding:16px 28px;min-width:100px}}
.stat strong{{display:block;font-size:30px}}
table{{width:100%;background:white;border-collapse:collapse;border-radius:12px;overflow:hidden}}
th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid var(--gray);vertical-align:top}}
th{{background:#ebf2fc}}pre{{white-space:pre-wrap;max-width:450px;font-size:12px}}
.passed{{color:#098552;font-weight:bold}}.failed{{color:#b02b35;font-weight:bold}}.skipped{{color:#a5701d;font-weight:bold}}
small{{opacity:.85}}@media(max-width:680px){{table{{font-size:12px}}th,td{{padding:7px}}}}
</style></head><body><header><h1>ReturnGuard AI</h1><h2>Rapport des tests métiers automatisés</h2>
<small>Généré le {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} · Pytest / JUnit</small></header>
<main><section class="stats"><div class="stat"><strong>{len(cases)}</strong>Cas exécutés</div>
<div class="stat"><strong>{counts['PASSED']}</strong>Réussis</div>
<div class="stat"><strong>{counts['FAILED']}</strong>Échoués</div>
<div class="stat"><strong>{counts['SKIPPED']}</strong>Ignorés</div></section>
<p>Le rapport récapitule la décision métier, les contrôles de conformité et les tests du workflow.</p>
<table><thead><tr><th>Groupe</th><th>Cas</th><th>Statut</th><th>Détails</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></main></body></html>'''
DST.write_text(html_doc, encoding="utf-8")
print(f"HTML report saved to {DST} ({len(cases)} tests)")
