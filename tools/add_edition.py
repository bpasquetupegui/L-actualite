#!/usr/bin/env python3
"""Ajoute (ou remplace) une édition du journal L'Actualité.

Usage : python3 tools/add_edition.py chemin/vers/edition.json

Le fichier d'entrée contient :
{
  "edition": {date, une, tldr, chiffres, chiffres_note, agenda, items},
  "articles": {"<id>": {...}, ...}
}
Voir tools/FORMAT.md pour le détail des champs.
Les éditions précédentes ne sont jamais supprimées.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
RUBS = {"France", "Europe", "Amérique du Nord", "Amérique du Sud", "Afrique", "Asie & Moyen-Orient", "Deals & buy-side"}

def fail(msg):
    sys.exit("ERREUR : " + msg)

src = json.load(open(sys.argv[1], encoding="utf-8"))
ed, arts = src.get("edition"), src.get("articles")
if not ed or not isinstance(arts, dict):
    fail("il faut les clés 'edition' et 'articles'")
date = ed.get("date", "")
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
    fail("date invalide (AAAA-MM-JJ attendu)")
ids = set()
for it in ed.get("items", []):
    i = it.get("id", "")
    if not re.fullmatch(date + r"-[a-z0-9-]{2,60}", i):
        fail(f"id invalide : {i!r} (attendu {date}-slug en minuscules ASCII)")
    if i in ids:
        fail(f"id en double : {i}")
    ids.add(i)
    for k in ("t", "c", "r", "s"):
        if not it.get(k):
            fail(f"champ '{k}' manquant pour {i}")
    if it["r"] not in RUBS:
        fail(f"rubrique inconnue pour {i} : {it['r']}")
    if i not in arts:
        fail(f"article détaillé manquant pour {i}")
    a = arts[i]
    if not (a.get("corps") or a.get("deal")):
        fail(f"article {i} sans 'corps' ni 'deal'")
    for s in a.get("sources", []):
        if not str(s.get("u", "")).startswith("http"):
            fail(f"source sans URL valide dans {i}")
if not ids:
    fail("aucun article dans l'édition")
for k in [ed.get("une")] + list(ed.get("tldr", [])):
    if k and k not in ids:
        fail(f"une/tldr référence un id inconnu : {k}")

os.makedirs(os.path.join(DATA, "editions"), exist_ok=True)
idx_path = os.path.join(DATA, "index.json")
idx = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {"editions": []}
idx["editions"] = [e for e in idx["editions"] if e.get("date") != date] + [ed]
idx["editions"].sort(key=lambda e: e["date"], reverse=True)
json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump({"date": date, "articles": arts}, open(os.path.join(DATA, "editions", date + ".json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"OK : édition {date}, {len(ids)} articles, {len(idx['editions'])} éditions au total")
