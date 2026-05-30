"""
Logica di business per il Conference Buddy.

Funzioni pure: prendono dati, restituiscono dati.
Nessun decoratore, nessuna dipendenza da framework, nessuna serializzazione.
"""

import json
from pathlib import Path

SCHEDULE_PATH = Path(__file__).parent.parent / "data" / "schedule.json"
SCHEDULE: list[dict] = json.loads(SCHEDULE_PATH.read_text())


def search_talks(
    query: str = "",
    day: str | None = None,
    level: str | None = None,
    language: str | None = None,
    tag: str | None = None,
) -> str:
    """Cerca talk, workshop e keynote nel programma della PyCon Italia 2026.

    Args:
        query: Testo da cercare nel titolo o nell'abstract. Può essere vuoto per filtrare solo per criteri.
        day: Filtra per giorno (formato YYYY-MM-DD). Giorni: 2026-05-27 (Open Day), 05-28 e 05-29 (conferenza), 05-30 (sprint/workshop).
        level: Filtra per livello: "Beginner", "Intermediate", "Advanced".
        language: Filtra per lingua: "it" o "en".
        tag: Filtra per tag (es. "ML and AI", "Web Frameworks", "Testing", "DevOps and SRE", "Data Engineering").
    """
    results = []

    for event in SCHEDULE:
        if event["type"] not in ("talk", "training", "keynote"):
            continue

        if query:
            text = f"{event.get('title', '')} {event.get('abstract', '')}".lower()
            if query.lower() not in text:
                continue

        if day and event.get("day") != day:
            continue
        if level and event.get("audience_level") != level:
            continue
        if language and event.get("language") != language:
            continue
        if tag and tag not in event.get("tags", []):
            continue

        results.append(
            {
                "title": event["title"],
                "type": event["type"],
                "day": event["day"],
                "start": event["start"],
                "end": event["end"],
                "duration_minutes": event["duration_minutes"],
                "rooms": event["rooms"],
                "speakers": [s["name"] for s in event.get("speakers", [])],
                "level": event.get("audience_level"),
                "language": event.get("language"),
                "tags": event.get("tags", []),
                "abstract": (event.get("abstract") or "")[:200] + "...",
                "url": event.get("url"),
            }
        )

    if not results:
        return json.dumps(
            {"results": [], "message": "Nessun risultato trovato."}, ensure_ascii=False
        )

    return json.dumps(
        {
            "results": results[:10],
            "total": len(results),
            "showing": min(10, len(results)),
        },
        indent=2,
        ensure_ascii=False,
    )


def suggest_schedule(
    interests: str,
    day: str | None = None,
    language: str | None = None,
) -> str:
    """Suggerisce un percorso di talk per la giornata, evitando sovrapposizioni.

    Args:
        interests: Interessi dell'utente separati da virgola (es. "machine learning, testing, web").
        day: Giorno specifico (formato YYYY-MM-DD). Se omesso, considera tutti i giorni.
        language: Preferenza lingua: "it", "en", o None per entrambe.
    """
    interest_list = [i.strip().lower() for i in interests.split(",")]

    candidates = []
    for event in SCHEDULE:
        if event["type"] not in ("talk", "training", "keynote"):
            continue
        if day and event.get("day") != day:
            continue
        if language and event.get("language") != language:
            continue

        text = f"{event.get('title', '')} {event.get('abstract', '')} {' '.join(event.get('tags', []))}".lower()
        score = sum(1 for interest in interest_list if interest in text)

        if score > 0:
            candidates.append(
                {
                    "title": event["title"],
                    "type": event["type"],
                    "start": event["start"],
                    "end": event["end"],
                    "rooms": event["rooms"],
                    "speakers": [s["name"] for s in event.get("speakers", [])],
                    "score": score,
                    "matching_interests": [i for i in interest_list if i in text],
                    "url": event.get("url"),
                }
            )

    candidates.sort(key=lambda x: (-x["score"], x["start"]))

    schedule = []
    occupied_slots = []

    for c in candidates:
        start, end = c["start"], c["end"]
        overlaps = any(not (end <= s or start >= e) for s, e in occupied_slots)
        if not overlaps:
            schedule.append(c)
            occupied_slots.append((start, end))

    schedule.sort(key=lambda x: x["start"])

    return json.dumps(
        {
            "schedule": schedule,
            "total_events": len(schedule),
        },
        indent=2,
        ensure_ascii=False,
    )


def speaker_info(name: str) -> str:
    """Cerca informazioni su uno speaker della PyCon Italia 2026.

    Args:
        name: Nome (o parte del nome) dello speaker da cercare.
    """
    name_lower = name.lower()
    speaker_talks: dict[str, dict] = {}

    for event in SCHEDULE:
        for speaker in event.get("speakers", []):
            if name_lower in speaker["name"].lower():
                speaker_name = speaker["name"]
                if speaker_name not in speaker_talks:
                    speaker_talks[speaker_name] = {
                        "name": speaker_name,
                        "photo": speaker.get("photo"),
                        "talks": [],
                        "bio": speaker.get("bio"),
                        "social": speaker.get("social"),
                    }
                speaker_talks[speaker_name]["talks"].append(
                    {
                        "title": event["title"],
                        "type": event["type"],
                        "day": event["day"],
                        "start": event["start"],
                        "rooms": event["rooms"],
                        "level": event.get("audience_level"),
                        "url": event.get("url"),
                    }
                )

    if not speaker_talks:
        return json.dumps(
            {"message": f"Nessuno speaker trovato con nome '{name}'."},
            ensure_ascii=False,
        )

    return json.dumps(list(speaker_talks.values()), indent=2, ensure_ascii=False)
