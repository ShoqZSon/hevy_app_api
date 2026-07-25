"""
Darstellung: Modell -> eigenständige HTML-Datei.
Kennt die API nicht und liest nichts außer den eigenen Assets.
"""

from __future__ import annotations

import json
from pathlib import Path

from hevy.model import Plan

ASSETS = Path(__file__).parent / "assets"


def render(plan: Plan) -> str:
    """Baut das vollständige HTML-Dokument als String."""
    template = (ASSETS / "template.html").read_text(encoding="utf-8")
    styles = (ASSETS / "styles.css").read_text(encoding="utf-8")
    script = (ASSETS / "app.js").read_text(encoding="utf-8")

    script = script.replace("__DATA__", json.dumps(plan.as_dict(), ensure_ascii=False))
    return template.replace("/*__CSS__*/", styles).replace("/*__JS__*/", script)


def write(plan: Plan, target: Path) -> Path:
    target.write_text(render(plan), encoding="utf-8")
    return target