"""Persistenz: liest und schreibt die Plan-JSONs. Kennt die API nicht."""

from __future__ import annotations

import json
from difflib import get_close_matches
from pathlib import Path

ALL_PLANS_FILE = "plans.json"


class PlanRepository:
    def __init__(self, plans_dir: Path):
        self.plans_dir = plans_dir

    # ---------- schreiben ----------
    def save_all(self, folders: list[dict]) -> Path:
        return self._write(ALL_PLANS_FILE, {"routine_folders": folders})

    def save_each(self, folders: list[dict]) -> list[Path]:
        return [self._write(f"{self.short_name(f)}.json", f) for f in folders]

    def _write(self, filename: str, payload: dict) -> Path:
        self.plans_dir.mkdir(parents=True, exist_ok=True)
        path = self.plans_dir / filename
        path.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")
        return path

    # ---------- lesen ----------
    def load_all(self, extra_dirs: list[Path] | None = None) -> list[dict]:
        """
        Sammelt Plan-Ordner aus allen *.json der Verzeichnisse und entfernt
        Duplikate über die id. Versteht plans.json und die Einzeldateien.
        """
        folders: dict[int, dict] = {}
        for directory in [self.plans_dir, *(extra_dirs or [])]:
            if not directory.is_dir():
                continue
            for file in sorted(directory.glob("*.json")):
                for folder in self._folders_in(file):
                    folders.setdefault(folder.get("id"), folder)
        return sorted(folders.values(), key=lambda f: f.get("index", 0))

    @staticmethod
    def _folders_in(file: Path) -> list[dict]:
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return []
        if not isinstance(data, dict):
            return []
        folders = data.get("routine_folders")
        if folders is None:
            folders = [data] if "routines" in data else []
        return [f for f in folders if isinstance(f, dict)]

    # ---------- suchen ----------
    @staticmethod
    def short_name(folder: dict) -> str:
        """'Off-Season: Hypertrophy -- ...' -> 'Off-Season'"""
        return folder.get("title", "unbenannt").split(":")[0].strip()

    def find(self, name: str, folders: list[dict] | None = None) -> dict:
        folders = folders if folders is not None else self.load_all()
        names = [self.short_name(f).lower() for f in folders]
        matches = get_close_matches(name.lower(), names, n=1, cutoff=0.3)
        if not matches:
            raise ValueError(
                f"Kein Plan passt zu '{name}'. Vorhanden: {[self.short_name(f) for f in folders]}")
        return folders[names.index(matches[0])]