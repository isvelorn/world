#!/usr/bin/env python3
"""Small deterministic foundation validator; Python 3.8+, standard library only.

This checks the current minimal canon. JSON Schema lives in schemas/; this
script is NOT a generic JSON Schema interpreter or balance test.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    ("element.water", "Вода", "💙"),
    ("element.earth", "Земля", "🤎"),
    ("element.fire", "Огонь", "❤️"),
    ("element.air", "Воздух", "🤍"),
    ("element.nature", "Природа", "💚"),
    ("element.electricity", "Электричество", "🩷"),
    ("element.light", "Свет", "💛"),
    ("element.darkness", "Тьма", "🖤"),
    ("element.sound", "Звук", "🩶"),
]


def main():
    data = json.loads((ROOT / "data/elements.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/elements.schema.json").read_text(encoding="utf-8"))
    assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
    assert data["schema_version"] == 1
    assert data["status"] == "partial-canon"
    items = data["elements"]
    assert len(items) == 9, "Exactly nine elements are canon"
    observed = []
    for item in items:
        assert item["status"] == "canon"
        observed.append((item["id"], item["name_ru"], item["symbol"]))
    assert observed == EXPECTED, "Element order, names, and symbols changed without a canon decision"
    assert len({e["id"] for e in items}) == len(items), "Duplicate element ID"
    darkness = next(e for e in items if e["id"] == "element.darkness")
    assert "not absence of light" in darkness.get("note", "")
    proposed = data["proposed_elements"]
    assert any(e["id"] == "element.cold" and e["status"] == "proposed" for e in proposed)
    assert not ({e["id"] for e in proposed} & {e["id"] for e in items})
    print("PASS: ISVELORN minimal magic canon and JSON syntax")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError) as exc:
        print("FAIL:", str(exc), file=sys.stderr)
        sys.exit(1)
