"""Tiny placeholder-substitution template renderer."""

import re

PLACEHOLDER_PATTERN = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}"
