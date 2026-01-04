"""
Count Manager

Manages entry/exit counts and tag occurrence tracking with persistence.
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import json


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
        # TODO: Student implements loading from file
        self.data = CountData()

    def add_entry(self, count: int = 1, tag_id: Optional[str] = None) -> None:
        """
        Record cattle entry.

        Args:
            count: Number of cattle entering
            tag_id: Optional tag identifier to update occurrence
        """
        # TODO: Student implements
        # Hint: Increment daily_entry, net_count, and tag_occurrences[tag_id]
        pass

    def add_exit(self, count: int = 1, tag_id: Optional[str] = None) -> None:
        """
        Record cattle exit.

        Args:
            count: Number of cattle exiting
            tag_id: Optional tag identifier to update occurrence
        """
        # TODO: Student implements
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
        # TODO: Student implements
        return 0

    def get_all_tag_occurrences(self) -> Dict[str, int]:
        """
        Get all tag occurrences.

        Returns:
            Dictionary of tag_id -> count
        """
        # TODO: Student implements
        return {}

    def reset_daily_counts(self) -> None:
        """Reset daily entry/exit counts, preserve tag occurrences."""
        # TODO: Student implements
        # Hint: Reset daily_entry, daily_exit, net_count to 0
        # IMPORTANT: Do NOT reset tag_occurrences!
        pass

    def manual_reset(self) -> None:
        """Reset everything including tag occurrences."""
        # TODO: Student implements
        # Hint: Reset all fields to defaults
        pass

    def _save(self) -> None:
        """Save counts to JSON file atomically."""
        # TODO: Student implements
        # Hint: Write to temp file, then rename for atomic operation
        pass

    def _load(self) -> None:
        """Load counts from JSON file."""
        # TODO: Student implements
        # Hint: Handle missing/corrupted files gracefully
        pass
