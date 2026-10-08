"""Tests for Rebo — run with: python -m pytest tests/ (or python -m unittest)."""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rebo.packager import ReboPackager, _extract_json, render_markdown
from rebo import cli


class TestPrompts(unittest.TestCase):
    def test_shorts_prompt_shape(self):
        p = ReboPackager(api_key="dummy")
        built = p.build("Rosemary does a massive wave stunt", format="shorts",
                        niche="stunt skating", tone="energetic")
        self.assertIn("YouTube Short", built["user"])
        self.assertIn("stunt skating", built["user"])
        self.assertGreater(built["estimated_input_tokens"], 50)

    def test_video_prompt_has_chapters(self):
        p = ReboPackager(api_key="dummy")
        built = p.build("How potato chips are made", format="video")
        self.assertIn("chapters", built["user"].lower())

    def test_transcript_grounding(self):
        p = ReboPackager(api_key="dummy")
        built = p.build("My video", transcript="she lands the trick cleanly")
        self.assertIn("she lands the trick cleanly", built["user"])


class TestExtractJson(unittest.TestCase):
    def test_plain_json(self):
        pkg = _extract_json('{"titles": ["a"], "description": "b"}')
        self.assertEqual(pkg["titles"], ["a"])

    def test_fenced_json(self):
        pkg = _extract_json('```json\n{"titles": ["a"]}\n```')
        self.assertEqual(pkg["titles"], ["a"])

    def test_surrounding_chatter(self):
        pkg = _extract_json('Here you go:\n{"titles": ["a"]}\nEnjoy!')
        self.assertEqual(pkg["titles"], ["a"])

    def test_no_json_raises(self):
        with self.assertRaises(ValueError):
            _extract_json("no json here")


class TestPackager(unittest.TestCase):
    def test_dry_run_needs_no_key(self):
        env = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            p = ReboPackager()
            result = p.pack("test topic", dry_run=True)
            self.assertTrue(result["dry_run"])
            self.assertIn("test topic", result["user"])
        finally:
            if env is not None:
                os.environ["ANTHROPIC_API_KEY"] = env

    def test_missing_key_raises(self):
        env = os.environ.pop("ANTHROPIC_API_KEY", None)
        try:
            p = ReboPackager()
            with self.assertRaises(RuntimeError):
                p.pack("test topic")
        finally:
            if env is not None:
                os.environ["ANTHROPIC_API_KEY"] = env


class TestRender(unittest.TestCase):
    def test_markdown_sections(self):
        pkg = {
            "titles": ["T1", "T2"],
            "description": "Desc here",
            "hashtags": ["#a", "#b"],
            "thumbnail_text": ["BIG", "WOW"],
            "pinned_comment": "Comment!",
        }
        md = render_markdown(pkg, "My topic")
        for section in ["## Titles", "## Description", "## Hashtags",
                        "## Thumbnail text", "## Pinned comment"]:
            self.assertIn(section, md)
        self.assertIn("#a #b", md)


class TestCli(unittest.TestCase):
    def test_pack_dry_run_parses(self):
        parser = cli.build_parser()
        args = parser.parse_args(["pack", "--topic", "hello", "--dry-run"])
        self.assertEqual(args.topic, "hello")
        self.assertTrue(args.dry_run)
        self.assertEqual(args.format, "shorts")


if __name__ == "__main__":
    unittest.main()
