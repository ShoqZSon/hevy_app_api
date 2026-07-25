"""
Ablauf: holt die Daten über den Client, verheiratet Routinen mit ihren
Ordnern und übergibt sie dem Repository. Die einzige Stelle, die beides kennt.
"""

from __future__ import annotations

from .client import HevyClient
from .repository import PlanRepository


def fetch_folders(client: HevyClient) -> list[dict]:
    """Alle Ordner samt der zugehörigen Routinen — ein Durchlauf, nicht fünf."""
    routines = client.routines()
    folders = client.routine_folders()
    for folder in folders:
        folder["routines"] = [r for r in routines if r.get("folder_id") == folder.get("id")]
    return folders


def sync(client: HevyClient, repository: PlanRepository, split: bool = True) -> list[dict]:
    folders = fetch_folders(client)
    repository.save_all(folders)
    if split:
        repository.save_each(folders)
    return folders