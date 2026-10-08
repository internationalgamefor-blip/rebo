"""Command-line interface for Rebo."""

import argparse
import json
import sys

from .packager import DEFAULT_MODEL, ReboPackager, render_markdown


def _read_transcript(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        print(f"Could not read transcript file: {exc}", file=sys.stderr)
        sys.exit(1)


def cmd_pack(args):
    transcript = _read_transcript(args.transcript) if args.transcript else None
    packager = ReboPackager(api_key=args.api_key, model=args.model)
    try:
        package = packager.pack(
            topic=args.topic,
            format=args.format,
            niche=args.niche,
            tone=args.tone,
            transcript=transcript,
            dry_run=args.dry_run,
        )
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print("=== DRY RUN — no API call made ===\n")
        print(f"Model: {package['model']}")
        print(f"Estimated input tokens: ~{package['estimated_input_tokens']}\n")
        print("--- system prompt ---")
        print(package["system"])
        print("\n--- user prompt ---")
        print(package["user"])
        return

    if args.out == "json":
        print(json.dumps(package, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(package, args.topic))


def build_parser():
    parser = argparse.ArgumentParser(
        prog="rebo",
        description="Rebo — AI publishing packages for YouTube creators, powered by Claude.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pack = sub.add_parser("pack", help="Generate a title/description/hashtag package.")
    pack.add_argument("--topic", required=True, help="What the video is about.")
    pack.add_argument("--format", choices=["shorts", "video"], default="shorts",
                      help="Short-form or long-form package (default: shorts).")
    pack.add_argument("--niche", default="general",
                      help="Channel niche, e.g. 'stunt skating' (default: general).")
    pack.add_argument("--tone", default="energetic",
                      help="Voice of the copy, e.g. 'funny', 'cinematic' (default: energetic).")
    pack.add_argument("--transcript",
                      help="Path to a transcript/caption file to ground the copy.")
    pack.add_argument("--model", default=DEFAULT_MODEL,
                      help=f"Claude model to use (default: {DEFAULT_MODEL}).")
    pack.add_argument("--api-key",
                      help="Anthropic API key (or set ANTHROPIC_API_KEY).")
    pack.add_argument("--out", choices=["md", "json"], default="md",
                      help="Output format (default: md).")
    pack.add_argument("--dry-run", action="store_true",
                      help="Print the prompt without calling the API.")
    pack.set_defaults(func=cmd_pack)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
