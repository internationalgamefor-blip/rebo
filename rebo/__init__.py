"""Rebo — AI publishing packages for YouTube creators, powered by Claude."""

from .packager import DEFAULT_MODEL, ReboPackager, render_markdown

__all__ = ["ReboPackager", "render_markdown", "DEFAULT_MODEL"]
__version__ = "0.1.0"
