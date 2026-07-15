"""
history_logger.py — Conversation History Logging Service

Handles reading and writing conversation history records
to the history.json file.
"""

# ──────────────────────────────────────────────
# Imports
# ──────────────────────────────────────────────
import json
from typing import List
from datetime import datetime

from config import get_settings


# ──────────────────────────────────────────────
# History Logger
# ──────────────────────────────────────────────

class HistoryLogger:
    """Manages conversation history persistence."""

    def __init__(self, file_path=None):
        """Initialize the HistoryLogger with a file path."""
        settings = get_settings()
        self.history_file = file_path or str(settings.HISTORY_FILE)

    def log_conversation(self, conversation_data: dict) -> None:
        """Append a conversation record to the history file."""
        history = self.get_history()
        conversation_data["logged_at"] = datetime.now().isoformat()
        history.append(conversation_data)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def get_history(self) -> List[dict]:
        """Retrieve all conversation history records."""
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def clear_history(self) -> None:
        """Clear all conversation history records."""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump([], f)
