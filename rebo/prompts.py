"""Prompt templates for Rebo's YouTube packaging generation."""

SYSTEM_PROMPT = """You are Rebo, an expert YouTube packaging assistant for creators.
You write titles, descriptions, hashtags and thumbnail text that are catchy and
honest — never clickbait that misrepresents the video. You always respond with
valid JSON only, no markdown fences, no commentary."""

SHORTS_USER_TEMPLATE = """Create a publishing package for a YouTube Short.

Topic: {topic}
Niche: {niche}
Tone: {tone}
{transcript_block}
Rules:
- 5 title options, each under 60 characters, punchy and curiosity-driven.
- Description: 2-3 short lines that tease the video, then hashtags on their own line.
- 10-14 hashtags: mix broad (#shorts) and niche-specific tags, no spaces inside tags.
- 3 thumbnail text ideas, each 3 words or fewer, BIG readable words.
- 1 pinned comment suggestion that invites replies.

Respond with JSON only in exactly this shape:
{{
  "titles": ["...", "...", "...", "...", "..."],
  "description": "...",
  "hashtags": ["#...", "..."],
  "thumbnail_text": ["...", "...", "..."],
  "pinned_comment": "..."
}}"""

VIDEO_USER_TEMPLATE = """Create a publishing package for a long-form YouTube video.

Topic: {topic}
Niche: {niche}
Tone: {tone}
{transcript_block}
Rules:
- 5 title options, each under 70 characters, curiosity-driven but honest.
- Description: hook paragraph, then "In this video" bullet list of 4-6 points,
  then a chapters section with plausible timestamps starting 00:00, then hashtags.
- 10-14 hashtags: mix broad and niche-specific tags, no spaces inside tags.
- 3 thumbnail text ideas, each 3 words or fewer.
- 1 pinned comment suggestion that invites replies and subscriptions.

Respond with JSON only in exactly this shape:
{{
  "titles": ["...", "...", "...", "...", "..."],
  "description": "...",
  "hashtags": ["#...", "..."],
  "thumbnail_text": ["...", "...", "..."],
  "pinned_comment": "..."
}}"""


def build_user_prompt(topic, format, niche, tone, transcript=None):
    transcript_block = ""
    if transcript:
        transcript_block = (
            "Video transcript (use it to stay accurate, do not invent details "
            "that contradict it):\n" + transcript.strip() + "\n"
        )
    template = SHORTS_USER_TEMPLATE if format == "shorts" else VIDEO_USER_TEMPLATE
    return template.format(
        topic=topic,
        niche=niche,
        tone=tone,
        transcript_block=transcript_block,
    )
