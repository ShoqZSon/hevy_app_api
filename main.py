"""
Einstiegspunkt. Verdrahtet die Bausteine, enthält selbst keine Logik.

    python main.py sync      # Hevy-API  -> plans/*.json
    python main.py report    # plans/    -> trainingsplan.html (öffnet den Browser)
    python main.py all       # beides
"""

from __future__ import annotations

import argparse
import webbrowser
from pathlib import Path

from hevy import HevyClient, PlanRepository, Plan, Settings
import report
from hevy.sync import sync


def run_sync(root: Path) -> None:
    settings = Settings.from_env(root)
    folders = sync(HevyClient(settings), PlanRepository(settings.plans_dir))
    print(f"{len(folders)} Pläne synchronisiert nach {settings.plans_dir}")


def run_report(root: Path, open_browser: bool) -> None:
    repository = PlanRepository(root / "plans")
    plan = Plan.from_folders(repository.load_all(extra_dirs=[root]))
    if not plan:
        raise SystemExit(f"Keine Pläne gefunden. Erst 'python main.py sync' laufen lassen.")

    target = report.write(plan, root / "trainingsplan.html")
    print(f"{len(plan.phases)} Phasen geschrieben nach {target}")
    if open_browser:
        webbrowser.open(target.resolve().as_uri())


def main() -> None:
    parser = argparse.ArgumentParser(description="Hevy-Trainingspläne synchronisieren und anzeigen.")
    parser.add_argument("command", choices=["sync", "report", "all"], nargs="?", default="all")
    parser.add_argument("--no-open", action="store_true", help="Browser nicht öffnen")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Projektverzeichnis")
    args = parser.parse_args()

    if args.command in ("sync", "all"):
        run_sync(args.root)
    if args.command in ("report", "all"):
        run_report(args.root, open_browser=not args.no_open)


if __name__ == "__main__":
    main()