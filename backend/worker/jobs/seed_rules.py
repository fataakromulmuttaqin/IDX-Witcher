"""Isi tabel watchlists dari rules/watchlists.yaml.

Wajib dijalankan sebelum run_rules karena watchlist_members punya foreign key ke watchlists.
"""
from sqlalchemy import text

from core.db import SessionLocal
from core.rules import load_rules


def run() -> dict:
    with SessionLocal() as s:
        for i, r in enumerate(load_rules("watchlists")):
            s.execute(text("""
                INSERT INTO watchlists (slug, name, description, rule_expr, sort_order)
                VALUES (:slug, :name, :desc, :expr, :ord)
                ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name,
                  description = EXCLUDED.description, rule_expr = EXCLUDED.rule_expr,
                  sort_order = EXCLUDED.sort_order"""),
                {"slug": r["slug"], "name": r["name"], "desc": r["description"],
                 "expr": " ".join(r["expr"].split()), "ord": i})
        s.commit()
    return {"status": "ok", "rows": len(load_rules("watchlists"))}
