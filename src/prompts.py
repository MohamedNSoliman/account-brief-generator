"""
Prompt templates and structures for account brief generation.
"""

from typing import List


def format_competitors_display(competitors: List[str]) -> str:
    """Format competitor list for display in text."""
    if len(competitors) == 1:
        return competitors[0]
    return ", ".join(competitors[:-1]) + f", and {competitors[-1]}"
