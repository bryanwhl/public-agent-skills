#!/usr/bin/env python3
"""Perform fast structural and safety checks on a rendered learning deck."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class Inspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.hrefs: list[str] = []
        self.errors: list[str] = []
        self.term_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)
        values = dict(attrs)
        if "id" in values and values["id"]:
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")
        if values.get("class") and "term" in values["class"].split():
            self.term_count += 1
            if not values.get("data-definition"):
                self.errors.append("Term button is missing data-definition")
        if any(name.lower().startswith("on") for name, _ in attrs):
            self.errors.append(f"Inline event handler found on <{tag}>")
        if tag in {"script", "link"} and values.get("src"):
            self.errors.append(f"Remote or external dependency found on <{tag}>")
        if tag == "link" and values.get("href"):
            self.errors.append("External stylesheet/link dependency found")


def validate(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    parser = Inspector()
    parser.feed(text)
    errors = list(parser.errors)
    for required in ("title", "nav", "main", "section", "details", "dialog", "script"):
        if required not in parser.tags:
            errors.append(f"Missing required <{required}> element")
    if parser.term_count == 0:
        errors.append("No interactive jargon terms found")
    if "TODO" in text or re.search(r"\{\{[A-Z_]+\}\}", text):
        errors.append("Placeholder text remains")
    for href in parser.hrefs:
        if href.startswith("#") and href[1:] not in parser.ids:
            errors.append(f"Broken internal link: {href}")
        elif not href.startswith("#"):
            parsed = urlparse(href)
            if parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"Unsafe external URL: {href}")
    if not re.search(r'class="cite"', text):
        errors.append("No inline citations found")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("deck", type=Path)
    args = parser.parse_args()
    path = args.deck.expanduser().resolve()
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Deck validation passed: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
