# Rebo 🤖

**AI publishing packages for YouTube creators — powered by Claude.**

Rebo is an open-source CLI that generates a complete, copy-paste-ready publishing
package for your video: 5 title options, a full description, hashtags, thumbnail
text ideas, and a pinned comment suggestion. It calls the Claude API, so the
copy is sharp, on-topic, and honest — never clickbait that misrepresents your video.

Built for creators who publish daily and need consistent, high-quality metadata
without the busywork.

## Install

```bash
git clone https://github.com/<you>/rebo.git
cd rebo
pip install -r requirements.txt
```

## Setup

Get an API key from the [Claude Console](https://console.anthropic.com/) and set it:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

```bash
# Package a YouTube Short
python -m rebo.cli pack --topic "Rosemary lands a massive wave stunt" \
  --niche "stunt skating" --tone "energetic"

# Package a long-form video, grounded in your transcript
python -m rebo.cli pack --topic "How potato chips are made" --format video \
  --niche "factory documentaries" --transcript captions.txt

# JSON output for piping into your own tooling
python -m rebo.cli pack --topic "My video" --out json > package.json

# Preview the prompt without spending API credits
python -m rebo.cli pack --topic "My video" --dry-run

# Use a different model
python -m rebo.cli pack --topic "My video" --model claude-sonnet-5
```

Default model is `claude-haiku-4-5` — fast and cheap, ideal for daily publishing.

## Example output

See [examples/sample_output.md](examples/sample_output.md) for a full package.

## How it works

1. You describe the video (`--topic`), optionally with a transcript file.
2. Rebo builds a structured prompt and sends it to the Claude API.
3. Claude returns a JSON package: titles, description, hashtags, thumbnail text,
   pinned comment.
4. Rebo renders it as copy-paste-ready Markdown (or raw JSON with `--out json`).

## Cost

A typical Shorts package uses ~250 input tokens and ~600 output tokens — a
fraction of a cent on Haiku. Publishing 3 Shorts a day costs pennies a month.

## License

MIT — see [LICENSE](LICENSE).
