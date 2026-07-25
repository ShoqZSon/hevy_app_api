"""Konfiguration. Einzige Stelle, die os.environ und .env kennt."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    plans_dir: Path
    output_file: Path

    @classmethod
    def from_env(cls, root: Path | None = None) -> "Settings":
        load_dotenv()
        api_key, base_url = os.getenv("API_KEY"), os.getenv("BASE_URL")
        if not api_key or not base_url:
            raise EnvironmentError("API_KEY und BASE_URL müssen in .env gesetzt sein.")

        root = root or Path.cwd()
        return cls(
            api_key=api_key,
            base_url=base_url.rstrip("/"),
            plans_dir=root / "plans",
            output_file=root / "trainingsplan.html",
        )