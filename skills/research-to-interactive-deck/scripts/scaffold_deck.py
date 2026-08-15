#!/usr/bin/env python3
"""Create a safe starter research.json for an interactive learning deck."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:60].strip("-")
    return slug or "topic"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", default="a motivated beginner")
    parser.add_argument("--output-root", type=Path, default=Path("~/Projects/personal"))
    args = parser.parse_args()

    root = args.output_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / f"{slugify(args.topic)}-learning-deck"
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {output}")
    output.mkdir(exist_ok=True)

    data = {
        "topic": args.topic,
        "subtitle": "TODO: one-sentence promise for the learner",
        "audience": args.audience,
        "updated": date.today().isoformat(),
        "objectives": ["TODO: learner outcome"],
        "sections": [
            {
                "id": "why-it-matters",
                "kicker": "Orientation",
                "title": "Why it matters",
                "summary": "TODO: concise explanation",
                "points": [{"text": "TODO: source-grounded point", "sources": ["S1"]}],
                "deep_dive": "TODO: optional detail",
                "terms": [{"term": "TODO term", "definition": "TODO plain-language definition"}],
            }
        ],
        "knowledge_check": [{"question": "TODO: check understanding", "answer": "TODO: answer"}],
        "sources": [
            {
                "id": "S1",
                "title": "TODO: source title",
                "publisher": "TODO: publisher",
                "published": "TODO or n.d.",
                "accessed": date.today().isoformat(),
                "url": "https://example.com/direct-source",
            }
        ],
    }
    path = output / "research.json"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
