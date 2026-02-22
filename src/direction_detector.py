"""
Direction Detector - STUB FOR STUDENT IMPLEMENTATION

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

    def __init__(self, counts_file: str = "data/counts.json", delay_seconds: int = 5):
        """Initialize direction detector and load tag occurrences from JSON."""
        self.readings = {}
        self.counts_file = counts_file
        self._load_tag_occurrences()
        self.last_detection_time = {}  # Track last detection time per tag
        self.last_direction = {}  # Track last known direction per tag
        from datetime import timedelta
        self.delay = timedelta(seconds=delay_seconds)

    def _load_tag_occurrences(self):
        try:
            with open(self.counts_file, "r") as f:
                data = json.load(f)
                self.tag_occurrences = data.get("tag_occurrences", {})
        except Exception:
            self.tag_occurrences = {}

    #Stub: For RSSI Trend Analysis
    def add_reading(self, tag_id: str, rssi: float, timestamp: datetime = None) -> None:
        """
        Add an RSSI reading for a tag.
        """
        if timestamp is None:
            timestamp = datetime.now()
        reading = RFIDReading(tag_id, rssi, timestamp)
        if tag_id not in self.readings:
            self.readings[tag_id] = []
        self.readings[tag_id].append(reading)

    def detect_direction(self, tag_id: str) -> Direction:
        """
        Detect direction: if tag is not in tag_occurrences, treat as EXIT (first seen).
        Adds a debounce delay to prevent rapid direction switching.
        If not enough time has passed, keep and return the last known direction.
        """
        from datetime import datetime
        # Reload tag occurrences in case file changed
        self._load_tag_occurrences()
        now = datetime.now()
        detector = DirectionDetector(delay_seconds=5)  # 5-second delay
        last_time = self.last_detection_time.get(tag_id)
        if tag_id not in self.tag_occurrences:
            direction = Direction.EXIT
            self.last_detection_time[tag_id] = now
            self.last_direction[tag_id] = direction
            return direction
        if last_time and (now - last_time) < self.delay:
            # Not enough time has passed, return last known direction
            return self.last_direction.get(tag_id, Direction.UNKNOWN)
        direction = Direction.ENTRY
        self.last_detection_time[tag_id] = now
        self.last_direction[tag_id] = direction
        return direction
       

    def get_readings(self, tag_id: str) -> List[RFIDReading]:
        """
        Get all readings for a specific tag.

        Args:
            tag_id: Tag identifier

        Returns:
            List of RFIDReading objects
        """
        return self.readings.get(tag_id, [])

    def clear_tag(self, tag_id: str) -> None:
        """
        Clear readings and debounce state for a specific tag.

        Args:
            tag_id: Tag to clear
        """
        if tag_id in self.readings:
            del self.readings[tag_id]
        if tag_id in self.last_detection_time:
            del self.last_detection_time[tag_id]
        if tag_id in self.last_direction:
            del self.last_direction[tag_id]

    def clear_all(self) -> None:
        """Clear all stored readings and debounce state for all tags."""
        self.readings.clear()
        self.last_detection_time.clear()
        self.last_direction.clear()
