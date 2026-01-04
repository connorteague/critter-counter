"""
Direction Detector - STUB FOR STUDENT IMPLEMENTATION

Determines cattle movement direction (ENTRY/EXIT) based on RSSI signal trends.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


class Direction(Enum):
    """Direction of cattle movement."""

    ENTRY = "entry"
    EXIT = "exit"
    UNKNOWN = "unknown"


@dataclass
class RFIDReading:
    """Single RFID tag reading with signal strength."""

    tag_id: str
    rssi: float
    timestamp: datetime
    antenna: Optional[int] = None


class DirectionDetector:
    """
    Detect cattle movement direction based on RSSI trends.

    NOTE: This is a placeholder implementation. You will implement:
    - add_reading(tag_id, rssi, timestamp): Store RSSI sample
    - detect_direction(tag_id): Analyze trend and return Direction
    - get_readings(tag_id): Return all readings for a tag
    - clear_tag(tag_id): Clear readings for one tag
    - clear_all(): Clear all stored readings

    Algorithm hint: RSSI increasing = ENTRY, decreasing = EXIT
    See docs/algorithm_notes.md for details.
    """

    def __init__(self):
        """Initialize direction detector."""
        # TODO: Implements data structure to track readings per tag
        pass

    def add_reading(self, tag_id: str, rssi: float, timestamp: datetime = None) -> None:
        """
        Add an RSSI reading for a tag.

        Args:
            tag_id: Tag identifier
            rssi: Signal strength in dBm
            timestamp: When reading was taken (defaults to now)
        """
        # TODO: Implementation
        pass

    def detect_direction(self, tag_id: str) -> Direction:
        """
        Determine movement direction based on RSSI trend.

        Args:
            tag_id: Tag to analyze

        Returns:
            Direction: ENTRY if signal strengthening, EXIT if weakening, UNKNOWN otherwise
        """
        # TODO: Implementation
        # Hint: Compare first_rssi vs last_rssi, check delta threshold
        return Direction.UNKNOWN

    def get_readings(self, tag_id: str) -> List[RFIDReading]:
        """
        Get all readings for a specific tag.

        Args:
            tag_id: Tag identifier

        Returns:
            List of RFIDReading objects
        """
        # TODO: Implementation
        return []

    def clear_tag(self, tag_id: str) -> None:
        """
        Clear readings for a specific tag.

        Args:
            tag_id: Tag to clear
        """
        # TODO: Implementation
        pass

    def clear_all(self) -> None:
        """Clear all stored readings."""
        # TODO: Implementation
        pass
