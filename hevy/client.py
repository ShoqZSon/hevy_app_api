"""HTTP-Zugriff auf die Hevy-API. Kennt weder Dateisystem noch Darstellung."""

from __future__ import annotations

from typing import Any, Iterator

import requests

from .config import Settings


class HevyClient:
    def __init__(self, settings: Settings, session: requests.Session | None = None):
        self._base_url = settings.base_url
        self._session = session or requests.Session()
        self._session.headers.update({
            "api-key": settings.api_key,
            "Content-Type": "application/json",
        })

    # ---------- intern ----------
    def _get(self, path: str, **params: Any) -> dict:
        response = self._session.get(f"{self._base_url}/{path}", params=params or None)
        response.raise_for_status()
        return response.json()

    def _paginate(self, path: str, key: str, page_size: int = 10) -> Iterator[dict]:
        """Läuft über alle Seiten einer Listen-Ressource."""
        page = 1
        while True:
            payload = self._get(path, page=page, pageSize=page_size)
            yield from payload.get(key, [])
            if page >= payload.get("page_count", 1):
                return
            page += 1

    # ---------- Ressourcen ----------
    def workout_count(self) -> int:
        return self._get("workouts/count")["workout_count"]

    def workouts(self, page: int = 1, page_size: int = 5) -> dict:
        return self._get("workouts", page=page, pageSize=page_size)

    def workout(self, workout_id: str) -> dict:
        return self._get(f"workouts/{workout_id}")

    def routines(self, page_size: int = 10) -> list[dict]:
        return list(self._paginate("routines", "routines", page_size))

    def routine(self, routine_id: str) -> dict:
        return self._get(f"routines/{routine_id}")

    def routine_folders(self, page_size: int = 10) -> list[dict]:
        return list(self._paginate("routine_folders", "routine_folders", page_size))

    def exercise_templates(self, page_size: int = 10) -> list[dict]:
        return list(self._paginate("exercise_templates", "exercise_templates", page_size))

    def exercise_history(self, template_id: str,
                         start_date: str | None = None,
                         end_date: str | None = None) -> dict:
        if bool(start_date) != bool(end_date):
            raise ValueError("start_date und end_date nur gemeinsam oder gar nicht.")
        params = {"exerciseTemplateId": template_id}
        if start_date:
            params |= {"start_date": start_date, "end_date": end_date}
        return self._get("exercise_history", **params)