"""
Count Manager

Manages entry/exit counts and tag occurrence tracking with persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import json
import os


@dataclass
class CountData:
    """
    Data structure for count tracking.

    STUB: Students should implement fields:
    - daily_entry: Number of cattle entries today
    - daily_exit: Number of cattle exits today
    - net_count: Current count (entry - exit)
    - last_reset: Timestamp of last daily reset
    - total_events: Total motion events processed
    - tag_occurrences: Dict[str, int] - how many times each tag seen
    """

    daily_entry: int = 0
    daily_exit: int = 0
    net_count: int = 0
    last_reset: Optional[datetime] = None
    total_events: int = 0
    tag_occurrences: Dict[str, int] = field(default_factory=dict)


class CountManager:
    """
    Manage cattle counts and tag occurrences with JSON persistence.

    STUB: This is a placeholder implementation. Students should implement:
    - add_entry(count, tag_id): Record entry and update tag occurrence
    - add_exit(count, tag_id): Record exit and update tag occurrence
    - get_tag_occurrence_count(tag_id): Return occurrence count for tag
    - get_all_tag_occurrences(): Return full occurrence dictionary
    - reset_daily_counts(): Reset daily counts, keep tag occurrences
    - manual_reset(): Reset everything
    - _save(): Save to JSON file atomically
    - _load(): Load from JSON file

    Important: Tag occurrences increment every time a tag is seen,
    regardless of direction. They persist across daily resets.
    """

    def __init__(self, counts_file: Path = Path("data/counts.json")):
        """
        Initialize count manager.

        Args:
            counts_file: Path to JSON file for persistence
        """
        self.counts_file = counts_file
        self.counts = CountData()
        self._load()

    def add_entry(self, count: int = 1, tag_id: Optional[str] = None) -> None:
        """
        Record cattle entry.

        Args:
            count: Number of cattle entering
            tag_id: Optional tag identifier to update occurrence
        """
        self.counts.daily_entry += count
        self.counts.net_count = self.counts.daily_entry - self.counts.daily_exit
        if tag_id:
            current_occurrence = self.get_tag_occurrence_count(tag_id)
            self.counts.tag_occurrences[tag_id] = current_occurrence + count
        self._save()
        # Hint: Increment daily_entry, net_count, and tag_occurrences[tag_id]
        pass

    def add_exit(self, count: int = 1, tag_id: Optional[str] = None) -> None:
        """
        Record cattle exit.

        Args:
            count: Number of cattle exiting
            tag_id: Optional tag identifier to update occurrence
        """

        self.counts.daily_exit += count
        self.counts.net_count = self.counts.daily_entry - self.counts.daily_exit
        if tag_id:
            current_occurrence = self.get_tag_occurrence_count(tag_id)
            self.counts.tag_occurrences[tag_id] = current_occurrence + count
        self._save()
        # Hint: Increment daily_exit, decrement net_count, and tag_occurrences[tag_id]
        pass

    def get_tag_occurrence_count(self, tag_id: str) -> int:
        """
        Get occurrence count for a specific tag.

        Args:
            tag_id: Tag identifier

        Returns:
            Number of times tag has been seen
        """
        return self.counts.tag_occurrences.get(tag_id, 0)

    def get_all_tag_occurrences(self) -> Dict[str, int]:
        """
        Get all tag occurrences.

        Returns:
            Dictionary of tag_id -> count
        """
    
        return self.counts.tag_occurrences

    def reset_daily_counts(self) -> None:
        """Reset daily entry/exit counts, preserve tag occurrences."""
        self.counts.daily_entry = 0
        self.counts.daily_exit = 0
        self.counts.net_count = 0
        self.counts.last_reset = datetime.now()
        self._save()
        # Hint: Reset daily_entry, daily_exit, net_count to 0
        # IMPORTANT: Do NOT reset tag_occurrences!
        pass

    def manual_reset(self) -> None:
        self.counts.daily_entry = 0
        self.counts.daily_exit = 0
        self.counts.net_count = 0
        self.counts.tag_occurrences = {}
        self.counts.last_reset = datetime.now()
        """Reset everything including tag occurrences."""
        # TODO: Student implements
        # Hint: Reset all fields to defaults
        pass

    def _save(self) -> None:
        """Save counts to JSON file atomically."""
        data = {
            "daily_entry": self.counts.daily_entry,
            "daily_exit": self.counts.daily_exit,
            "last_reset": self.counts.last_reset.isoformat() if self.counts.last_reset else None,
            "total_events": self.counts.total_events,
            "tag_occurrences": self.counts.tag_occurrences,
        }
        temp_file = self.counts_file.with_suffix(".tmp")
        try:
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=4)
            temp_file.replace(self.counts_file)
        except Exception as e:
            if temp_file.exists():
                temp_file.unlink()  # Clean up the failed temp file
            print(f"Error saving count data: {e}")

    def _load(self) -> None:
        """Load counts from JSON file."""
        # TODO: Student implements
        # Hint: Handle missing/corrupted files gracefully
        pass
