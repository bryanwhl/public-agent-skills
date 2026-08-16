from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-to-interactive-deck"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = load_module("scaffold_deck", SKILL / "scripts" / "scaffold_deck.py")
builder = load_module("build_deck", SKILL / "scripts" / "build_deck.py")
validator = load_module("validate_deck", SKILL / "scripts" / "validate_deck.py")


class SkillTests(unittest.TestCase):
    def test_slugify_is_bounded_and_safe(self):
        slug = scaffold.slugify("../../A Very Long Topic! " * 20)
        self.assertLessEqual(len(slug), 60)
        self.assertRegex(slug, r"^[a-z0-9-]+$")
        self.assertNotIn("..", slug)

    def test_render_escapes_research_text_and_validates(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        data["sections"][0]["summary"] += " <script>alert(1)</script>"
        template = (SKILL / "assets" / "deck-template.html").read_text()
        rendered = builder.render(data, template)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", rendered)
        self.assertNotIn("<script>alert(1)</script>", rendered)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index.html"
            output.write_text(rendered)
            self.assertEqual(validator.validate(output), [])

    def test_rejects_unsafe_source_url(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        data["sources"][0]["url"] = "javascript:alert(1)"
        template = (SKILL / "assets" / "deck-template.html").read_text()
        with self.assertRaisesRegex(ValueError, "HTTPS"):
            builder.render(data, template)

    def test_rejects_unknown_citation(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        data["sections"][0]["points"][0]["sources"] = ["S404"]
        template = (SKILL / "assets" / "deck-template.html").read_text()
        with self.assertRaisesRegex(ValueError, "Unknown source"):
            builder.render(data, template)

    def test_rejects_formal_phrase(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        data["sections"][0]["summary"] = "People utilize this method to share data."
        template = (SKILL / "assets" / "deck-template.html").read_text()
        with self.assertRaisesRegex(ValueError, 'replace "utilize" with "use"'):
            builder.render(data, template)

    def test_rejects_sentence_over_thirty_words(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        data["sections"][0]["summary"] = " ".join(["word"] * 31) + "."
        template = (SKILL / "assets" / "deck-template.html").read_text()
        with self.assertRaisesRegex(ValueError, "30 words or fewer"):
            builder.render(data, template)

    def test_uses_simple_interface_labels(self):
        data = json.loads((ROOT / "tests" / "fixture-research.json").read_text())
        template = (SKILL / "assets" / "deck-template.html").read_text()
        rendered = builder.render(data, template)
        self.assertIn("Learn more", rendered)
        self.assertIn("Check what you learned", rendered)
        self.assertIn("Where the facts came from", rendered)
        self.assertIn("published or updated", rendered)
        self.assertIn("viewed on", rendered)
        self.assertNotIn("Retrieval practice", rendered)
        self.assertNotIn("Sources and methodology", rendered)

    def test_cli_build_and_validate_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "index.html"
            subprocess.run(
                ["python3", str(SKILL / "scripts" / "build_deck.py"), str(ROOT / "tests" / "fixture-research.json"), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            result = subprocess.run(
                ["python3", str(SKILL / "scripts" / "validate_deck.py"), str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
