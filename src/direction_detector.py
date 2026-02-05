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

    def __init__(self, min_samples: int = 3, rssi_delta_threshold: float = 5.0):
        """Initialize direction detector.
        
        Args:
            min_samples: Minimum number of readings required for direction detection
            rssi_delta_threshold: Minimum RSSI change (dBm) to determine direction
        """
        self.min_samples = min_samples
        self.rssi_delta_threshold = rssi_delta_threshold
        self._readings = {}  # Dict[str, List[RFIDReading]]

    def add_reading(self, tag_id: str, rssi: float, timestamp: datetime = None) -> None:
        """
        Add an RSSI reading for a tag.

        Args:
            tag_id: Tag identifier
            rssi: Signal strength in dBm
            timestamp: When reading was taken (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now()

        reading = RFIDReading(tag_id=tag_id, rssi=rssi, timestamp=timestamp)

        if tag_id not in self._readings:
            self._readings[tag_id] = []

        self._readings[tag_id].append(reading)

    def detect_direction(self, tag_id: str) -> Direction:
        """
        Determine movement direction based on RSSI trend.

        Args:
            tag_id: Tag to analyze

        Returns:
            Direction: ENTRY if signal strengthening, EXIT if weakening, UNKNOWN otherwise
        """
        # Get readings for this tag
        readings = self._readings.get(tag_id, [])

        # Need minimum samples to determine direction
        if len(readings) < self.min_samples:
            return Direction.UNKNOWN

        # Calculate RSSI delta (last - first)
        rssi_delta = readings[-1].rssi - readings[0].rssi

        # Check if change is significant enough
        if abs(rssi_delta) < self.rssi_delta_threshold:
            return Direction.UNKNOWN

        # Determine direction based on trend
        if rssi_delta > 0:
            return Direction.ENTRY  # Signal getting stronger (approaching)
        return Direction.EXIT  # Signal getting weaker (departing)

    def get_readings(self, tag_id: str) -> List[RFIDReading]:
        """
        Get all readings for a specific tag.

        Args:
            tag_id: Tag identifier

        Returns:
            List of RFIDReading objects
        """
        return self._readings.get(tag_id, [])

    def clear_tag(self, tag_id: str) -> None:
        """
        Clear readings for a specific tag.

        Args:
            tag_id: Tag to clear
        """
        if tag_id in self._readings:
            del self._readings[tag_id]

    def clear_all(self) -> None:
        """Clear all stored readings."""
        self._readings.clear()
