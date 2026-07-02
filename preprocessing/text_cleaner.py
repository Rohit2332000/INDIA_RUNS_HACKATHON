"""
text_cleaner.py

Centralized text preprocessing utilities used throughout the project.

These functions are reused by:
- Candidate preprocessing
- JD parsing
- Feature engineering
- Embedding generation
"""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional


class TextCleaner:
    """Utility class for text normalization."""

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Remove extra spaces."""
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def remove_html(text: str) -> str:
        """Remove HTML tags."""
        return re.sub(r"<.*?>", " ", text)

    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs."""
        return re.sub(r"http\S+|www\S+", "", text)

    @staticmethod
    def normalize_unicode(text: str) -> str:
        """Convert unicode to ASCII-friendly format."""
        return unicodedata.normalize("NFKD", text)

    @staticmethod
    def clean_text(text: Optional[str]) -> str:

        if text is None:
            return ""

        text = str(text)

        text = TextCleaner.normalize_unicode(text)

        text = TextCleaner.remove_html(text)

        text = TextCleaner.remove_urls(text)

        text = text.lower()

        # keep only letters, numbers, +, #, ., -, &
        text = re.sub(r"[^a-z0-9+#.&/\-\s]", " ", text)

        text = TextCleaner.normalize_whitespace(text)

        return text

    @staticmethod
    def clean_list(values: Optional[List]) -> List[str]:
        """
        Clean list of strings.
        """

        if values is None:
            return []

        cleaned = []

        for value in values:

            value = TextCleaner.clean_text(value)

            if value:
                cleaned.append(value)

        # Remove duplicates while preserving order
        return list(dict.fromkeys(cleaned))

    @staticmethod
    def normalize_title(title: Optional[str]) -> str:
        """
        Normalize job titles.
        """

        title = TextCleaner.clean_text(title)

        replacements = {
            "sr.": "senior",
            "sr": "senior",
            "jr": "junior",
            "sde": "software engineer",
            "ml": "machine learning",
            "ai": "artificial intelligence",
            "engg": "engineer",
            "dev": "developer",
        }

        for old, new in replacements.items():
            title = title.replace(old, new)

        return TextCleaner.normalize_whitespace(title)

    @staticmethod
    def merge_text(*texts: str) -> str:
        """
        Merge multiple text fields into one clean document.
        """

        merged = " ".join(
            TextCleaner.clean_text(t)
            for t in texts
            if t is not None
        )

        return TextCleaner.normalize_whitespace(merged)