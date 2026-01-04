"""
Data Logger

Logs events to CSV with motion context and tag information.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import csv


@dataclass
class CattleEvent:
    """
    Single event in the cattle tracking system.

    You will implement fields based on CSV schema:
    - timestamp: When event occurred
    - motion_start: When motion began (for tag events)
    - motion_end: When motion ended (for tag events)
    - tag_id: Tag identifier (None for motion events)
    - direction: ENTRY/EXIT/UNKNOWN (None for motion events)
    - rssi: Signal strength (None for motion events)
    - occurrence_count: How many times tag has been seen
    - event_type: motion_start, motion_end, motion_timeout, tag_detection
    """

    timestamp: datetime
    event_type: str
    motion_start: Optional[datetime] = None
    motion_end: Optional[datetime] = None
    tag_id: Optional[str] = None
    direction: Optional[str] = None
    rssi: Optional[float] = None
    occurrence_count: Optional[int] = None


class DataLogger:
    """
    Log events to CSV file.

    Data structure:
    - log_motion_start(timestamp): Log motion detection
    - log_motion_end(timestamp): Log motion ended
    - log_motion_timeout(timestamp): Log 5s timeout reached
    - log_tag_detection(...): Log tag with direction, RSSI, occurrence
    - get_recent_events(n): Return last N events from CSV
    - _write_event(event): Append event to CSV file

    CSV Schema:
    timestamp,motion_start,motion_end,tag_id,direction,rssi,occurrence_count,event_type
    """

    def __init__(self, log_file: Path = Path("data/events.csv")):
        """
        Initialize data logger.

        Args:
            log_file: Path to CSV file for event logging
        """
        self.log_file = log_file
        # TODO: create file with headers

    def log_motion_start(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion detection event.

        Args:
            timestamp: When motion started (defaults to now)
        """
        # TODO: Log the motion event
        pass

    def log_motion_end(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion ended event.

        Args:
            timestamp: When motion ended (defaults to now)
        """
        # TODO: Log when motion has ended
        pass

    def log_motion_timeout(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion timeout event (5s after last motion).

        Args:
            timestamp: When timeout occurred (defaults to now)
        """
        # TODO: Log when lotion has timed out
        pass

    def log_tag_detection(
        self,
        tag_id: str,
        direction: str,
        rssi: float,
        occurrence_count: int,
        motion_start: datetime,
        motion_end: datetime,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Log tag detection with full context.

        Args:
            tag_id: Tag identifier
            direction: ENTRY/EXIT/UNKNOWN
            rssi: Signal strength in dBm
            occurrence_count: How many times tag has been seen
            motion_start: When motion event started
            motion_end: When motion event ended
            timestamp: When tag was detected (defaults to now)
        """
        # TODO: Log the tag that has been detected and all relevant data
        pass

    def get_recent_events(self, n: int = 10) -> List[CattleEvent]:
        """
        Get the most recent N events from the log.

        Args:
            n: Number of events to retrieve

        Returns:
            List of CattleEvent objects (newest first)
        """
        # TODO: Read CSV to return last n events
        # Hint: Read CSV, parse rows, return last N events
        return []

    def _write_event(self, event: CattleEvent) -> None:
        """
        Write event to CSV file.

        Args:
            event: Event to write
        """
        # TODO: Write new event to CSV file
        # Hint: Use csv.DictWriter to append row
        pass
