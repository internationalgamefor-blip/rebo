"""Core packaging logic: builds prompts, calls the Claude API, parses results."""

import json
import os
import re

from .prompts import SYSTEM_PROMPT, build_user_prompt

DEFAULT_MODEL = "claude-haiku-4-5"
MAX_TOKENS = 1500


def estimate_tokens(text):
    """Rough token estimate (~4 chars per token)."""
    return max(1, len(text) // 4)


def _extract_json(raw):
    """Pull a JSON object out of model output, tolerating code fences."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model output did not contain a JSON object.")
    return json.loads(text[start : end + 1])


class ReboPackager:
    def __init__(self, api_key=None, model=DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model

    def build(self, topic, format="shorts", niche="general", tone="energetic",
              transcript=None):
        """Return the prompt pair without calling the API (used by dry-run)."""
        user_prompt = build_user_prompt(topic, format, niche, tone, transcript)
        return {
            "system": SYSTEM_PROMPT,
            "user": user_prompt,
            "model": self.model,
            "estimated_input_tokens": estimate_tokens(SYSTEM_PROMPT + user_prompt),
        }

    def pack(self, topic, format="shorts", niche="general", tone="energetic",
             transcript=None, dry_run=False):
        built = self.build(topic, format, niche, tone, transcript)
        if dry_run:
            return {"dry_run": True, **built}

        if not self.api_key:
            raise RuntimeError(
                "No API key found. Set the ANTHROPIC_API_KEY environment "
                "variable or pass --api-key."
            )
        try:
            import anthropic
        except ImportError:
            raise RuntimeError(
                "The 'anthropic' package is not installed. "
                "Run: pip install -r requirements.txt"
            )

        client = anthropic.Anthropic(api_key=self.api_key)
        message = client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            system=built["system"],
            messages=[{"role": "user", "content": built["user"]}],
        )
        raw = message.content[0].text
        package = _extract_json(raw)
        package["model"] = self.model
        package["usage"] = {
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        }
        return package


def render_markdown(package, topic):
    """Render a package as copy-paste-ready Markdown."""
    lines = [f"# {topic}", ""]
    lines.append("## Titles")
    for i, title in enumerate(package.get("titles", []), 1):
        lines.append(f"{i}. {title}")
    lines += ["", "## Description", package.get("description", "")]
    lines += ["", "## Hashtags", " ".join(package.get("hashtags", []))]
    lines += ["", "## Thumbnail text"]
    for text in package.get("thumbnail_text", []):
        lines.append(f"- {text}")
    lines += ["", "## Pinned comment", package.get("pinned_comment", ""), ""]
    return "\n".join(lines)
