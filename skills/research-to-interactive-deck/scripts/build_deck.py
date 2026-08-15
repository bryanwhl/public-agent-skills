#!/usr/bin/env python3
"""Render researched JSON into a safe, self-contained interactive HTML deck."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


FORMAL_PHRASES = {
    "utilize": "use",
    "facilitate": "help",
    "commence": "start",
    "terminate": "stop or end",
    "approximately": "about",
    "subsequently": "later or then",
    "prior to": "before",
    "in order to": "to",
    "due to the fact that": "because",
    "a large number of": "many",
    "at this point in time": "now",
    "with regard to": "about",
    "has the ability to": "can",
    "is able to": "can",
    "for the purpose of": "to or for",
    "in the event that": "if",
    "pertaining to": "about",
}


def learner_text(data: dict):
    """Yield labels and learner-facing prose that must use simple English."""
    yield "subtitle", data.get("subtitle", "")
    for index, objective in enumerate(data.get("objectives", []), start=1):
        yield f"objective {index}", objective
    for section_index, section in enumerate(data.get("sections", []), start=1):
        prefix = f"section {section_index}"
        yield f"{prefix} summary", section.get("summary", "")
        for point_index, point in enumerate(section.get("points", []), start=1):
            yield f"{prefix} point {point_index}", point.get("text", "")
        if section.get("deep_dive"):
            yield f"{prefix} extra detail", section["deep_dive"]
        for term_index, term in enumerate(section.get("terms", []), start=1):
            yield f"{prefix} term {term_index} definition", term.get("definition", "")
    for check_index, check in enumerate(data.get("knowledge_check", []), start=1):
        yield f"learning check {check_index} question", check.get("question", "")
        yield f"learning check {check_index} answer", check.get("answer", "")


def plain_english_issues(data: dict) -> list[str]:
    issues = []
    for label, value in learner_text(data):
        text = str(value).strip()
        lowered = text.casefold()
        for phrase, replacement in FORMAL_PHRASES.items():
            if re.search(rf"\b{re.escape(phrase)}\b", lowered):
                issues.append(f'{label}: replace "{phrase}" with "{replacement}"')
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", text):
            words = re.findall(r"\b[\w'-]+\b", sentence)
            if len(words) > 30:
                issues.append(f"{label}: sentence has {len(words)} words; split it into sentences of 30 words or fewer")
    return issues


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_id(value: object) -> str:
    result = re.sub(r"[^a-z0-9-]+", "-", str(value).lower()).strip("-")
    if not result:
        raise ValueError("Section id cannot be empty")
    return result


def safe_url(value: object) -> str:
    url = str(value)
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"Only direct HTTPS source URLs are allowed: {url}")
    return esc(url)


def require(data: dict, key: str):
    if key not in data or data[key] in (None, "", []):
        raise ValueError(f"Missing required field: {key}")
    return data[key]


def render(data: dict, template: str) -> str:
    language_issues = plain_english_issues(data)
    if language_issues:
        raise ValueError("Use simpler English:\n- " + "\n- ".join(language_issues))

    topic = require(data, "topic")
    sections = require(data, "sections")
    sources = require(data, "sources")
    source_ids = {str(require(source, "id")) for source in sources}

    objectives = "".join(f"<li>{esc(item)}</li>" for item in require(data, "objectives"))
    intro = (
        '<section class="slide" id="learning-goals">'
        '<p class="eyebrow">Start here</p><h2>What you will learn</h2>'
        f'<ul class="objectives">{objectives}</ul></section>'
    )
    nav = ['<a href="#learning-goals">Goals</a>']
    rendered_sections = [intro]

    for section in sections:
        section_id = safe_id(require(section, "id"))
        title = require(section, "title")
        nav.append(f'<a href="#{section_id}">{esc(title)}</a>')
        points = []
        for point in require(section, "points"):
            refs = point.get("sources", [])
            unknown = set(map(str, refs)) - source_ids
            if unknown:
                raise ValueError(f"Unknown source id(s) in {section_id}: {sorted(unknown)}")
            citations = "".join(
                f' <a class="cite" href="#source-{safe_id(ref)}" aria-label="Source {esc(ref)}">[{esc(ref)}]</a>'
                for ref in refs
            )
            points.append(f'<li>{esc(require(point, "text"))}{citations}</li>')
        terms = " ".join(
            f'<button class="term" type="button" data-definition="{esc(require(term, "definition"))}">{esc(require(term, "term"))}</button>'
            for term in section.get("terms", [])
        )
        deep_dive = section.get("deep_dive", "")
        details = f'<details><summary>Learn more</summary><p>{esc(deep_dive)}</p></details>' if deep_dive else ""
        glossary = f'<p><strong>Key terms:</strong> {terms}</p>' if terms else ""
        rendered_sections.append(
            f'<section class="slide" id="{section_id}">'
            f'<p class="eyebrow">{esc(section.get("kicker", "Core idea"))}</p>'
            f'<h2>{esc(title)}</h2><p class="lead">{esc(require(section, "summary"))}</p>'
            f'<ul class="points">{"".join(points)}</ul>{glossary}{details}</section>'
        )

    checks = data.get("knowledge_check", [])
    if checks:
        nav.append('<a href="#knowledge-check">Check</a>')
        questions = "".join(
            f'<details><summary>{esc(require(item, "question"))}</summary><p>{esc(require(item, "answer"))}</p></details>'
            for item in checks
        )
        rendered_sections.append(
            f'<section class="slide" id="knowledge-check"><p class="eyebrow">Quick check</p>'
            f'<h2>Check what you learned</h2>{questions}</section>'
        )

    nav.append('<a href="#sources">Sources</a>')
    source_items = []
    for source in sources:
        sid = safe_id(require(source, "id"))
        source_items.append(
            f'<li id="source-{sid}"><strong>[{esc(source["id"])}]</strong> '
            f'<a href="{safe_url(require(source, "url"))}" rel="noopener noreferrer">{esc(require(source, "title"))}</a>. '
            f'{esc(require(source, "publisher"))}; published or updated {esc(source.get("published", "date not listed"))}; '
            f'viewed on {esc(require(source, "accessed"))}.</li>'
        )
    sources_html = (
        '<section class="slide sources" id="sources"><p class="eyebrow">Where the facts came from</p>'
        f'<h2>Sources and research notes</h2><ol>{"".join(source_items)}</ol></section>'
    )

    replacements = {
        "{{TITLE}}": esc(topic),
        "{{SUBTITLE}}": esc(require(data, "subtitle")),
        "{{AUDIENCE}}": esc(require(data, "audience")),
        "{{UPDATED}}": esc(require(data, "updated")),
        "{{NAV}}": "".join(nav),
        "{{CONTENT}}": "".join(rendered_sections),
        "{{SOURCES}}": sources_html,
        "{{GENERATED}}": esc(date.today().isoformat()),
    }
    result = template
    for token, value in replacements.items():
        result = result.replace(token, value)
    if re.search(r"\{\{[A-Z_]+\}\}", result):
        raise ValueError("Unresolved template token")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("research_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.research_json.expanduser().resolve()
    output = args.output.expanduser().resolve() if args.output else source.with_name("index.html")
    template_path = Path(__file__).resolve().parent.parent / "assets" / "deck-template.html"
    data = json.loads(source.read_text(encoding="utf-8"))
    output.write_text(render(data, template_path.read_text(encoding="utf-8")), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
