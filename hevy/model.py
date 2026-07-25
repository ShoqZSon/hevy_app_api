"""
Domänenmodell. Übersetzt das Hevy-JSON in Objekte und leitet alles ab,
was die Darstellung braucht. Keine I/O, kein HTML.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

WORK_SECONDS_PER_SET = 45  # Annahme für die Dauerschätzung


def _range(values: list[float], unit: str = "") -> str:
    """'10' oder '9–13' aus einer Werteliste."""
    if not values:
        return ""
    low, high = min(values), max(values)
    return (f"{low:g}" if low == high else f"{low:g}–{high:g}") + unit


@dataclass
class Exercise:
    position: int
    name: str
    sets: int
    notes: str
    rest: int
    summary: str          # z.B. "4×8–10 · 30–32.5 kg"
    has_numbers: bool     # False = Hevy hat keine Wdh/Gewichte gespeichert
    group: str | None = None   # Superset-Kennung A, B, C …

    @classmethod
    def from_raw(cls, raw: dict, position: int, group: str | None) -> "Exercise":
        sets = raw.get("sets", [])
        summary, has_numbers = cls._summarize(sets)
        return cls(
            position=position,
            name=raw.get("title", "?"),
            sets=len(sets),
            notes=(raw.get("notes") or "").strip().replace("\n", " · "),
            rest=raw.get("rest_seconds") or 0,
            summary=summary,
            has_numbers=has_numbers,
            group=group,
        )

    @staticmethod
    def _summarize(sets: list[dict]) -> tuple[str, bool]:
        def values(key):
            return [s[key] for s in sets if s.get(key) is not None]

        reps, weights = values("reps"), values("weight_kg")
        seconds, meters = values("duration_seconds"), values("distance_meters")

        if reps:
            head = f"{len(sets)}×{_range(reps)}"
        elif seconds:
            head = f"{len(sets)}×{_range(seconds, ' s')}"
        elif meters:
            head = f"{len(sets)}×{_range(meters, ' m')}"
        else:
            return f"{len(sets)} Sätze", False

        return head + (f" · {_range(weights, ' kg')}" if weights else ""), True

    def as_dict(self) -> dict:
        return {"pos": self.position, "group": self.group, "name": self.name,
                "sets": self.sets, "summary": self.summary,
                "numbers": self.has_numbers, "notes": self.notes, "rest": self.rest}


@dataclass
class Routine:
    title: str
    exercises: list[Exercise] = field(default_factory=list)

    @classmethod
    def from_raw(cls, raw: dict) -> "Routine":
        raw_exercises = raw.get("exercises", [])
        groups = cls._superset_labels(raw_exercises)
        return cls(
            title=raw.get("title", "?"),
            exercises=[Exercise.from_raw(e, i, groups.get(e.get("superset_id")))
                       for i, e in enumerate(raw_exercises, start=1)],
        )

    @staticmethod
    def _superset_labels(raw_exercises: list[dict]) -> dict[int, str]:
        """superset_id -> 'A', 'B', … in Reihenfolge des ersten Auftretens."""
        order: list[int] = []
        for e in raw_exercises:
            sid = e.get("superset_id")
            if sid is not None and sid not in order:
                order.append(sid)
        return {sid: chr(ord("A") + i) for i, sid in enumerate(order)}

    @property
    def total_sets(self) -> int:
        return sum(e.sets for e in self.exercises)

    @property
    def minutes(self) -> int:
        seconds = sum(e.sets * (e.rest + WORK_SECONDS_PER_SET) for e in self.exercises)
        return round(seconds / 60)

    @property
    def average_rest(self) -> int:
        rests = [e.rest for e in self.exercises if e.rest]
        return round(sum(rests) / len(rests)) if rests else 0

    def as_dict(self) -> dict:
        return {"title": self.title, "sets": self.total_sets, "minutes": self.minutes,
                "rest": self.average_rest,
                "exercises": [e.as_dict() for e in self.exercises]}


@dataclass
class Phase:
    name: str          # "Off-Season"
    focus: str         # "Hypertrophy"
    span: str          # "September - February"
    weeks: int         # 24, 0 wenn im Titel nichts steht
    routines: list[Routine] = field(default_factory=list)

    @classmethod
    def from_raw(cls, folder: dict) -> "Phase":
        title = folder.get("title", "?")
        name, _, subtitle = title.partition(":")
        weeks = re.search(r"(\d+)\s*Weeks", title, re.I)
        span = re.match(r"\s*([^(]+?)\s*(?:\(|$)", subtitle.split("--")[-1])
        return cls(
            name=name.strip(),
            focus=subtitle.split("--")[0].strip() if "--" in subtitle else subtitle.strip(),
            span=span.group(1).strip() if span and "--" in subtitle else "",
            weeks=int(weeks.group(1)) if weeks else 0,
            routines=[Routine.from_raw(r) for r in folder.get("routines", [])],
        )

    def as_dict(self) -> dict:
        return {"name": self.name, "focus": self.focus, "span": self.span,
                "weeks": self.weeks, "routines": [r.as_dict() for r in self.routines]}


@dataclass
class Plan:
    phases: list[Phase] = field(default_factory=list)

    @classmethod
    def from_folders(cls, folders: list[dict]) -> "Plan":
        return cls(phases=[Phase.from_raw(f) for f in folders])

    def __bool__(self) -> bool:
        return bool(self.phases)

    def as_dict(self) -> dict:
        return {"phases": [p.as_dict() for p in self.phases]}